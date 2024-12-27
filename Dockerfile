FROM node:23.5.0-slim

RUN mkdir -p /app

COPY app-controller.js /app
COPY app-test.js /app
COPY app.js /app
COPY index.html /app
COPY package-lock.json /app
COPY package.json /app
COPY oas.json /app


WORKDIR /app

RUN npm install 
ENTRYPOINT [ "npm","run","start" ]
EXPOSE 3000