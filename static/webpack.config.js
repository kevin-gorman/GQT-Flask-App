const webpack = require('webpack');
const config = {
    devtool: 'eval-source-map',
    entry: __dirname + '/js/eventflow.js',
    output:{
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js','.jsx','.css']
    },
    module: {
        rules: [
            {
                test: /\.jsx?/,
                loader: 'babel-loader',
            //    exclude: /node_modules/,
                query:{
                    presets: ['react','es2015']
                }
            },
            {
                test: /\.css$/,
                loader: 'style-loader!css-loader',
            }
        ]
    }
};
module.exports = config;