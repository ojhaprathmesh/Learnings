const express = require("express");
const path = require("path");
const app = express();

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "./templates/views"));

app.get("/", () => {
    app.render("home", { "username": "Amit" });
});

app.listen(3000, () => { 
    console.log("Server connected at http://localhost:3000")
});