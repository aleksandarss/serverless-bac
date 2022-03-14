const AWS = require('aws-sdk');
const { NotFoundError } = require('./customErrors');

AWS.config.update({
    region: 'us-east-1'
});

const getItem = async (itemId) => {
    try {
        const dynamoClient = new AWS.DynamoDB.DocumentClient();

        const params = prepareParams(itemId);
        const item = await dynamoClient.query(params).promise();
        if (item) {
            return item;
        } else {
            return Promise.reject(new NotFoundError(`Item with the id = [${itemId}] not found.`));
        }
    } catch (err) {
        console.error('Something went wrong in getItem controller: ', err.message);
        throw err;
    }
}

const prepareParams = (itemId) => {
    return {
        TableName: process.env.TABLE_NAME,
        KeyConditionExpression: '#id = :id',
        ExpressionAttributeNames: {
            '#id': 'id'
        },
        ExpressionAttributeValues: {
            ':id': itemId
        }
    }
}

module.exports = {
    getItem
}