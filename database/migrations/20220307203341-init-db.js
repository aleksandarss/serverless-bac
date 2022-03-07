module.exports = {
  up: (queryInterface) => {
    const { migrate } = require('./utils/index');
    return migrate(__filename, queryInterface);
  },
  down: () => Promise.reject(new Error('error'))
};
