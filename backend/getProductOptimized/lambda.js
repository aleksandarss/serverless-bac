"use strict"
const getProductController = require('./getProductController');
exports.handler = async (event, context) => {
    const {statusCode, responseBody} = await getProductController.getProduct(event);
    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "access-control-allow-origin": "*"
        },
        "body": JSON.stringify(responseBody),
        "isBase64Encoded": false
    }
}