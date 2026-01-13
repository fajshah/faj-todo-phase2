const express = require('express');
const router = express.Router();
const { auth } = require('../middleware/auth');
const {
  getAllTodos,
  getTodoById,
  createTodo,
  updateTodo,
  deleteTodo,
  toggleTodo,
} = require('../controllers/todoController');

router.get('/', auth, getAllTodos);
router.get('/:id', auth, getTodoById);
router.post('/', auth, createTodo);
router.put('/:id', auth, updateTodo);
router.delete('/:id', auth, deleteTodo);
router.patch('/:id/toggle', auth, toggleTodo);

module.exports = router;