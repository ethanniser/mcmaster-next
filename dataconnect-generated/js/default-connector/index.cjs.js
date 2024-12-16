const { getDataConnect, validateArgs } = require('firebase/data-connect');

const connectorConfig = {
  connector: 'default',
  service: 'next-faster-data-connect',
  location: 'us-east1'
};
exports.connectorConfig = connectorConfig;

