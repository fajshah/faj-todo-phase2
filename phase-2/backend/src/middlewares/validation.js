const validateRegister = (req, res, next) => {
  const { username, email, password } = req.body;

  // Username validation
  if (!username || typeof username !== 'string' || username.trim().length < 3) {
    return res.status(400).json({
      error: 'Username must be at least 3 characters long'
    });
  }

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email || !emailRegex.test(email)) {
    return res.status(400).json({
      error: 'Valid email is required'
    });
  }

  // Password validation
  if (!password || password.length < 6) {
    return res.status(400).json({
      error: 'Password must be at least 6 characters long'
    });
  }

  next();
};

const validateLogin = (req, res, next) => {
  const { email, password } = req.body;

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email || !emailRegex.test(email)) {
    return res.status(400).json({
      error: 'Valid email is required'
    });
  }

  // Password validation
  if (!password || typeof password !== 'string') {
    return res.status(400).json({
      error: 'Password is required'
    });
  }

  next();
};

const validateTodoCreation = (req, res, next) => {
  const { title, description, priority } = req.body;

  if (!title || typeof title !== 'string' || title.trim().length === 0) {
    return res.status(400).json({
      error: 'Title is required and must be a non-empty string'
    });
  }

  if (description && typeof description !== 'string') {
    return res.status(400).json({
      error: 'Description must be a string if provided'
    });
  }

  if (priority && !['low', 'medium', 'high'].includes(priority)) {
    return res.status(400).json({
      error: 'Priority must be one of: low, medium, high'
    });
  }

  next();
};

const validateTodoUpdate = (req, res, next) => {
  const { title, description, status, priority } = req.body;

  if (title !== undefined && (typeof title !== 'string' || title.trim().length === 0)) {
    return res.status(400).json({
      error: 'Title must be a non-empty string if provided'
    });
  }

  if (description !== undefined && typeof description !== 'string') {
    return res.status(400).json({
      error: 'Description must be a string if provided'
    });
  }

  if (status !== undefined && !['pending', 'in-progress', 'completed'].includes(status)) {
    return res.status(400).json({
      error: 'Status must be one of: pending, in-progress, completed'
    });
  }

  if (priority !== undefined && !['low', 'medium', 'high'].includes(priority)) {
    return res.status(400).json({
      error: 'Priority must be one of: low, medium, high'
    });
  }

  next();
};

const errorHandler = (err, req, res, next) => {
  console.error(err.stack);

  // Handle Mongoose validation errors
  if (err.name === 'ValidationError') {
    const errors = Object.values(err.errors).map(e => e.message);
    return res.status(400).json({ error: errors.join(', ') });
  }

  // Handle Mongoose duplicate key errors
  if (err.code === 11000) {
    return res.status(400).json({ error: 'Duplicate field value entered' });
  }

  // Handle JWT errors
  if (err.name === 'JsonWebTokenError') {
    return res.status(401).json({ error: 'Invalid token' });
  }

  if (err.name === 'TokenExpiredError') {
    return res.status(401).json({ error: 'Token expired' });
  }

  // Default error
  res.status(500).json({ error: 'Internal server error' });
};

module.exports = {
  validateRegister,
  validateLogin,
  validateTodoCreation,
  validateTodoUpdate,
  errorHandler
};