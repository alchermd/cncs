FROM node:current-slim

COPY yarn.lock /yarn.lock
COPY package.json /package.json

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
RUN yarn

WORKDIR /usr/src/web
COPY . /web

EXPOSE 3000
EXPOSE 35729

ENTRYPOINT ["/bin/bash", "/web/run.sh"]
CMD ["start"]