const mongoose = require('mongoose');

// Define User schema
const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: [true, 'Username is required'],
    unique: true,
    trim: true,
    minlength: [3, 'Username must be at least 3 characters long']
  },
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'Please enter a valid email']
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: [6, 'Password must be at least 6 characters long']
  }
}, {
  timestamps: true
});

// Create User model
const User = mongoose.model('User', userSchema);

// Create user
const create = async (userData) => {
  try {
    const user = new User(userData);
    return await user.save();
  } catch (error) {
    throw error;
  }
};

// Find user by email
const findByEmail = async (email) => {
  try {
    return await User.findOne({ email });
  } catch (error) {
    throw error;
  }
};

// Find user by email or username
const findByEmailOrUsername = async (email, username) => {
  try {
    return await User.findOne({
      $or: [
        { email },
        { username }
      ]
    });
  } catch (error) {
    throw error;
  }
};

module.exports = {
  create,
  findByEmail,
  findByEmailOrUsername
};