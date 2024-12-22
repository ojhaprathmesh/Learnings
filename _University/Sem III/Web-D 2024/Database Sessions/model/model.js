const mongoose = require("mongoose");

const schema = new mongoose.Schema(
    {
        roll: { type: String, required: true },
        name: { type: String, required: true },
        marks: Number,
        repeatStatus: Boolean,
        date_adm: { type: Date, default: Date.now }
    }
);

const Student = mongoose.model("Student", schema);

// creating data
const saveDoc = async () => {
    s1 = new Student({ roll: "1", name: "Arpita Bansal", marks: 87, repeatStatus: true });
    s2 = new Student({ roll: "2", name: "Parul Gupta", marks: 67, repeatStatus: true });
    s3 = new Student({ roll: "3", name: "Parul Aggarwal", marks: 76, repeatStatus: true });

    try {
        await Student.insertMany([s1, s2, s3]);
        console.log("Data insertion successfull");
    } catch (error) {
        console.error("Error inserting data: ", error);
    }
};


// fetching data
let getData = async () => {
    let res = await Student.find({name: "Arpita Bansal"})
    // let res = await Student.find({roll:"3"})
    // let res = await Student.find({roll:"3"}).select({roll:1})
    // let res = await Student.find({roll:"3"}).select({_id:0,roll:1})
    // let res = await Student.find({roll:"5"}).select({_id:0,roll:0})
    // let res = await Student.find({marks:"67"}).select({_id:0,marks:1})
    // let res = await Student.find({marks:"67"}).select({marks:1,_id:0}).limit(1)
    // let res = await Student.find({marks:"35"}).select({marks:3}).count()
    // let res = await Student.find().select({_id:0, roll:1}).sort({"roll":1})

    //    sort({"roll":-1} -> Data will be sorted by roll in descending order
    // changing -1 to 1 will arrange in ascending order


    console.log("data:" + res)
}

// updating data in DB
let updateData = async (roll) => {
    let res = await Student.updateMany(
        { roll },
        { $set: { "marks": 222 } }
    )
}

// delete data
let deleteData = async (roll) => {
    let res = await Student.deleteMany({ roll })
    console.log(res)
}

module.exports = { saveDoc, getData, updateData, deleteData };
