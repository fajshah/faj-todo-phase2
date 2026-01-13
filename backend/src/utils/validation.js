const Joi = require('joi');

const validateTodo = (data) => {
  const schema = Joi.object({
    title: Joi.string().trim().min(1).max(200).required(),
    description: Joi.string().trim().max(1000).optional(),
    completed: Joi.boolean().optional(),
  });

  return schema.validate(data);
};

const validateUserRegistration = (data) => {
  const schema = Joi.object({
    username: Joi.string().alphanum().min(3).max(30).required(),
    email: Joi.string().email().required(),
    password: Joi.string().min(6).max(100).required(),
  });

  return schema.validate(data);
};

const validateUserLogin = (data) => {
  const schema = Joi.object({
    email: Joi.string().email().required(),
    password: Joi.string().min(6).max(100).required(),
  });

  return schema.validate(data);
};

module.exports = {
  validateTodo,
  validateUserRegistration,
  validateUserLogin,
};