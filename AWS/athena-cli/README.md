Athena CLI
==========

Presto-like CLI for AWS Athena.

Installation
------------

Clone the GitHub repo and run:

    $ python setup.py install

Or, to install remotely from GitHub run:

    $ pip install git+https://github.com/satterly/tools.git#subdirectory=AWS/athena-cli

Configuration
-------------

Define a S3 results bucket and default AWS region.

```python
PLUGINS = ['influxdb']
```

**Default Configuration**

```python
INFLUXDB_DSN = 'influxdb://user:pass@localhost:8086/alerta'
INFLUXDB_MEASUREMENT = 'event'
```

**Examples**

Define a different DSN with valid username/password:

```python
INFLUXDB_DSN = 'influxdb://alerta:p8ssw0rd@localhost:8086/alerta'
```

Only override the database name:

```python
INFLUXDB_DATABASE = 'monitoring'
```

**Query Example**

Find diskUtil values for all "Web" services:

```SQL
$ influx -precision rfc3339
Connected to http://localhost:8086 version 1.2.2
InfluxDB shell version: 1.2.2
> use alerta
Using database alerta
> select * from event where service =~ /Frontend/;
name: event
time                     environment event    resource    service      severity value
----                     ----------- -----    --------    -------      -------- -----
2017-05-19T21:13:41.494Z Production  diskUtil host01:/tmp Web,Frontend major    98.01
2017-05-19T21:14:31.92Z  Production  diskUtil host02:/var Web,Frontend minor    79.54
```

Troubleshooting
---------------

Run in debug mode using `--debug` option.

References
----------

  * AWS Athena:
  * Presto:

License
-------

Copyright (c) 2017 Nick Satterly. Available under the MIT License.