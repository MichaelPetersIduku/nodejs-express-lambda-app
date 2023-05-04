require("dotenv").config();
const express = require("express");
const serverless = require("serverless-http");
const mongoose = require("mongoose");
const { connection, Schema, model } = mongoose;
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use(async function(req, res, next) {
  await mongoose.connect(process.env.MONGODB_URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });
  res.on("finish", async function () {
    if (connection.readyState === 1) {
      await connection.close();
    }
  });

  next();
});

connection.on("error", (error) => {
  console.log(`MongoDB database connection error: ${error}`);
  throw error;
});

connection.once("open", async function () {
  console.log("MongoDB database connection opened successfully.");
});

const schema = new Schema({
  name: String,
  age: Number,
  email: String
});

const person = model('Person', schema);

app.get("/", (req, res) => {
  res
    .status(200)
    .send("My test express app on aws lambda. Lets see if it works");
});

app.get("/info", async (req, res) => {
  const someone = await person.create({name: "Gregory", age: 76, email: "gregory@beans.com"});

  res.status(200).json({
    info: "You want an info, this is it",
    isDBConnnected: connection.readyState,
    ...someone
  });
});

if (process.env.ENVIRONMENT === "lambda") {
  module.exports.handler = serverless(app);
} else {
  app.listen(3000, () => {
    console.log("Listening on port 3000");
  });
}
