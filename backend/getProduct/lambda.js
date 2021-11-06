const serverless = require('serverless-http');
const express = require('express');
const bodyParser = require('body-parser');
const getProductController = require('./getProductController');
const { NotFoundError } = require('./customErrors');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/product-get/:productId', async (req, res) => {
    try {
        if (!req.params.productId) {
            res.status(400);
            return res.json({ error: 'A valid product id must be provided' });
        }
        
        const product = await getProductController.getProduct(req.params.productId);

        res.status(200);
        return res.json({
            product
        });
    } catch (err) {
        console.log('Something went wrong in product-get view: ', err.message);
        err instanceof NotFoundError ? res.status(404) : res.status(500);
        return res.json({
            error: err.message
        });
    }    
});

module.exports.handler = serverless(app);