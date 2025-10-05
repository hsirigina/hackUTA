# HackUTA Frontend - Driver Monitoring Dashboard

A modern React-based authentication and dashboard system for fleet supervisors to monitor their drivers in real-time.

## Features

✨ **Beautiful Authentication**
- Modern login/signup page with smooth animations
- Supabase authentication integration
- Social login options (Google, GitHub, Apple)
- Form validation and error handling

📊 **Supervisor Dashboard**
- View supervisor information at a glance
- Horizontally scrollable driver cards
- Real-time driver status monitoring
- Arduino device tracking
- Safety scores and trip statistics

## Tech Stack

- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React Router** - Navigation
- **Supabase** - Authentication & Backend
- **Lucide React** - Icons

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update with your Supabase credentials (already configured)

### Development

Run the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── AuthPage.jsx      # Login/Signup page
│   │   └── Dashboard.jsx      # Supervisor dashboard
│   ├── lib/
│   │   └── supabase.js        # Supabase client config
│   ├── App.jsx                # Main app with routing
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── public/                    # Static assets
├── index.html                 # HTML template
├── vite.config.js            # Vite configuration
├── tailwind.config.js        # Tailwind configuration
└── package.json              # Dependencies

```

## Routes

- `/` - Authentication page (Login/Signup)
- `/dashboard` - Supervisor dashboard (protected)

## Environment Variables

```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Mock Data

The dashboard currently uses mock data for:
- Supervisor information
- Driver profiles
- Arduino device associations
- Safety scores and trip statistics

Replace with real API calls when backend is ready.

## Future Enhancements

- [ ] Protected route authentication
- [ ] Real-time driver tracking
- [ ] Driver detail pages
- [ ] Analytics and reporting
- [ ] Push notifications for alerts
- [ ] Export data functionality

## License

MIT
