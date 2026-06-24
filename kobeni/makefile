.PHONY: build
build:
	docker build -t kobeni .

.PHONY: arm
arm:
	docker build -t kobeni:arm64 --platform=arm64 .

.PHONY: deploy
deploy: arm
	docker save kobeni:arm64 \
		| zstd -19 \
		| pv \
		| ssh asgard "zstd -cd | docker load && docker compose up -d"

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
# Ice has been upgraded to fix this at the time of writing, but may break again
# in future, so keep this around.
.PHONY: venv
venv:
	docker build -t kobeni-dev -f Dockerfile.venv .
	docker run --rm -v ./:/app kobeni-dev:latest
