import json
from models.db_models import TakeCourse, Test, Course
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

def progress_course(body, progress):
    logger.info(f'Updating course progress for body: {body}')
    try:
        course_id = body['course_id']
        user_id = body['user_id']

        take_course = session.query(TakeCourse).filter(
            TakeCourse.user_id == user_id,
            TakeCourse.course_id == course_id
        ).first()

        take_course.progress += progress
        logger.debug(f'TakeCourse after updating is: {take_course}')

        session.add(take_course)
        session.commit()
        session.refresh(take_course)

        return {
            "statusCode": 200,
            "body": json.dumps(take_course.as_dict())
        }
    except Exception as e:
        logger.error(f'Something went wrong while progressing course - {e}')
        return {
            "statusCode": 500,
            "error": f"Error: {e}"
        }


def get_test_count(courseId):
    logger.debug(f'Fetching number of tests of course: {courseId}')
    tests = session.query(Test).join(Course).filter(Course.id == courseId).all()
    return len(tests)


def calculate_progress(testCount):
    logger.debug(f'Calculating course progress for: {testCount}# of tests.')
    return 100 / testCount


def handler(event, context):
    logger.info(f'Received event to progress course - {event}')
    records = event['Records']
    response = {}

    for record in records:
        body = json.loads(record['body'])
        test_count = get_test_count(body['course_id'])
        progress = calculate_progress(test_count)
        response = progress_course(body, progress)
        
    return response