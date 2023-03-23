# build stage
FROM node:14-buster-slim as build-stage

ENV NODE_ENV=development
RUN mkdir /app
WORKDIR /app

RUN npm install -g @vue/cli
COPY ./client/package*.json /app/

RUN npm install

COPY ./client /app/

RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
ENV NODE_ENV=production
COPY ./ops/client/prod/nginx.conf /etc/nginx/nginx.conf
RUN rm -rf /usr/share/nginx/html/*

COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
