module.exports = {
    devServer: {
      clientLogLevel: 'info',
      publicPath: '/',
      proxy: {
        '^/api': {
          target: 'http://localhost:5000',
          changeOrigin: true
        }
      }
    },
  };