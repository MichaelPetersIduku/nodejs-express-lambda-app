const express = require("express");
const serverless = require("serverless-http");
// const mongoose = require("mongoose");

// const { connection } = mongoose;
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

console.log("MONGODB_URL", process.env.MONGODB_URL);
mongoose.connect(process.env.MONGODB_URL, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  // useCreateIndex: true,
  // useFindAndModify: false,
  // autoIndex: true,
});

connection.on("error", (error) => {
  console.log(`MongoDB database connection error: ${error}`);
  throw error;
});

connection.once("open", async function () {
  console.log("MongoDB database connection opened successfully.");
});

app.get("/", (req, res) => {
  res
    .status(200)
    .send("My test express app on aws lambda. Lets see if it works");
});

app.get("/info", (req, res) => {
  res.status(200).json({
    info: "You want an info, this is it",
  });
});

if (process.env.ENVIRONMENT === "lambda") {
  module.exports.handler = serverless(app);
} else {
  app.listen(3000, () => {
    console.log("Listening on port 3000");
  });
}
