const path = require('path');
const webpack = require('webpack');
const Dotenv = require('dotenv-webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

// importLoader:1 from https://blog.madewithenvy.com/webpack-2-postcss-cssnext-fdcd2fd7d0bd
const envPath = path.resolve(__dirname, '../../.env');

module.exports = {
    // devtool: 'source-map', // No need for dev tool in production


    plugins: [
        new ExtractTextPlugin('styles/[name].css'),
        new webpack.optimize.OccurrenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            }
        }),
        new Dotenv({
            path: envPath
        })
    ]
};
