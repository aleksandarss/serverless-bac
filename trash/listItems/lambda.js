const serverless = require('serverless-http');
const express = require('express');
const bodyParser = require('body-parser');
const listItemsController = require('./listItemsController');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/item-list', async (req, res) => {
    try {        
        const items = await listItemsController.listItems();

        res.status(200);
        return res.json({
            items
        });
    } catch (err) {
        console.log('Something went wrong in item-list view: ', err.message);
        err instanceof NotFoundError ? res.status(404) : res.status(500);
        return res.json({
            error: err.message
        });
    }    
});

module.exports.handler = serverless(app);