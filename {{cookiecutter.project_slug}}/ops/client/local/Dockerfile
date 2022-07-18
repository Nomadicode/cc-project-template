FROM node:carbon-slim

RUN apt-get -y update \
    && apt-get install -y git

RUN npm install -g @vue/cli yarn

WORKDIR /app

ADD ./client /app/

RUN yarn install
EXPOSE 8080

USER node

CMD ["yarn", "serve"]