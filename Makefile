include Makefile.deploy


# checks targets
check-lint:
	@echo "======================================="
	@flake8 && echo "flake8: SUCCESS" || (echo "flake8: FAILURE"; exit 1)

check-type:
	@echo "======================================="
	@mypy . --ignore-missing-imports && echo "mypy: SUCCESS" || (echo "mypy: FAILURE"; exit 1)

check-test:
	@echo "======================================="
	@pytest --cov -v && echo "pytest: SUCCESS" || (echo "pytest: FAILURE"; exit 1)

# docker-compose targets
docker-compose-build:
	docker-compose build

docker-compose-down:
	docker-compose down --remove-orphans

docker-compose-up:
	docker-compose up -d --remove-orphans

docker-compose-restart:
	docker-compose restart

docker-compose-logs:
	docker-compose logs -f

docker-compose-ps:
	docker-compose ps

# utils target
clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.cache' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +
	find . -name '.mypy_cache' -exec rm -fr {} +

# aliases
check: check-lint check-type check-test
checks: check

up: docker-compose-up
down: docker-compose-down
build: docker-compose-build
restart: docker-compose-restart
status: docker-compose-ps
logs: docker-compose-logs
