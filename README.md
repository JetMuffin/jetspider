# JetSpider

## A Distributed Web Crawler and Parser

* Start from the url and fetch web pages with allowed domain
* Save the pages' information to database
* Increase slave node easily
* Support logging

## Dependencies

* python && pip (all nodes)
* redis (data-node or master-node if you work on standalone mode)
* mongodb (data-node or master-node if you work on standalone mode)

**Notice:**
if you are running with source code, you should install python modules `BeautifulSoup4`,`psutil`,`rpyc`,`lxml`,`redis`,`pymongo` using command:

```
$: sudo pip install <module_name>
```

## Usage

for the master node, start up the master node using command:

```
$: python ./master-start.py 
```

for the data node, start up redis server and mongo database:

```
$: <path_to_redis>/src/redis-server

$: <path_to_mongo>/bin/mongd
```

for slave node, run command:

```
python ./slave-start --master=<master_ip:master_port> --type=<spider/parser> --name=<slave_name>
```

more detail command help:

```
Usage: slave-start.py [options]

Options:
  -h, --help            show this help message and exit
  -m MASTER, --master=MASTER
                        address of your cluster's master
  -n NAME, --name=NAME  give a name to your slave
  -t TYPE, --type=TYPE  slave type: spider or parser
```

Some parts of modules are **under development**, so I wish you could have fun with this codes!

## Contact

[564936642@qq.com](mailto:564936642@qq.com) or [jeffchen328@gmail.com](mailto:jeffchen328@gmail.com)

