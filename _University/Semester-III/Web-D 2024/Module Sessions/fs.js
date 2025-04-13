const fs = require("fs");

try {
    // Create the 'Test' directory synchronously if it doesn't exist
    fs.mkdirSync("Test");
} catch (or) {
    console.log("or making directory!");
}

// Write to the file synchronously
fs.writeFileSync("Test/abc.txt", "Hello!\n"); // Use '\n' for newlines

// Append to the file asynchronously (callback works)
fs.appendFile("Test/abc.txt", "We are learning FileSystem.\n", (err) => {
    if (err) {
        console.log("Error writing file!!");
    } else {
        console.log("Written successfully!!");
    }
});

// Append to the file synchronously (callback doesn't works)
fs.appendFileSync("Test/abc.txt", "We are also going to learn Path and OS Module.\n", (err) => {
    if (err) {
        console.log("Error writing file!!!!");
    } else {
        console.log("Written successfully!!!!");
    }
});
