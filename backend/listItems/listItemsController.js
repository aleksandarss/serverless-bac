const AWS = require('aws-sdk');

const listItems = async () => {
    try {
        const dynamoClient = new AWS.DynamoDB.DocumentClient();

        const result = [];
        let items;
        let params = prepareParams();
        do {
            items = await dynamoClient.scan(params).promise();
            items.Items.forEach(item => result.push(item));
            params.ExclusiveStartKey = items.LastEvaluatedKey;
        } while (typeof items.LastEvaluatedKey !== 'undefined');

        return result;
    } catch (err) {
        throw err;
    }
}

const prepareParams = () => {
    return {
        TableName: process.env.TABLE_NAME
    }
}

module.exports = {
    listItems
}