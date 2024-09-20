install:
	poetry install

run:
	cp -f ./deploy/compose/local/docker-compose.yml docker-compose.yml && \
		cp -n .env.example .env && \
		docker-compose up -d --build --remove-orphans

run-mac:
	cp -f ./deploy/compose/local/docker-compose.yml docker-compose.yml && \
	cp -f .env.example .env && \
	docker-compose up -d --build --remove-orphans

stop:
	docker-compose down

migration:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . \
		run --rm fastapi_test alembic revision --autogenerate && \
		sudo chown -R $(USER):$(USER) ./src/alembic

migration-apply:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . \
		run --rm fastapi_test alembic upgrade head


migration-downgrade:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . \
		run --rm fastapi_test alembic downgrade -1

logs:
	docker-compose logs -f