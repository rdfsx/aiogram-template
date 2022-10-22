.ONESHELL:

py := poetry --project=src/tgbot run
python := $(py) python

package_dir := src
tgbot_dir := src/tgbot

code_dir := $(tgbot_dir)


define setup_env
    $(eval ENV_FILE := $(1))
    @echo " - setup env $(ENV_FILE)"
    $(eval include $(1))
    $(eval export)
endef

.PHONY: reformat
reformat:
	$ black $(code_dir) --line-length 100 .
	$ isort $(code_dir) --profile black --filter-files

.PHONY: dev-docker
dev-docker:
	docker compose -f=./docker-compose.dev.yml --env-file=./.env.dev up

.PHONY: dev-bot
dev-bot:
	$(call setup_env, ./deployment/.env.dev)
	python -m app.tgbot --init_admin_db

.PHONY: prod
prod:
	docker compose -f=./docker-compose.prod.yml --env-file=./.env up