.PHONY: all clean default install lock update check pc test integr docs run

default: check

install:
	prek install
	uv sync
lock:
	uv lock
update:
	uv sync --upgrade
	prek auto-update

check: pc lint test
pc:
	prek run -a
lint:
	uv run ruff check .
	uv run ruff format .
	uv run ty check .
test:
	uv run pytest

unit:
	uv run pytest -m 'not integr'

doc:
	uv run mkdocs serve

bumped:
	git cliff --bumped-version

# make release TAG=$(git cliff --bumped-version)-alpha.0
release: check
	git cliff -o CHANGELOG.md --tag $(TAG)
	prek run --files CHANGELOG.md || prek run --files CHANGELOG.md
	git add CHANGELOG.md
	git commit -m "chore(release): prepare for $(TAG)"
	git push
	git tag -a $(TAG) -m "chore(release): $(TAG)"
	git push origin $(TAG)
