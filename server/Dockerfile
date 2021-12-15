# https://www.digitalocean.com/community/tutorials/como-crear-una-aplicacion-node-js-con-docker-es

FROM node:10-alpine

RUN mkdir -p C:\Users\ruben\Documents\Git\Ruben\Mentiroso\server && chown -R node:node /home/node/app

WORKDIR /home/node/app

COPY package*.json ./

USER node

RUN npm install

COPY --chown=node:node alpine /home/node/app/

EXPOSE 8080

CMD [ "node", "app.js" ]