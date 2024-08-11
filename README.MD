# Flibusta Telegram Bot

Teleram bot created to help users download books from Flibusta. With this bot, users can search for books by title, author, or sequence and download them in various formats, including FB2, EPUB, MOBI, PDF, and more.

----------------------------
### Getting Started

**1. Clone the Repository**

```
git clone https://github.com/yourusername/flibusta-telegram-bot.git
cd flibusta-telegram-bot
```

**2. Set Up Environment Variables**

Create a .env file in the project root directory with the necessary environment variables. You can base it on the
.env.dist if provided.

**3. Build and Start the Services**

```
docker-compose up --build
```

**4. Run Alembic Migrations**

To create a new migration:
```
make alembic-revision
```

To apply the latest migration:
```
make alembic-upgrade
```


---------------------------
##### **Contributing**

Feel free to submit issues or pull requests if you want to contribute to this project.