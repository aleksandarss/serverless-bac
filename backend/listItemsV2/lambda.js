const serverless = require('serverless-http');
const express = require('express');
const bodyParser = require('body-parser');
const listItemsController = require('/opt/listItemsLayer/index.js');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/v2/item-list', async (req, res) => {
    try {        
        const items = await listItemsController.listItems();

        res.status(200);
        return res.json({
            items
        });
    } catch (err) {
        console.log('Something went wrong in item-list view: ', err.message);
        res.status(500);
        return res.json({
            error: err.message
        });
    }
});

module.exports.handler = serverless(app);