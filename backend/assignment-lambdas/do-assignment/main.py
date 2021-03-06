import json
from models.db_models import Test, TakeTest, Assignment, DoAssignment
from utils import create_db_engine, create_db_session
from sqlalchemy import and_
import boto3
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
db_cluster_arn = os.getenv('DB_CLUSTER_ARN')
secret_arn = os.getenv('DB_SECRET_ARN')
database_name = os.getenv('DB_NAME')
secrets_client = boto3.client('secretsmanager')
sqs_client = boto3.client('sqs')

# Get SQLAlchemy Session
def get_db_session():
    db_conn_string = 'postgresql+auroradataapi://:@/' + database_name
    
    logger.info(f'Creating SQLAlchemy database engine for database: "{database_name}"')
    engine = create_db_engine(db_conn_string, db_cluster_arn, secret_arn)
    session = create_db_session(engine)
    return session

session = get_db_session()

def get_assignment(assignmentId):
    logger.debug(f'invoking get-assignment lambda with path param: {assignmentId}')
    lambdaClient = boto3.client('lambda')
    response = lambdaClient.invoke(
        FunctionName='assignment-service-dev-getAssignment', # f'{os.getenv("SERVICE_NAME")}-{os.getenv("STAGE")}-getAssignment',
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "pathParameters": {
                "assignment_id": assignmentId 
            },
            "httpMethod": 'GET'
        })
    )
    result = json.loads(response['Payload'].read())
    logger.debug(f'received response from get-assignment lambda: {result}')
    return json.loads(result['body'])


def do_assignment(userId, assignmentId, achievedPoints):
    logger.debug('inserting doAssignment into db ...')
    try:
        doAssignment = DoAssignment(
            achieved_points = achievedPoints,
            user_id = userId,
            assignment_id = assignmentId
        )

        session.add(doAssignment)
        session.commit()
        session.refresh(doAssignment)

        return {
            "statusCode": 200,
            "body": json.dumps(doAssignment.as_dict())
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "error": f"Error: {e}"
        }

"""
Checks if all the assignments are already done.
returns:
True if the assignment can be done - done assignment count is < total assignment count
Fals if the assignment can't be done - done assignment count is == total assignment count
"""
def check_test_status(testId, userId):
    logger.debug(f'checking test status for test: {testId} user: {userId}')
    assignments_done = session.query(DoAssignment).join(Assignment).filter(and_(
        Assignment.test_id == testId,
        DoAssignment.user_id == userId
    )).all()
    logger.info(f'User: {userId} did following assignments: {assignments_done}')
    logger.info(f'User: {userId} did {len(assignments_done)}#')
    assignments_total = session.query(Assignment).join(Test).filter(Assignment.test_id == testId).all()
    for assignment in assignments_total:
        print("ASSIGNMENT: ", assignment.__dict__)

    if len(assignments_done) == len(assignments_total):
        return False
    else:
        return True


def complete_test(testId, userId):
    logger.info(f'Sending complete test body to queue: {os.getenv("COMPLETE_TEST_QUEUE_URL")}')
    response = sqs_client.send_message(
        QueueUrl=os.getenv('COMPLETE_TEST_QUEUE_URL'),
        MessageBody=f'{{ "test_id": {testId}, "user_id": {userId} }}'
    )
    logger.info(f'Received response from queue: {response}')



def handler(event, context):
    req = json.loads(event["body"])

    assignment = get_assignment(req["assignment_id"])

    if check_test_status(assignment['test_id'], req['user_id']):
        # Check answer
        if req["answer"] == assignment["answer"]:
            points = assignment["points"]
        else:
            points = 0
        response = do_assignment(req["user_id"], req["assignment_id"], points)
        
        # Check if test done after this assignment
        if not check_test_status(assignment['test_id'], req['user_id']):
            # Complete test
            complete_test(assignment['test_id'], req['user_id'])

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "You have already done all assignments for this test!"})
        }
        
    return response