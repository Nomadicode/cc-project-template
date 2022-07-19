FROM node:14-buster-slim

RUN apt-get -y update \
    && apt-get install -y git
RUN mkdir /app

ENV NODE_ENV=development

RUN npm install -g @vue/cli

WORKDIR /app
COPY package*.json ./

ADD ./client ./

RUN npm install -y

EXPOSE 8080

CMD ["npm", "run", "serve"]