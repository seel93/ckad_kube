FROM node:lts-alpine
WORKDIR /app
COPY package*.json ./
RUN npm i
COPY index.js index.js
CMD ["npm", "start"]
