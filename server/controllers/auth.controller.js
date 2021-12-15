const { response } = require("express");
const bcrypt = require("bcryptjs");
const userContext = require("../models/user.model");
const { generateJwt } = require("../helpers/jwt");

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
		// const token = generateJwt(dbUser.id, userName);

		return res.status(200).json({
			ok: true,
			userId: dbUser.id,
			name: userName,
			msg: "Usuario creado correctamente",
		});
	} catch (error) {
		console.log(error);
		return res.status(500).json({
			ok: false,
			msg: "Algo no ha funcionado en la creación del usuario",
		});
	}
};

// Usuario eliminado
const removeUser = async (req, res = response) => {
	try {
		const { userName } = req.body;

		const dbUser = await userContext.findOne({ userName });
		if (!dbUser) {
			return res.status(400).json({
				ok: false,
				msg: "Ese nombre de usuario no existe",
			});
		}
		userContext
			.deleteOne({ userName })
			.then(() => {
				console.log("User deleted");
			})
			.catch((error) => {
				console.log(error);
			});

		return res.json({
			ok: true,
			userId: dbUser.id,
			name: userName,
			msg: "Usuario eliminado correctamente",
		});
	} catch (error) {
		console.log(error);
		return res.status(500).json({
			ok: false,
			msg: "Hable con el administrador",
		});
	}
};

// Comprueba la existencia del usuario, valida los credenciales y devuelve el token de acceso
const loginUser = async (req, res = response) => {
	const { email, password } = req.body;

	try {
		const dbUser = await userContext.findOne({ email });
		if (!dbUser) {
			return res.status(400).json({
				ok: false,
				msg: "El correo no existe",
			});
		}

		const validPassword = bcrypt.compareSync(password, dbUser.password);
		if (!validPassword) {
			return res.status(400).json({
				ok: false,
				msg: "El password no es válido",
			});
		}

		const token = await generateJwt(dbUser.id, dbUser.name);

		return res.json({
			ok: true,
			uid: dbUser.id,
			name: dbUser.name,
			token: token,
		});
	} catch (error) {
		console.log(error);
		return res.status(500).json({
			ok: false,
			msg: "Hable con el administrador",
		});
	}
};

// Genera un nuevo token de acceso a partir del anterior
const refreshToken = async (req, res = response) => {
	const { id, userName } = req.user;

	const token = generateJwt(id, userName);

	return res.json({
		ok: true,
		id,
		name,
		token,
	});
};

module.exports = {
	getUsers,
	createUser,
	removeUser,
};
