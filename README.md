# MS authorization

## Run locally

### Run with Docker Compose

> :warning: **Linux Users**: Running docker-compose may require using sudo command if current user is not in the docker group

> :warning: **Windows Users**: Check that your `git config core.autocrlf` is `false` or set it to `false` before starting, otherwise build/run may fail

```shell script
	make run
```

or

```shell script
	cp .env.example .env
	cp ./deploy/compose/local/docker-compose.yml docker-compose.yml
	docker-compose up -d
```

### Useful Tips

- use http://localhost/api/docs to access web Swagger
- use http://rabbitmq.localhost to access rabbitmq dashboard (see credentials in .env or .env.example)
- use `make logs` to see logs
