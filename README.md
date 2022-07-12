# Nomadicode Project Template

This repo represents the standard project template for Nomadicode projects. It is designed to be easy to extend, and enables the use of a client only, or a server only project.


## Server

The server is set up with Django and provides

* REST or GraphQL API
* Internationalization (i18n)

## Client
The server is build on the vue framework and provides:

* Internationalization
* Easy connection to the server


## Setup

1. Create project with step by step configuration
2. cd into the new directory
3. docker-compose -f local.py up

All CI/CD data is configure out of the box, you just need to handle the initial configuration for deploying

## CI/CD setup
1. Log into the provider and set up a server
2. set up docker on the server
3. pull the repo into the new server
4. run docker-compose -f production.yml up -d
5. Ready!