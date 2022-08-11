SHELL := /bin/bash
{% if cookiecutter.include_server == 'y' %}
connect-server:
	docker-compose run --rm server bash
{% endif %}
{% if cookiecutter.include_client == 'y' %}
connect-client:
	docker-compose run --rm client bash
{% endif %}
{% if cookiecutter.include_client == 'y' %}
start-client:
	docker-compose up client
{% endif %}
{% if cookiecutter.include_server == 'y' %}
start-server:
	docker-compose up server
{% endif %}
start: 
	docker-compose up
{% if cookiecutter.include_client == 'y' %}
test-client:
	docker-compose run --rm client npm run test
{% endif %}
{% if cookiecutter.include_server == 'y' %}
test-server:
	docker-compose run --rm server python manage.py test
{% endif %}
test: {% if cookiecutter.include_client == 'y' %}test-client{% endif %} {% if cookiecutter.include_server == 'y' %}test-server{% endif %}
