const webpack = require('webpack');
const config = require('./config.json');

const NODE_ENV = process.env.NODE_ENV || 'development'; // production|development
const API_PREFIX = process.env.API_PREFIX || config.API_PREFIX;
const IS_DEV = NODE_ENV == 'development';

let plugins = [
    new webpack.DefinePlugin({
        'process.env': {
            'NODE_ENV': JSON.stringify(NODE_ENV),
            'API_PREFIX': JSON.stringify(API_PREFIX)
        }
    })
];

if (!IS_DEV) {
    plugins.push(
        new webpack.optimize.UglifyJsPlugin({minimize: true})
    );
}

module.exports = {
    watch: IS_DEV,
    //http://webpack.github.io/docs/configuration.html#devtool
    devtool: IS_DEV ? '#module-eval-source-map' : false,
    entry: {
        'private'  : './jsx/private/index.js',
        'polyfill' : './jsx/babel-polyfill.js'
    },
    output: {
        path: __dirname,
        filename: 'js/components/[name].js'
    },
    plugins: plugins,
    module: {
        loaders: [
            {
                test: /\.js|\.jsx$/,
                loader: "babel-loader",
                exclude: [/node_modules/],
                query: {
                    presets: ['es2015', 'react']
                }
            },
            {
                test: /\.json$/,
                loader: "json-loader"
            },
            {
                test: /\.css$/,
                loader: [ 'style-loader', 'css-loader' ]
            }
        ]
    }
}
