#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

# Configuration
CONTAINER_NAME="flibusta-telegram-bot-db-1"  # MySQL Docker container name
DUMP_DIRECTORY="./dumps"  # Directory where SQL dump files are stored

# Check if the dump directory exists
if [ ! -d "$DUMP_DIRECTORY" ]; then
  echo "Directory $DUMP_DIRECTORY does not exist."
  exit 1
fi

# Loop through all .sql files in the directory
for sql_file in "$DUMP_DIRECTORY"/*.sql; do
  if [ -f "$sql_file" ]; then
    echo "Restoring $sql_file into $DB_NAME..."
    cat "$sql_file" | docker exec -i $CONTAINER_NAME mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE
    if [ $? -eq 0 ]; then
      echo "Successfully restored $sql_file."
    else
      echo "Error while restoring $sql_file."
    fi
  fi
done

echo "Database restoration completed."
