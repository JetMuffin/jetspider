/**
 * Created by jeff on 15/12/1.
 */
import 'babel/polyfill';
import express from 'express'
import path from 'path'

let config = require('./config/config')
let app = express()

app.set('port', config.port)
app.use(express.static(path.join(_dirname)))
app.listen(app.get('port'), () => {
    if (process.send){
        process.send('online');
    } else {
        console.log('The server is running at http://localhost:' + app.get('port'))
    }
})

require('./routes/default')(app)

if (process.env.NODE_ENV == 'development'){
    let jsonServer = require('json-server')
    let fs = require('fs')

    let server = jsonServer.create()

    server.use(jsonServer.defaults())

    const stubFile = './src/stub.json'
    let router = jsonServer.router(stubFile)
    server.use(router)

    server.listen(8000)
}