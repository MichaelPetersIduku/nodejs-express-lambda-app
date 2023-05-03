const express = require("express");
const awsServerlessExpressMiddleware = require("aws-serverless-express/middleware");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();

app.use(awsServerlessExpressMiddleware.eventContext());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use(cors());
app.use(bodyParser.json({ strict: false }));

app.get("/", (req, res) => {
  res
    .status(200)
    .send("My test express app on aws lambda. Lets see if it works");
});

app.get("/info", (req, res) => {
  res
    .status(200)
    .json({
      info: "You want an info, this is it",
      event: req.apiGateway.event,
    });
});

app.listen(3000, () => {
  console.log("Listening on port 3000");
});
