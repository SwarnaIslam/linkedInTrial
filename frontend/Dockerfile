FROM node:18-alpine as build

WORKDIR /app

COPY package.json ./
RUN npm i -g npm@9.6.7
RUN npm install -g @angular/cli

COPY . ./
RUN npm run build -- --configuration=production --output-path=dist/front-end

EXPOSE 4200

