# Project: tdb_io


## Grafana

`docker run -d -p 3000:3000  grafana/grafana`
What is the password? admin admin - change from webinterface now


Datasources:


http://x.x.x.x:8086
no change anything
database user
pass
save

# Appendix:

## Setup influxdb

Install
```
apt install influxdb
apt install influxdb-client
```
`emacs /etc/influxdb/influxdb.conf` and  `auth-enabled = false`
`systemctl restart influxdb`


`CREATE USER admin WITH PASSWORD 'asd' WITH ALL PRIVILEGES`


Create databases
```
influx
> show databases
> create database test
> create database data
> show databases
name: databases
name
----
_internal
test
data
```

Create user
```
influx
> create user xxx with password 'xxxxxx'
> show users
user admin
---- -----
xxx  false
```


GRANT USER
```
> grant all on  test to  xxx
> grant all on  data to xxx
> quit
```

` auth-enabled = false` to
`true`


RESTART with auth
`emacs /etc/influxdb/influxdb.conf` and  `auth-enabled = true`

`systemctl restart influxdb`
influx
auth
## Module: mongo
