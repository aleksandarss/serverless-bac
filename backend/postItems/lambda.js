const serverless = require('serverless-http');
const express = require('express');
const bodyParser = require('body-parser');
const createItemController = require('./createItemController');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/item-create', async (req, res) => {
    try {
        if (!req.body) {
            res.status(400);
            return res.json({ error: 'Body must be valid.' });
        }
        
        let newItem = await createItemController.createItem(req.body);

        res.status(201);
        return res.json({
            newItem
        });
    } catch (err) {
        console.log('Something went wrong in item-create view: ', err.message);
        return res.json({
            error: err.message
        });
    }    
});

module.exports.handler = serverless(app);