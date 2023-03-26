inspect-db-host:
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' database

remove-volumes:
	docker-compose down --volumes

docker-prune:
	docker image prune && docker volume prune && docker container prune


# Example: make migration_name=add_new_table alembic-migrate
# Perhaps you need run the next command: pip install pymysql cryptography
alembic-migrate:
ifdef migration_name
	@echo '$(migration_name) is defined'
	MYSQL_URL=mysql+pymysql://mysql:password@localhost:3306/database alembic revision --autogenerate -m "$(migration_name)"
else
	@echo "The migration hasn't been created. Please write the migration_name correctly."
	@echo "Check MakeFile to see the example."
endif
