const express = require('express');
const { uniqueNamesGenerator, starWars } = require('unique-names-generator'); const app = express();// Get maximum character from ENVs else return 5 character
const MAX_STAR_WARS_CHARACTERS = process.env.MAX_STAR_WARS_CHARACTERS || 5; const config = {
  dictionaries: [starWars]
}// Get the character name array


const client = require('prom-client');
const collectDefaultMetrics = client.collectDefaultMetrics;
const prefix = 'my_application_';
collectDefaultMetrics({ prefix });


const getStarWarsCharacters = () => {
  const characterNames = []; for (let i = 1; i <= MAX_STAR_WARS_CHARACTERS; i += 1) {
    characterNames.push(uniqueNamesGenerator(config));
  }
  return characterNames;
}; 


const counter = new client.Counter({
  name: 'count',
  help: 'help me count'
});


const histogram = new client.Histogram({
  name: 'histogram',
  help: 'help me histo'
});

app.get('/', (req, res) => {
  console.log('Character requested!!');
  counter.inc();
  res.json(getStarWarsCharacters());
}); 


app.get('/another', (req, res) => {
  console.log('Character requested!!');
  counter.inc();
  res.json("something else");
}); 

app.get('/metrics', (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.send(client.register.metrics());
})

app.listen(3000, () => {
  console.log('Server started on port 3000');
  console.log('client up and runnning');
});
