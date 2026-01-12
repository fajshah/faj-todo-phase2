# Phase 2 Frontend - Todo App

This is the frontend for the Phase 2 Todo Application, built with Next.js 14 and Tailwind CSS.

## Features

- Modern, responsive UI with Tailwind CSS
- Authentication pages (Login/Register)
- Todo dashboard with CRUD operations
- State management with React Hooks
- API integration with the backend
- Environment-based configuration

## Pages

- `/` - Landing page
- `/login` - User login
- `/register` - User registration
- `/dashboard` - Todo management dashboard

## Setup Instructions

1. Clone the repository
2. Navigate to the frontend directory: `cd phase-2/frontend`
3. Install dependencies: `npm install`
4. Create a `.env.local` file based on the environment variables below
5. Start the development server: `npm run dev`

## Environment Variables

Create a `.env.local` file in the frontend root directory with the following variables:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
```

## Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run start` - Start the production server
- `npm run lint` - Run the linter

## Deployment

The frontend is ready for deployment to platforms like Vercel, Netlify, or other hosting providers that support Next.js applications. Make sure to set the environment variables in your deployment platform.

## Dependencies

- react: UI library
- react-dom: React package for DOM manipulation
- next: React framework
- tailwindcss: CSS framework
- autoprefixer: PostCSS plugin
- postcss: CSS processor