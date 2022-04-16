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

# Get SQLAlchemy Session
def get_db_session():
    db_conn_string = 'postgresql+auroradataapi://:@/' + database_name
    
    logger.info(f'Creating SQLAlchemy database engine for database: "{database_name}"')
    engine = create_db_engine(db_conn_string, db_cluster_arn, secret_arn)
    session = create_db_session(engine)
    return session

session = get_db_session()

def complete_test(event, points):
    try:
        logger.info(f"inserted TakeTest with points: [{points}] into the db ...")
        req = event['body']
        completeTest = TakeTest(
            points = points,
            user_id = int(req['user_id']),
            test_id = int(req['test_id'])
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


def handler(event, context):
    print(event)
    req = event['body']
    total_points = calculate_points(req['test_id'], req['user_id'])
    response = complete_test(event, total_points)
        
    return response

