const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const extractVueSCSS = new MiniCssExtractPlugin({
	filename: 'css/vue.css'
});

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
	  },
	  {
        test: /\.(sass|scss)$/,
        use: [
			process.env.NODE_ENV !== 'production'
            	? 'vue-style-loader'
				: MiniCssExtractPlugin.loader,
			'vue-style-loader',
			'css-loader',
			'sass-loader'
		]
	  },
	  {
		test: /\.(eot|svg|ttf|woff|woff2)$/,
		use: [
				 {
					 loader: 'file-loader?name=../fonts/webfonts/[name].[ext]'
				 },
				 {
					 loader: 'file-loader?name=../fonts/Roboto/[name].[ext]'
				 }
			 ]
		},
		{
			test: /\.(png|jpg|jpeg|gif)$/,
			use: [
					 {
						 loader: 'file-loader?name=../assets/images/[name].[ext]'
					 }
				 ]
			}
    ]
  },
  plugins: [
	new VueLoaderPlugin(),
	extractVueSCSS
  ],
  externals: {
    'vue': 'Vue'
  }
};
module.exports = config;
