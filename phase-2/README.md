# Phase 2 - Full Stack Todo Application

This is the Phase 2 implementation of the Todo Application, featuring a complete full-stack solution with authentication, database integration, and a modern web interface.

## 🚀 Overview

Phase 2 transforms the original CLI-based todo app into a modern web application with:
- Full user authentication (register/login)
- Personalized todo management
- Responsive web interface
- Secure API endpoints
- Database persistence

## 📁 Folder Structure

```
phase-2/
├── backend/                 # Node.js + Express backend
│   ├── src/
│   │   ├── controllers/     # Route controllers
│   │   ├── routes/         # API route definitions
│   │   ├── middlewares/    # Authentication & validation
│   │   ├── services/       # Database services
│   │   └── utils/          # Utility functions
│   ├── app.js             # Express app configuration
│   ├── server.js          # Server entry point
│   ├── package.json       # Backend dependencies
│   └── README.md          # Backend documentation
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js app router pages
│   │   ├── components/    # Reusable components
│   │   ├── services/      # API services
│   │   └── styles/        # Style files
│   ├── package.json       # Frontend dependencies
│   ├── next.config.js     # Next.js configuration
│   └── README.md          # Frontend documentation
└── README.md              # This file
```

## 🛠️ Tech Stack

### Backend
- **Node.js** - JavaScript runtime
- **Express** - Web framework
- **MongoDB** - Database
- **Mongoose** - ODM
- **JWT** - Authentication
- **Bcrypt** - Password hashing
- **Cors, Helmet, Morgan** - Security and logging

### Frontend
- **Next.js 14** - React framework with App Router
- **React** - UI library
- **Tailwind CSS** - Styling
- **Fetch API** - Client-side data fetching

## 🚀 Quick Start

### Prerequisites
- Node.js (v14 or higher)
- MongoDB (local or cloud instance)

### Backend Setup
1. Navigate to the backend directory: `cd phase-2/backend`
2. Install dependencies: `npm install`
3. Create `.env` file based on `.env.example`
4. Start the server: `npm run dev`

### Frontend Setup
1. Navigate to the frontend directory: `cd phase-2/frontend`
2. Install dependencies: `npm install`
3. Create `.env.local` file with `NEXT_PUBLIC_API_BASE_URL`
4. Start the development server: `npm run dev`

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user and get JWT token

### Todos
- `GET /api/todos` - Get all user's todos (requires auth)
- `GET /api/todos/:id` - Get a specific todo (requires auth)
- `POST /api/todos` - Create a new todo (requires auth)
- `PUT /api/todos/:id` - Update a todo (requires auth)
- `DELETE /api/todos/:id` - Delete a todo (requires auth)

## 📋 Features

### Authentication
- User registration with validation
- Secure login with JWT tokens
- Password hashing with bcrypt
- Protected routes

### Todo Management
- Create, read, update, delete todos
- Set priority levels (low, medium, high)
- Track todo status (pending, in-progress, completed)
- Filter and sort functionality

### Security
- Input validation and sanitization
- Rate limiting
- CORS configuration
- JWT token authentication
- Password security with bcrypt

## 🚀 Deployment

### Backend Deployment
The backend can be deployed to platforms like:
- Heroku
- DigitalOcean
- AWS
- Google Cloud Platform

Remember to set environment variables in your deployment platform.

### Frontend Deployment
The frontend can be deployed to:
- Vercel (recommended for Next.js)
- Netlify
- AWS Amplify
- Any static hosting service

## 🧪 Testing

Backend tests can be run with Jest:
```bash
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, please open an issue in the repository.

---

**Note:** Phase 1 (CLI-based todo app) remains completely untouched and functional in the parent directory.