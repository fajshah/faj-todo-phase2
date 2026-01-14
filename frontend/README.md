# Todo Frontend

Frontend for the Phase II Todo Full-Stack Web Application built with Next.js.

## Features

- Responsive user interface
- Task management dashboard
- User authentication
- Real-time task updates
- Clean and modern UI

## Environment Variables

Create a `.env.local` file in the root of the frontend directory with the following:

```env
NEXT_PUBLIC_API_URL=https://fajji-backend-todo.hf.space/api
```

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) to view the application in your browser.

## API Integration

The frontend is configured to communicate with the backend API at the URL specified in `NEXT_PUBLIC_API_URL`. The application handles:

- User authentication (signup/login)
- Task CRUD operations
- Real-time updates
- Error handling

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Lint the code