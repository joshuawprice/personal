.PHONY: build
build:
	docker build -t kobeni .

.PHONY: run
run: build
	docker run --env-file=.env --network=host kobeni

.PHONY: dev
dev: build
	docker compose -f compose.dev.yml up

# A python dependency for the project (zeroc-ice) doesn't build on my host,
# only on debian 13. Therefore, create the venv in there so that I can
# continue developing properly on my host.
#
# See also: Dockerfile.venv and make-venv.sh
.PHONY: venv
venv:
	docker build -t kobeni-dev -f Dockerfile.venv .
	docker run --rm -v ./:/app kobeni-dev:latest
