import json
from models.db_models import TakeTest, DoAssignment, Assignment
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

def complete_test(body, points):
    try:
        logger.info(f"inserting TakeTest with points: [{points}] into the db ...")
        completeTest = TakeTest(
            points = points,
            user_id = int(body['user_id']),
            test_id = int(body['test_id'])
        )

        session.add(completeTest)
        session.commit()
        session.refresh(completeTest)
        logger.info(f"inserted TakeTest: {completeTest.as_dict()}")
        return {
            "statusCode": 200,
            "body": json.dumps(completeTest.as_dict())
        }
    except Exception as e:
        logger.error(f"Something went wrong during insert - {e}")
        return {
            "statusCode": 500,
            "error": f"Error: {e}"
        }

def calculate_points(testId, userId):
    assignments_done = session.query(DoAssignment).join(Assignment).filter(and_(
        Assignment.test_id == testId,
        DoAssignment.user_id == userId
    )).all()
    total_points = 0
    for row in assignments_done:
        print('Done ASSIGNMENT: ', row.__dict__)
        total_points += row.achieved_points
    logger.info(f'user [{userId}] achieved [{total_points}] on test [{testId}]')

    return total_points

def get_test(testId):
    logger.debug(f'invoking get-test lambda')
    lambdaClient = boto3.client('lambda')
    response = lambdaClient.invoke(
        FunctionName='test-service-dev-getTest', 
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "pathParameters": {
                "test_id": testId
            },
            "httpMethod": 'GET'
        })
    )
    result = json.loads(response['Payload'].read())
    logger.debug(f'received response from get-test lambda: {result}')
    return json.loads(result['body'])


def progress_course(testId, userId, achievedPoints):
    logger.info(f'Sending message to queue to progress course for user: {userId}')
    test = get_test(testId)
    if achievedPoints >= test['total_points'] / 2:
        logger.info(f'Sending complete test body to queue: {os.getenv("PROGRESS_COURSE_QUEUE_URL")}')
        response = sqs_client.send_message(
            QueueUrl=os.getenv('PROGRESS_COURSE_QUEUE_URL'),
            MessageBody=f'{{ "course_id": {test["course_id"]}, "user_id": {userId} }}'
        )
        logger.info(f'Received response from queue: {response}') 


def handler(event, context):
    print(event)
    response = {}
    records = event['Records']

    for record in records:
        body = json.loads(record['body'])
        achievedPoints = calculate_points(body['test_id'], body['user_id'])
        response = complete_test(body, achievedPoints)
        progress_course(body['test_id'], body['user_id'], achievedPoints)
    
    return response
