const jwt = require("jsonwebtoken");

/**
 * Generar un token para la validación del usuario en el cliente.
 * INFO: https://jwt.io/
 * @param {String} userId Identificador del usuario
 * @param {String} userName Nombre del usuario
 * @returns El JWT en formato string
 */
const generateJwt = (userId, userName) => {
    const payload = { userId, userName };
    
    return new Promise((resolve, reject) => {
        jwt.sign(payload, process.env.JWT_SECRET, {
            expiresIn: '24h'
        }, (err, token => {
            if (err) {
                console.log("Algo falló en la generación del token");
                reject(err);
            } else {
                console.log("Nuevo token generado");
                resolve(token);
            }
        }));
    });
};

module.exports = {
    generateJwt
};