const express = require("express");
const cors = require ("cors")
const { MongoClient } = require('mongodb');

const app = express();
app.use(express.json());
app.use(cors())

// or as an es module:
// import { MongoClient } from 'mongodb'

// Connection URL
const url = 'mongodb://127.0.0.1:27017';
const client = new MongoClient(url);

// Database Name
const dbName = 'motor-db';

async function getData(palabra) {
  // Use connect method to connect to the server
  await client.connect();
  console.log('Connected successfully to server');
  const db = client.db(dbName);
  const collection = db.collection('motor');
  // the following code examples can be pasted here...
  var cursor = await collection.find({ $or: [ { palabra1: palabra }, { palabra2: palabra }, {palabra3: palabra} ] } ).sort( { "ranking1": -1, "ranking2": -1 , "ranking3": -1}).toArray()
  await client.close();
  return cursor;
}

async function searchWord(req, res){
    const params = req.query;
    const palabra = params.palabra;
    try{
        const data = await getData(palabra);
        if(!data){
            res.status(400).send('Error al obtener datos')
        }
        else{
            res.status(200).send(data);
        }
    }catch(error){
        res.status(500).send(error);
    }
}

PORT = 3000; 

app.get("/", function(req, res) {
    res.send("Success")
});

app.get("/api/get-documents", searchWord);


app.listen(PORT, function() {
    console.log(`Server started on port ${PORT}`);
});