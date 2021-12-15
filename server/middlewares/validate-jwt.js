const { response } = require("express");
const jwt = require("jsonwebtoken");

const validateJwt = (req, res = response, next) => {
    const token = req.header("auth-token");
	if (!token) {
		return res.status(401).json({
			ok: false,
			msg: "Error en el token"
		});
	}

    try {
        const { userId, userName } = jwt.verify(token, process.env.JWT_SECRET);
        req.user = {
            id: userId,
            userName: userName
        };
    }
    catch (error) {
        return res.status(401).json({
            ok: false,
            msg: "Token no válido"
        });
    }

    next();
}

module.exports = {
    validateJwt
};