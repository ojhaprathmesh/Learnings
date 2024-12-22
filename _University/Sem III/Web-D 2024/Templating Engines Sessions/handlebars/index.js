const express = require("express");
const path = require("path");
const hbs = require("hbs");
const app = express();

app.set("view engine", "hbs");
app.set("views", path.join(__dirname, "./views"));
hbs.registerPartials(path.join(__dirname, "./partials")); // Corrected this line

app.get("/", (req, res) => {
    res.render("home", { "username": "Amit" });
});

app.listen(3000, () => { 
    console.log("Server connected at http://localhost:3000");
});
