# Mood Tracking Diary
A telegram bot that asks you about your day / mood and writes your answers into a database. It is able to generate diaries for you to read and analyze the data, providing insight into what raises / lowers your mood. 

## Prerequisits
You need the following software:
- Docker Compose
- Node.js and Python 3 (when developing locally without Docker)

Then perform the following steps:
- In `telegrambot/config.py` add the Telegram Bot token

## Run bot and backend with Docker Compose

1. Build the webview react app

    ```
    cd webview
    npm run build
    ```
2. Build all other components and start containers
    ```
    ./br.sh
    ```
    or
    ```
    cp -R webview/build/* backend/public/
    docker-compose build
    docker-compose up
    ```

## Run webview react app only with mock data
1. Set `mock=true` in app.js to enable the use of mock data without backend
2. Start development server
    ```
    cd webview
    npm install
    npm start
    ```
