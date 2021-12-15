const express = require("express");
const http = require("http");
const socketio = require("socket.io");
const cors = require("cors");
const { dbConnection } = require("./db/config");
require("dotenv").config();

// Crear servidor/aplicación de express y la libreria de websockets
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

const server = http.Server(app);
const io = socketio(server);

io.on("connection", (sock) => {
	console.log("Connected");
});

server.on("error", (error) => {
	console.error(error);
});
// Hostear la aplicación
server.listen(process.env.PORT, () => {
	console.log(`Servidor corriendo en puerto ${process.env.PORT}`);
});
