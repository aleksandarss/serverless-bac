- npm install -g amplify
- amplify configure: 
    - created new iam user: amplify-xxxxx
    - added profile 'amplify' to aws config
- amplify init:
    - a signup role was created
    - a sign in role was created
    - an s3 bucket was created
- amplify import auth
    - imported user pool
    - had to add web app without secret to user pool manually

** ASSIGNMENTS **
* All assignments are 5 points worth
* There are no partially correct answers
* 

** TEST **
- Start-test only writes entry into the DB
- The logic for doing assignments is in /do-assignment route

** OPEN QUESTIONS **
Q: How to know that the test ended?
A: Look at the number of assignments user completed vs number of assignments that belong to that test.
   Do check after every /do-assignment call 

***03.04.2022***

* Problem:
 - Detected error: No module named '_tkinter'.
 - Only reference to 'tkinter' found in dpdeps layer, no idea how it got installed. 
* Solutions:
 - Removed six.py from dbdeps/python
* Solution: 
 - a module got imported by vs autocomplete in the db_models.py

***17.04.2022***
* Finish test:
    - do assignment lambda writes a message to queue with body containing necessary info to complete the test
    `client = boto3.client('sqs')
    response = client.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/552166557473/MyQueue',
        MessageBody='{ "message": "Handle this mafadaka!!!" }'
    )`

    - complete test lambda is triggered by the SQS Queue
    - Example event from the queue:
    `{'Records': [{'messageId': '08118c7a-e4c8-49e0-bc25-1763c2207aa3', 'receiptHandle': 'AQEBS0So0ZQYA2Ln71ZyErVjfZyBA64P2JUVqOGw0iq1xhydQr5nUPeo71lp3NmWlNKFV8/P4orsBeCmmEVfS3cVNsgWJAkPJmtpVggd4J5K6LmBQvL8XZhDtfUDUrK5xH3CVLF5L7Q8CW6/qtJbCLevXsCr/4ZzS1bI52RRI+JD7gqv179nAAJaxQ82wZJsLkiq1t6OlgBABg/MkWk0xKOqVGNswmjJmC1eBlyaN1zI787V8d1jEi5b9eCj21iJCYA4yD0IogDMA77Wewf1xMpBeBHrr/wmpiWpARXltj2ZIKI3eIU9AVymO52LNwKCbgryvjMRjD+S/H3BcJ4hn63HmtV76StPJP0lsaE/87jj7T32GSjnsNC8gP6hxl3OsVUF', 'body': '{ "message": "Handle this mafadaka!!!" }', 'attributes': {'ApproximateReceiveCount': '1', 'SentTimestamp': '1650190317701', 'SenderId': 'AROAYBD5RA4QQD5LV26LN:setterFunc', 'ApproximateFirstReceiveTimestamp': '1650190317708'}, 'messageAttributes': {}, 'md5OfBody': 'd821d12bc08f2c14e924337e0baea522', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:us-east-1:552166557473:MyQueue', 'awsRegion': 'us-east-1'}]}` 

* Progress course - same as above

* For tomorrow:
- Progress course logic:
- add logic to fetch existing course logic
- do addition of calculated course progress from the completed test and add to existing course progress
- just call all the defined functions in correct order and it should work


