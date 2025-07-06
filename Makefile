.PHONY: all clean default install lock update check pc test integr docs run

default: check

install:
	pre-commit install
	uv sync
lock:
	uv lock
update:
	uv sync --upgrade

check: pc install lint test
pc:
	pre-commit run -a
lint:
	uv run ruff check .
	uv run ruff format .
	uv run mypy .
	uv run pyright .
test:
	uv run pytest -m 'not online'

# TODO: testcontainers
integr:
	docker compose -f docker-compose.firebird.yml up -d
	uv run pytest
	docker compose -f docker-compose.firebird.yml down

doc:
	uv run mkdocs serve

bumped:
	git cliff --bumped-version

# make release TAG=$(git cliff --bumped-version)-alpha.0
release: check
	git cliff -o CHANGELOG.md --tag $(TAG)
	pre-commit run --files CHANGELOG.md || pre-commit run --files CHANGELOG.md
	git add CHANGELOG.md
	git commit -m "chore(release): prepare for $(TAG)"
	git push
	git tag -a $(TAG) -m "chore(release): $(TAG)"
	git push origin $(TAG)
