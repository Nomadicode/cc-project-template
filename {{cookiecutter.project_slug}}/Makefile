SHELL := /bin/bash

connect-server:
	docker-compose -f local.yml run --rm server bash

connect-client:
	docker-compose -f local.yml run --rm client bash

start-client:
	docker-compose -f local.yml up client

start-server:
	docker-compose -f local.yml up server

start: 
	docker-compose -f local.yml up

test-client:
	docker-compose -f local.yml run --rm client npm run test

test-server:
	docker-compose -f local.yml run --rm server python manage.py test

test: test-client test-server
