const mongoose = require('mongoose');

// Define Todo schema
const todoSchema = new mongoose.Schema({
  title: {
    type: String,
    required: [true, 'Title is required'],
    trim: true,
    maxlength: [200, 'Title cannot exceed 200 characters']
  },
  description: {
    type: String,
    default: '',
    maxlength: [1000, 'Description cannot exceed 1000 characters']
  },
  status: {
    type: String,
    enum: ['pending', 'in-progress', 'completed'],
    default: 'pending'
  },
  priority: {
    type: String,
    enum: ['low', 'medium', 'high'],
    default: 'medium'
  },
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  }
}, {
  timestamps: true
});

// Create Todo model
const Todo = mongoose.model('Todo', todoSchema);

// Find all todos with filter
const find = async (filter) => {
  try {
    return await Todo.find(filter);
  } catch (error) {
    throw error;
  }
};

// Find todo by ID and user ID
const findByIdAndUserId = async (id, userId) => {
  try {
    return await Todo.findOne({ _id: id, userId });
  } catch (error) {
    throw error;
  }
};

// Create todo
const create = async (todoData) => {
  try {
    const todo = new Todo(todoData);
    return await todo.save();
  } catch (error) {
    throw error;
  }
};

// Update todo by ID and user ID
const findByIdAndUpdateAndUserId = async (id, userId, updateData) => {
  try {
    return await Todo.findOneAndUpdate(
      { _id: id, userId },
      { ...updateData },
      { new: true, runValidators: true }
    );
  } catch (error) {
    throw error;
  }
};

// Delete todo by ID
const deleteById = async (id) => {
  try {
    return await Todo.findByIdAndDelete(id);
  } catch (error) {
    throw error;
  }
};

// Count documents
const countDocuments = async (filter) => {
  try {
    return await Todo.countDocuments(filter);
  } catch (error) {
    throw error;
  }
};

module.exports = {
  find,
  findByIdAndUserId,
  create,
  findByIdAndUpdateAndUserId: findByIdAndUpdateAndUserId,
  deleteById,
  countDocuments
};