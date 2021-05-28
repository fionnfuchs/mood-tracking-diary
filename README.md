# Mood Tracking Diary
A telegram bot that asks you about your day / mood and writes your answers into a database. In the future it will be able to generate diaries for you to read and analyze the data it collected in a meaningful way.

Warning: Currently diary entries and stats are not protected and anyone with access to the backend and your Telegram User ID can read them. By the time this project will be hosted somewhere they will only be accessible with a secret link the bot can generate for you then.

## Run bot and backend with Docker Compose
```
docker-compose build

docker-compose up
```

## Run Webview React app
```
cd webview

npm install

npm start
```
