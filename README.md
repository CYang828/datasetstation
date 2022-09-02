<p align="center">
  <img width="320" src="/assets/logo/logo.png">
</p>

<p align="center">
    <a href="https://github.com/tornadoweb/tornado">
        <img src="https://img.shields.io/badge/tornado-5.0.2-brightgreen.svg" alt="tornado">
    </a>
    <a href="https://github.com/celery/celery">
        <img src="https://img.shields.io/badge/celery-4.2.0-brightgreen.svg" alt="celery">
    </a>
    <a href="https://github.com/apache/thrift">
        <img src="https://img.shields.io/badge/thrifit-0.11.0-brightgreen.svg" alt="thrift">
    </a>
    <a href="https://github.com/BSlience/fastweb">
        <img src="https://travis-ci.org/BSlience/fastweb.svg?branch=master" alt="fastweb">
    </a>
    <a href="LICENSE">
        <img src="https://img.shields.io/badge/Apache%202-license-blue.svg" alt="license">
    </a>

</p>

English | [简体中文](./README.zh-CN.md)

## Introduction

[fastweb](https://github.com/BSlience/fastweb) is a web-server integration solution. It based on [tornado](https://github.com/tornadoweb/tornado), [celery](https://github.com/celery/celery), [thrift](https://github.com/apache/thrift).

- [Documentation]()

- [Examples](examples/)

It is a charming web-server framework based on the effective technique and organized into component. The components could be used with only several config and code. It is always so easy to make a new component.It also provides many scenes to construct your apis, pages, rpc functions, tasks and so on efficiently.

## Features

<p align="center">
  <img width="600" src="/assets/features/features.png">
</p>

```
    - Configuration
        - ini

    - Web
        - api
        - page render

    - Task
        - distributed task
        - periodic task
        - touting task

    - Rpc
        - thrift

    - Component
        - mysql
        - redis
        - mongo
        - http
        - soap

    - Manager
        - pool
```

## Getting Started

```bash
pip install fastweb
```

## Examples

Many useful examples are [here](examples/).

## Changelog

Detail changes for each releases are documented in the [release notes](CHANGELOG.md).

## License

[Apache License](LICENSE.md)

Copyright on (c) 2018-present bslience
