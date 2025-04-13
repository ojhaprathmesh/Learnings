const fs = require("fs");
const os = require("os");

// Ensure directories exist, avoid errors if they already exist
try {
    fs.mkdirSync("abc");
    fs.mkdirSync("xyz");
} catch (err) {
    console.log("Directories already exist!");
}

const xyzPath = "xyz/xyz.txt";

fs.writeFile(xyzPath, "1) Hello (first line contains 'hello')\n", (err) => {
    if (err) {
        console.log("Error writing file: ", err);
    } else {
        fs.appendFileSync(xyzPath, "2) Today we learnt different modules of Node.js: fs, os and path\n");
        fs.appendFileSync(xyzPath, `3) ${os.platform()}\n`);
        fs.appendFileSync(xyzPath, `4) ${os.arch()}\n`);
    }
});

fs.writeFile("abc/abc.txt", "Hi! I am abc.txt.\nNice to meet you all", (err) => {
    if (err) {
        console.log("Error writing file: ", err);
    } else {
        // Read data after writing it, else it will read before writing
        const data = fs.readFileSync("abc/abc.txt", "utf-8")
        console.log(data);
    }
});