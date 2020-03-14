DJANGO_CONTAINER_NAME = web

attach:
	docker exec -it ${DJANGO_CONTAINER_NAME} bash

shell:
	docker exec -it ${DJANGO_CONTAINER_NAME} python manage.py shell
