===========================
mongo-connector-transaction
===========================

The mongo-connector-transaction project originated as a project that is based
on already exists `mongo-connector <https://github.com/yougov/mongo-connector>`__.

This repository and the `library <https://pypi.org/project/mongo-connector-transaction/>`__ it
provides are just for supporting mongo-connector to be able to work with
transactions process as when it was built it doesn't consider the different
oplog structure for the transaction oplog documents.

**Currently it only supports integration with elastic2-doc-manager**

For complete documentation, check out the `Mongo Connector Wiki
<https://github.com/AmrAdelKhalil/mongo-connector/wiki>`__.

`Note`: Pardon me if the documents could be a little missy but the library
supports everything that mongo-connector used to support but you shall add
**-transaction** part only.


System Overview
---------------

`mongo-connector-transaction` creates a pipeline from a MongoDB cluster to one or more
target systems, such as Solr, Elasticsearch, or another MongoDB cluster.  It
synchronizes data in MongoDB to the target then tails the MongoDB oplog, keeping
up with operations in MongoDB in real-time. Detailed documentation is
available on the `wiki
<https://github.com/AmrAdelKhalil/mongo-connector/wiki>`__.

Getting Started
---------------

mongo-connector-transaction supports Python 3.4+ and MongoDB versions
3.4 and 3.6.

Installation
~~~~~~~~~~~~

To install mongo-connector-transaction with the MongoDB doc manager suitable for
replicating data to MongoDB, use `pip <https://pypi.python.org/pypi/pip>`__::

  pip install mongo-connector-transaction


The install command can be customized to include the `Doc Managers`_
and any extra dependencies for the target system.

+----------------------------------+-------------------------------------------------------------+
|         Target System            |            Install Command                                  |
+==================================+=============================================================+
| MongoDB                          | ``pip install mongo-connector-transaction``                 |
+----------------------------------+-------------------------------------------------------------+
| Elasticsearch 5.x                | ``pip install 'mongo-connector-transaction[elastic5]'``     |
+----------------------------------+-------------------------------------------------------------+

You may have to run ``pip`` with ``sudo``, depending
on where you're installing mongo-connector and what privileges you have.

System V Service
~~~~~~~~~~~~~~~~

Mongo Connector provides support for installing and uninstalling itself as
a service daemon under System V Init on Linux. Following install of the
package, install or uninstall using the following command:

    $ python -m mongo_connector.service.system-v [un]install

Development
~~~~~~~~~~~

You can also install the development version of mongo-connector
manually::

  git clone https://github.com/AmrAdelKhalil/mongo-connector
  pip install ./mongo-connector

Using mongo-connector
~~~~~~~~~~~~~~~~~~~~~

mongo-connector replicates operations from the MongoDB oplog, so a
`replica
set <http://docs.mongodb.org/manual/tutorial/deploy-replica-set/>`__
must be running before startup. For development purposes, you may find
it convenient to run a one-node replica set (note that this is **not**
recommended for production)::

  mongod --replSet myDevReplSet

To initialize your server as a replica set, run the following command in
the mongo shell::

  rs.initiate()

Once the replica set is running, you may start mongo-connector. The
simplest invocation resembles the following::

  mongo-connector-transaction -m <mongodb server hostname>:<replica set port> \
                  -t <replication endpoint URL, e.g. http://localhost:8983/solr> \
                  -d <name of doc manager, e.g., solr_doc_manager>

mongo-connector has many other options besides those demonstrated above.
To get a full listing with descriptions, try ``mongo-connector-transaction --help``.
You can also use mongo-connector with a `configuration file <https://github.com/AmrAdelKhalil/mongo-connector/wiki/Configuration-Options>`__.

If you want to jump-start into using mongo-connector with a another particular system, check out:

- `Usage with Elasticsearch <https://github.com/AmrAdelKhalil/mongo-connector/wiki/Usage%20with%20ElasticSearch>`__
- `Usage with MongoDB <https://github.com/AmrAdelKhalil/mongo-connector/wiki/Usage-with-MongoDB>`__

Doc Managers
~~~~~~~~~~~~

Elasticsearch 2.x and 5.x: https://github.com/AmrAdelKhalil/elastic2-doc-manager

The MongoDB doc manager comes packaged with the mongo-connector project.
