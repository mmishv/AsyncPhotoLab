FROM node:18-alpine as build

WORKDIR /app

ADD *.json ./

RUN npm install

ADD ./public ./public
ADD ./src ./src
