const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

const config = {
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
  entry: {
    'main': './src/js/app.js'
  },
  output: {
    filename: 'main.min.js',
    path: path.resolve(__dirname, 'public', 'js')
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      }
    ]
  },
  plugins: [
    new VueLoaderPlugin()
  ],
  externals: {
    'vue': 'Vue'
  }
};
module.exports = config;
