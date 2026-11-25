
const app = require('./app');
const Eureka = require('eureka-js-client').Eureka;

const PORT = parseInt(process.env.PORT || '8083', 10);

const client = new Eureka({
  instance: {
    app: 'MEETING',
    instanceId: `MEETING:${PORT}`,
    hostName: 'localhost',
    ipAddr: '127.0.0.1',

    port: {
      '$': PORT,
      '@enabled': true
    },

    vipAddress: 'MEETING',
    statusPageUrl: `http://localhost:${PORT}/info`,
    healthCheckUrl: `http://localhost:${PORT}/health`,

    dataCenterInfo: {
      '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
      name: 'MyOwn'
    }
  },

  eureka: {
    host: 'localhost',
    port: 8761,
    servicePath: '/eureka/apps/'
  }
});

app.listen(PORT, () => {
  console.log(`Meeting running on http://localhost:${PORT}`);

  client.start((error) => {
    if (error) {
      console.error('Erreur inscription Eureka:', error);
    } else {
      console.log('MEETING enregistré dans Eureka !');
    }
  });
});
