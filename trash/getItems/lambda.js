const serverless = require('serverless-http');
const express = require('express');
const bodyParser = require('body-parser');
const getItemController = require('./getItemController');
const { NotFoundError } = require('./customErrors');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/item-get/:itemId', async (req, res) => {
    try {
        if (!req.params.itemId) {
            res.status(400);
            return res.json({ error: 'A valid item id must be provided' });
        }
        
        const item = await getItemController.getItem(req.params.itemId);

        res.status(200);
        return res.json({
            item: item.Items[0]
        });
    } catch (err) {
        console.log('Something went wrong in item-get view: ', err.message);
        err instanceof NotFoundError ? res.status(404) : res.status(500);
        return res.json({
            error: err.message
        });
    }    
});

module.exports.handler = serverless(app);