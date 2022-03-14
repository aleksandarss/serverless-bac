import json
from models.db_models import Test
from utils import create_db_engine, create_db_session
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

def get_test(event):
    try:
        test_id = event['pathParameters']['test_id']

        test = session.query(Test).get(int(test_id))

        return {
            "statusCode": 200,
            "body": json.dumps(test.as_dict())
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "error": f"Error: {e}"
        }

def handler(event, context):
    if (event['httpMethod'] == 'GET'):
        response = get_test(event)
    else:
        raise Exception(f"No handler for http verb: {event['httpMethod']}")
        
    return response