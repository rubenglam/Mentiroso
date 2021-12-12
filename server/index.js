const express = require("express");
const cors = require("cors");
const { dbConnection } = require("./db/config");
require("dotenv").config();

// Crear servidor/aplicación de express
const app = express();

// Connectar con la base de datos
dbConnection();

// Añadir el directorio de archivos estáticos
app.use(express.static("public"));

// Añadir el CORS
app.use(cors());

// JSON lector y conversor
app.use(express.json());

// Rutas
app.use("/api/auth", require("./routes/auth.routes"));

// Hostear la aplicación en el puerto pasado
app.listen(process.env.PORT, () => {
	console.log(`Servidor corriendo en puerto ${process.env.PORT}`);
});
