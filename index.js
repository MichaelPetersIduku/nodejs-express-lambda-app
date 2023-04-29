const express = require('express');
const app = express();

app.use(express.json());
app.use(express.urlencoded({extended: false}));

app.get("/", (req, res) => {
    res.status(200).send("My test express app on aws lambda");
})

app.listen(3000, () => {
    console.log("Listening on port 3000");
})