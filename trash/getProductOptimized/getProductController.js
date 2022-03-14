const AWS = require('aws-sdk');
const { NotFoundError } = require('./customErrors');

AWS.config.update({
    region: 'us-east-1'
});

const getProduct = async (event) => {
    try {
        const { productId } = event.pathParameters;
        const dynamoClient = new AWS.DynamoDB.DocumentClient();

        const params = prepareParams(productId);
        const product = await dynamoClient.query(params).promise();
        if (product) {
            let items = await getItems();
            return {
                responseBody: mergeItemsProduct(product.Items[0], items),
                statusCode: 200
            }
        } else {
            return Promise.reject(new NotFoundError(`Product with the id = [${productId}] not found.`));
        }
    } catch (err) {
        console.error('Something went wrong in getProduct controller: ', err.message);
        throw err;
    }
}

const prepareParams = (productId) => {
    return {
        TableName: process.env.TABLE_NAME,
        KeyConditionExpression: '#id = :id',
        ExpressionAttributeNames: {
            '#id': 'id'
        },
        ExpressionAttributeValues: {
            ':id': productId
        }
    }
}

const getItems = async (productId) => {
    try {
        const lambdaClient = new AWS.Lambda();

        const params = {
            FunctionName: 'sls-list-items-dev-api',
            InvocationType: 'RequestResponse',
            Payload: JSON.stringify({
                path: '/item-list',
            })
        }

        const lambdaInvocation = await lambdaClient.invoke(params).promise();
        let parsed = JSON.parse(lambdaInvocation.Payload)
        let parsedBody = JSON.parse(parsed.body);
        return parsedBody.items;
    } catch (err) {
        console.error('Something went wrong in getItems method: ', err.message);
        throw err;
    }
}

const mergeItemsProduct = (product, items) => {
    console.log('ITEMS ARE: ', items);
    console.log('PRODUCT IS: ', product);
    let filteredItems = items.filter(elem => elem.product_id === product.id);
    return {...product, items: filteredItems}
}

module.exports = {
    getProduct
}