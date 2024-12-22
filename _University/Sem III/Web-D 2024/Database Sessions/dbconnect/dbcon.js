const mongoose = require("mongoose");

const constring = "mongodb+srv://arpitabansal321:Jk1premSVmKr6mqC@firstsmile.amnra.mongodb.net/";

const dbconnect = async () => {
    try {
        await mongoose.connect(constring, {});
        console.log("Connected to database successfully!");
    } catch (err) {
        console.log(`Error: ${err}`);
    }
}

module.exports = { dbconnect };