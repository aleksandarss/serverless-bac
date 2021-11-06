const AWS = require('aws-sdk');
const uuid = require('uuid');
const moment = require('moment');

AWS.config.update({
    reqgion: 'us-east-1'
});

const createProduct = async (body) => {
    try {
        const dynamoClient = new AWS.DynamoDB.DocumentClient();

        const params = prepareParams(body);
        await dynamoClient.put(params).promise();
        return {
            product: params.Item
        }
    } catch (err) {
        console.error('Something went wrong: ', err);
        throw err;
    }
}

const prepareParams = (body) => {
    return {
        TableName: process.env.TABLE_NAME,
        Item: {
            'id': uuid.v4(),
            'name': body.name,
            'description': body.description,
            'created_at': moment().toISOString(),
        }
    }
}

module.exports = {
    createProduct
}