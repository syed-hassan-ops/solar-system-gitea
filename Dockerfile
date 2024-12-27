FROM node:23.5.0-slim

RUN mkdir -p /app

COPY . /app

WORKDIR /app

RUN npm install 
ENTRYPOINT [ "npm","run","start" ]
EXPOSE 3000