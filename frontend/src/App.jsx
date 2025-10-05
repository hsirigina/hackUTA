import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import AuthPage from './components/AuthPage'
import Dashboard from './components/Dashboard'
import DriverDetail from './components/DriverDetail'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AuthPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/driver/:driverId" element={<DriverDetail />} />
      </Routes>
    </Router>
  )
}

export default App
