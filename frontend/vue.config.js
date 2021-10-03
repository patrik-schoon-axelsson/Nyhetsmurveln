module.exports = {
    devServer: {
      outputDir: './../dist',
      publicPath: '/',
      proxy: {
        '^/api': {
          target: 'http://localhost:5000',
          changeOrigin: true
        }
      }
    }
  };