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

# Get SQLAlchemy Session
def get_db_session():
    db_conn_string = 'postgresql+auroradataapi://:@/' + database_name
    
    logger.info(f'Creating SQLAlchemy database engine for database: "{database_name}"')
    engine = create_db_engine(db_conn_string, db_cluster_arn, secret_arn)
    session = create_db_session(engine)
    return session

session = get_db_session()

def get_assignment(assignmentId):
    lambdaClient = boto3.client('lambda')
    response = lambdaClient.invoke(
        FunctionName=f'{os.getenv("SERVICE_NAME")}-{os.getenv("STAGE")}-getAssignment',
        InvocationType='RequestResponse',
        Payload={
            "pathParameters": {
                "assignment_id": assignmentId 
            }
        }
    )
    return response["body"]


def do_assignment(userId, assignmentId, achievedPoints):
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

def check_test_status(testId, userId):
    assignments_done = Assignment.query.join(DoAssignment).filter(and_(Assignment.test_id == testId, DoAssignment.user_id == userId))
    logger.info(f'User: {userId} did following assignments: {assignments_done}')
    assignments_total = Assignment.query.join(Test).filter(Assignment.test_id == testId)
    logger.info(f'For test: {testId} following assignments are assigned: {assignments_total}')



def handler(event, context):
    req = json.loads(event["body"])

    assignment = get_assignment(req["assignment_id"])
    logger.info(f'Found assignment: {assignment}')
    check_test_status(assignment['test_id'], req['user_id'])
    
    # Check answer
    if req["answer"] == assignment["answer"]:
        points = assignment["points"]
    else:
        points = 0

    if (event['httpMethod'] == 'POST'):
        response = do_assignment(req["user_id"], req["assignment_id"], points)
    else:
        raise Exception(f"No handler for http verb: {event['httpMethod']}")
        
    return response