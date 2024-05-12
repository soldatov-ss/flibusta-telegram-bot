# Restoring database. See more info dumps/README.MD
restore-db:
	scripts/restore_database.sh

# Get IP Address of the Database Container
db-host:
	@echo "Retrieving IP address of the Docker container..."
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' flibusta-telegram-bot-db-1
