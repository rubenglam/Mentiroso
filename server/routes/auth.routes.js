const { Router } = require("express");
const { check } = require("express-validator");
const { getUsers, createUser, removeUser } = require('../controllers/auth.controller');
const { validateFields } = require("../middlewares/validate-fields");

const router = Router();

// Auth controller
router.get("/users", getUsers);
router.post("/createUser", [
    check("userName", "El nombre de usuario es obligatorio").isLength({ min: 3 }),
    validateFields
], createUser);
router.delete("/removeUser", [
    check("userName", "El nombre de usuario es obligatorio").isLength({ min: 3 }),
    validateFields
], removeUser);

module.exports = router;