# Restoring database. See more info dumps/README.MD
restore-db:
	scripts/restore_database.sh

# Get IP Address of the Database Container
db-host:
	@echo "Retrieving IP address of the Docker container..."
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' flibusta-telegram-bot-db-1

alembic-revision:
	read -p "Enter name of migration: " $message
	docker-compose exec bot alembic revision --autogenerate -m "$message"

alembic-upgrade:
	docker-compose exec bot alembic upgrade head

clean-db:
	docker-compose down -v
	sudo rm -rf ./data/
	docker volume prune