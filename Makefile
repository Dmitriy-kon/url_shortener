.PHONY: help
help:
	@echo "Available commands:"
	@echo "  prod-start         - Start the production environment"
	@echo "  prod-stop          - Stop the production environment"
	@echo "  dev-start          - Start the development environment"
	@echo "  dev-stop           - Stop the development environment"
	@echo "  test-start         - Start the production test environment"
	@echo "  test-stop          - Stop the production test environment"
	@echo "  test-local-start   - Start the local test environment"
	@echo "  test-local-stop    - Stop the local test environment"

.PHONY: prod-start
prod-start:
	docker compose up

.PHONY: prod-stop
prod-stop:
	docker compose down

.PHONY: dev-start
dev-start:
	docker compose -f docker-compose-dev.yaml up

.PHONY: dev-stop
dev-stop:
	docker compose -f docker-compose-dev.yaml down

.PHONY: test-start
test-start:
	docker compose -f docker-compose-prod-test.yaml up

.PHONY: test-stop
test-stop:
	docker compose -f docker-compose-prod-test.yaml down

.PHONY: test-local-start
test-local-start:
	docker compose -f docker-compose-local-test.yaml up

.PHONY: test-local-stop
test-local-stop:
	docker compose -f docker-compose-local-test.yaml down
