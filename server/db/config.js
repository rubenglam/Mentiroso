const mongoose = require("mongoose");

const dbConnection = async() => {
    try {
        mongoose.connect(process.env.CONNECTION_STRING, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
            // useCreateIndex: true
        });
        console.log("Db connected successfully");
    }
    catch(exception) {
        console.log(exception);
        throw new Error("Error al conectar a la base de datos");
    }
};

module.exports = {
    dbConnection
};