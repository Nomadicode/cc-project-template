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
1. Log into Digital Ocean
2. set up new app from DO registry
3. Assign a static IP
4. point a URL
5. Ready!
