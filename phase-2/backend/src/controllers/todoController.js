const Todo = require('../services/todoService');

const getAllTodos = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { page = 1, limit = 10, status, priority } = req.query;

    const filter = { userId };
    if (status) filter.status = status;
    if (priority) filter.priority = priority;

    const todos = await Todo.find(filter)
      .sort({ createdAt: -1 })
      .limit(limit * 1)
      .skip((page - 1) * limit)
      .exec();

    const total = await Todo.countDocuments(filter);

    res.status(200).json({
      todos,
      totalPages: Math.ceil(total / limit),
      currentPage: page,
      total
    });
  } catch (error) {
    console.error('Get all todos error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

const getTodoById = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { id } = req.params;

    const todo = await Todo.findByIdAndUserId(id, userId);
    if (!todo) {
      return res.status(404).json({ error: 'Todo not found' });
    }

    res.status(200).json(todo);
  } catch (error) {
    console.error('Get todo by ID error:', error);
    if (error.name === 'CastError') {
      return res.status(400).json({ error: 'Invalid todo ID' });
    }
    res.status(500).json({ error: 'Internal server error' });
  }
};

const createTodo = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { title, description, priority = 'medium' } = req.body;

    if (!title) {
      return res.status(400).json({ error: 'Title is required' });
    }

    const todo = await Todo.create({
      title,
      description,
      priority,
      userId
    });

    res.status(201).json(todo);
  } catch (error) {
    console.error('Create todo error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

const updateTodo = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { id } = req.params;
    const { title, description, status, priority } = req.body;

    const updateData = {};
    if (title !== undefined) updateData.title = title;
    if (description !== undefined) updateData.description = description;
    if (status !== undefined) updateData.status = status;
    if (priority !== undefined) updateData.priority = priority;

    const todo = await Todo.findByIdAndUpdateAndUserId(id, userId, updateData);
    if (!todo) {
      return res.status(404).json({ error: 'Todo not found' });
    }

    res.status(200).json(todo);
  } catch (error) {
    console.error('Update todo error:', error);
    if (error.name === 'CastError') {
      return res.status(400).json({ error: 'Invalid todo ID' });
    }
    res.status(500).json({ error: 'Internal server error' });
  }
};

const deleteTodo = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { id } = req.params;

    const todo = await Todo.findByIdAndUserId(id, userId);
    if (!todo) {
      return res.status(404).json({ error: 'Todo not found' });
    }

    await Todo.deleteById(id);
    res.status(200).json({ message: 'Todo deleted successfully' });
  } catch (error) {
    console.error('Delete todo error:', error);
    if (error.name === 'CastError') {
      return res.status(400).json({ error: 'Invalid todo ID' });
    }
    res.status(500).json({ error: 'Internal server error' });
  }
};

module.exports = {
  getAllTodos,
  getTodoById,
  createTodo,
  updateTodo,
  deleteTodo
};