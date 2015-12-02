/**
 * Created by jeff on 15/12/2.
 */
var redis = require("redis");
var client = redis.createClient(6379,'127.0.0.1');


module .exports = redis;