const serverless = require('serverless-http');
const express = require('express');
const bodyParser = require('body-parser');
const createProductController = require('./createProductController');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/product-create', async (req, res) => {
    try {
        if (!req.body) {
            res.status(400);
            return res.json({ error: 'Body must be valid.' });
        }
        
        let newProduct = await createProductController.createProduct(req.body);

        res.status(201);
        return res.json(newProduct);
    } catch (err) {
        console.log('Something went wrong in product-create view: ', err.message);
        return res.json({
            error: err.message
        });
    }    
});

module.exports.handler = serverless(app);