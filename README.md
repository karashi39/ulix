# README

load mermaidjs flowchart to neo4j and dump

## usage

### setup

requirement

- python
- uv


install

```
make install
```

run

```
make run
```

### commands

load

```sh
cat sample.mermaid | make cmd
```

dump

```sh
make cmd ARG=dump
```

delete all

```sh
make cmd ARG=delete-all
```
