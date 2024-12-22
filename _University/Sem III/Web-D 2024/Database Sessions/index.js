const express = require("express");
const app = express();

const { dbconnect } = require("./dbconnect/dbcon.js");
const { saveDoc, getData, updateData, deleteData } = require("./model/model.js");


app.listen("3200", () => {
    console.log("Successfully Connected!")
    console.log("Served at http://localhost:3200");
});

dbconnect();

// saveDoc();

getData();

updateData(1);

deleteData(1);