const { response } = require("express");
const bcrypt = require("bcryptjs");
const userContext = require("../models/user.model");
const jwt = require("../helpers/jwt");

// Coger los usuarios
const getUsers = (req, res = response) => {
    return res.json({
        ok: true,
        msg: "Crear usuario",
    });
};

// Crear un nuevo usuario
const createUser = async (req, res = response) => {
    try {
        const { userName } = req.body;

        const user = await userContext.findOne({ userName });
        if (user) {
            return res.status(400).json({
                ok: false,
                msg: "Ese nombre de usuario ya existe",
            });
        }

        const dbUser = new userContext(req.body);

        // TODO: Utilizar cuando tengamos el sistema de cuentas
        // const salt = await bcrypt.genSaltSync(10);
        // dbUser.password = await bcrypt.hashSync(password, salt);

        await dbUser.save();

        // TODO: Utilizar cuando tengamos el sistema de cuentas
        // const token = jwt.generateJwt(dbUser.id, userName);

        return res.status(200).json({
            ok: true,
            userId: dbUser.id,
            name: userName,
            msg: "Usuario creado correctamente"
        });
    }
    catch (error) {
        console.log(error);
        return res.status(500).json({
            ok: false,
            msg: "Algo no ha funcionado en la creación del usuario"
        });
    }
};

// Usuario eliminado
const removeUser = async (req, res = response) => {
    try {
        const { userName } = req.body;

        const dbUser = userContext.findOne({ userName });
        if (!dbUser) {
            return res.status(400).json({
                ok: false,
                msg: "Ese nombre de usuario no existe",
            });
        }
        userContext.deleteOne({ userName }).then(() => {
            console.log("User deleted");
        }).catch(error => {
            console.log(error);
        });

        return res.status(200).json({
            ok: true,
            userId: dbUser.id,
            name: userName,
            msg: "Usuario eliminado correctamente"
        });
    }
    catch (error) {
        console.log(error);
        return res.status(500).json({
            ok: false,
            msg: "Algo no ha funcionado en la eliminación del usuario"
        });
    }
}

// !TODO¡ - Aún no es necesario
// // Comprueba la existencia del usuario, valida los credenciales y devuelve el token de acceso
// const loginUser = (req, res = response) => {
//     return res.json({
//         ok: true,
//         msg: "Crear usuario",
//     });
// };

module.exports = {
    getUsers,
    createUser,
    removeUser
};