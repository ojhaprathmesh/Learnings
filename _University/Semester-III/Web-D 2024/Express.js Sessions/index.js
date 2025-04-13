const express = require("express");
let app = express();
const path = require("path");

app.use(express.static(path.join(__dirname, "/public")));

app.get("/", (req, res) => {
    res.sendFile("bml.html", { root: __dirname });
});

app.get("/sol", (req, res) => {
    res.sendFile("sol.html", { root: __dirname });
});

app.get("/soet", (req, res) => {
    res.sendFile("soet.html", { root: __dirname });
});

app.listen("3000", () => {
    console.log("Connected!!!");
    console.log(__dirname);
    console.log(path.join(__dirname, "/public"))
})