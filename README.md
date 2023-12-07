# Example of AWS Neptune test infrastructure

Graph databases, such as AWS Neptune and Neo4j, are crucial tools. During development, it's common to emulate a graph database in a local environment for testing and verification. However, building a test framework from scratch can be challenging. In this repository, we provide the source code for a simple API server, serving as an example of a test framework. It has been implemented using FastAPI, a Gremlin server, and pytest-docker.

## Set up the environment

```shell
$ poetry install
```

## Run the test

```shell
python -m pytest
```

## Notes

### When unable to execute tests

Please try the following commands.

```
$ chmod 777 tests/gremlin-console/
$ chmod 777 tests/gremlin-server/
```
