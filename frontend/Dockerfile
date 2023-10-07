FROM node:18-alpine as build

WORKDIR /app

COPY package.json ./
RUN npm install
RUN npm install -g @angular/cli

COPY . ./
RUN npm run build

EXPOSE 4200

