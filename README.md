# JetSpider
---

a python distributed web spider and parser

## Dependencies

* python && pip
* redis
* ...

## Usage

for master node, you should start up your redis server on `<redis_server_ip:redis_server_port`

then, start up the master node using command:

```
python ./master-start.py 
```

for slave node, run command:

```
python ./slave-start --master=<master_ip:master_port> --type=<spider/parser> --name=<slave_name>
```

and the last, have fun~

