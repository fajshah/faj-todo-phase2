const express = require('express');
const {
  getAllTodos,
  getTodoById,
  createTodo,
  updateTodo,
  deleteTodo
} = require('../controllers/todoController');
const {
  validateTodoCreation,
  validateTodoUpdate
} = require('../middlewares/validation');

const router = express.Router();

router.get('/', getAllTodos);
router.get('/:id', getTodoById);
router.post('/', validateTodoCreation, createTodo);
router.put('/:id', validateTodoUpdate, updateTodo);
router.delete('/:id', deleteTodo);

module.exports = router;