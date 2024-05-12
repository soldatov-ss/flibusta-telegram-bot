# Database Restoration

This directory contains SQL dump files used for restoring the database of the Flibusta Telegram Bot project. These dumps are crucial for setting up the database in a new environment or recovering data.

## Directory Structure

- Each `.sql` file in this folder is a dump from a specific table of the database.
- `README.MD`: This file, containing instructions and guidelines on how to use the dump files.

## Prerequisites

- Docker must be installed and running on your machine.
- The MySQL Docker container should be running and accessible.
- MySQL client must be installed on the host if running scripts outside the container.

## Environment Setup

Before running the restore scripts, ensure the `.env` file is correctly configured with the necessary database credentials and Docker container details. Example:
```
MYSQL_DATABASE=database 
MYSQL_USER=mysql    
MYSQL_PASSWORD=password     
```


## Restoring the Database

1. **Navigate to the Project Root**:
   Ensure you are in the root directory of the project where the `Makefile` and `scripts` directory are located.

2. **Run the Restoration Script**:
   Execute the database restoration process by running:

```
make restore-db
```


This command triggers a script that loops through all `.sql` files in this `dumps` folder and applies them to the configured database within the specified Docker container.
