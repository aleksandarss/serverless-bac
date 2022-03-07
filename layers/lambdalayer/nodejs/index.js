
const hello = () => {
    console.log('Hello from lambda layer!');
}

module.exports = {
    hello
}

// to require:
// const layer = require('/opt/nodejs/index.js')