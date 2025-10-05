import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  User,
  Mail,
  Car,
  Activity,
  AlertCircle,
  CheckCircle,
  Clock,
  ChevronRight,
  LogOut,
  Bell,
  Settings,
  Wifi,
  WifiOff
} from 'lucide-react'
import { supabase } from '../lib/supabase'

const Dashboard = () => {
  const navigate = useNavigate()
  const [supervisor, setSupervisor] = useState(null)
  const [drivers, setDrivers] = useState([])
  const [loading, setLoading] = useState(true)
  const [user, setUser] = useState(null)

  useEffect(() => {
    checkAuth()
  }, [])

  useEffect(() => {
    if (user) {
      fetchDrivers()
      // Poll every 2 seconds for updates
      const interval = setInterval(() => {
        fetchDrivers()
      }, 2000)
      return () => clearInterval(interval)
    }
  }, [user])

  const checkAuth = async () => {
    try {
      const { data: { user: currentUser }, error: authError } = await supabase.auth.getUser()

      if (authError || !currentUser) {
        navigate('/')
        return
      }

      setUser(currentUser)

      // Fetch supervisor info
      const { data: supervisorData, error: supervisorError } = await supabase
        .from('supervisors')
        .select('*')
        .eq('user_id', currentUser.id)
        .single()

      if (supervisorError) {
        console.error('Error fetching supervisor:', supervisorError)
        // Create supervisor if doesn't exist
        const name = currentUser.user_metadata?.full_name || currentUser.email.split('@')[0]
        const { data: newSupervisor } = await supabase
          .from('supervisors')
          .insert({
            user_id: currentUser.id,
            name: name,
            email: currentUser.email,
            role: 'Fleet Supervisor'
          })
          .select()
          .single()

        setSupervisor(newSupervisor || {
          name: name,
          email: currentUser.email,
          role: 'Fleet Supervisor',
          avatar: name.split(' ').map(n => n[0]).join('').toUpperCase()
        })
      } else {
        setSupervisor({
          ...supervisorData,
          avatar: supervisorData.name.split(' ').map(n => n[0]).join('').toUpperCase()
        })
      }
    } catch (error) {
      console.error('Error in checkAuth:', error)
      navigate('/')
    }
  }

  const handleLogout = async () => {
    await supabase.auth.signOut()
    navigate('/')
  }

  const fetchDrivers = async () => {
    try {
      // Fetch all drivers
      const { data: driversData, error: driversError } = await supabase
        .from('drivers')
        .select('*')
        .order('last_active', { ascending: false })

      if (driversError) throw driversError

      // Fetch all sessions for today
      const today = new Date().toISOString().split('T')[0]
      const { data: sessionsData } = await supabase
        .from('driving_sessions')
        .select('*')
        .gte('started_at', `${today}T00:00:00`)

      // Process drivers data
      const processedDrivers = driversData.map(driver => {
        const driverSessions = sessionsData?.filter(s => s.driver_id === driver.id) || []
        const activeSession = driverSessions.find(s => s.status === 'active')

        return {
          id: driver.id,
          name: driver.name,
          email: driver.email,
          arduinoId: driver.arduino_id,
          status: driver.status,
          connectionStatus: driver.connection_status || 'offline',
          lastActive: formatLastActive(driver.last_active),
          tripsToday: driverSessions.length,
          safetyScore: driver.safety_score || 100,
          avatar: getInitials(driver.name),
          hasActiveSession: !!activeSession
        }
      })

      setDrivers(processedDrivers)
    } catch (error) {
      console.error('Error fetching drivers:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatLastActive = (timestamp) => {
    if (!timestamp) return 'Never'
    const now = new Date()
    const then = new Date(timestamp)
    const diffMs = now - then
    const diffMins = Math.floor(diffMs / 60000)

    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins} min${diffMins > 1 ? 's' : ''} ago`

    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`

    const diffDays = Math.floor(diffHours / 24)
    return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
  }

  const getInitials = (name) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase()
  }

  const getStatusColor = (status) => {
    switch(status) {
      case 'active': return 'bg-green-500'
      case 'warning': return 'bg-yellow-500'
      case 'inactive': return 'bg-gray-400'
      default: return 'bg-gray-400'
    }
  }

  const getStatusIcon = (status) => {
    switch(status) {
      case 'active': return <CheckCircle className="w-5 h-5" />
      case 'warning': return <AlertCircle className="w-5 h-5" />
      case 'inactive': return <Clock className="w-5 h-5" />
      default: return <Clock className="w-5 h-5" />
    }
  }

  const getSafetyScoreColor = (score) => {
    if (score >= 90) return 'text-green-600'
    if (score >= 75) return 'text-yellow-600'
    return 'text-red-600'
  }

  const handleDriverClick = (driver) => {
    // Navigate to driver detail page using driver ID
    navigate(`/driver/${driver.id}`)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#12161e' }}>
        <div className="text-white">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#12161e' }}>
      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur-lg" style={{ backgroundColor: '#12161e' }}>
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#38b6ff' }}>
                <Car className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold" style={{
                  color: '#ffffff',
                  fontFamily: 'Orbitron, monospace',
                  textShadow: '0 0 2px #ffffff, 0 0 4px #38b6ff, 0 0 8px #38b6ff',
                  letterSpacing: '2px',
                  textTransform: 'uppercase',
                  fontWeight: '900'
                }}>
                  FLEET DASHBOARD
                </h1>
                <p className="text-sm" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>Monitor your drivers in real-time</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleLogout}
                className="p-2 rounded-lg transition-colors"
                style={{ backgroundColor: '#1a1f2e' }}
              >
                <LogOut className="w-5 h-5" style={{ color: '#ffffff' }} />
              </motion.button>
            </div>
          </div>

          {/* Supervisor Info */}
          {supervisor && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-8 rounded-2xl p-6 border"
              style={{ backgroundColor: '#1a1f2e', borderColor: '#38b6ff' }}
            >
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-xl flex items-center justify-center text-xl font-bold" style={{ backgroundColor: '#38b6ff', color: '#12161e' }}>
                  {supervisor.avatar}
                </div>
                <div className="flex-1">
                  <h2 className="text-xl font-bold flex items-center gap-2" style={{ color: '#ffffff' }}>
                    {supervisor.name}
                  </h2>
                  <p className="flex items-center gap-2" style={{ color: '#a0a0a0' }}>
                    <Mail className="w-4 h-4" />
                    {supervisor.email}
                  </p>
                  <p className="text-sm" style={{ color: '#a0a0a0' }}>{supervisor.role}</p>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </header>

      {/* Drivers Section */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold mb-2" style={{ color: '#ffffff' }}>Your Drivers ({drivers.length})</h2>
          <p style={{ color: '#a0a0a0' }}>Click on a driver to see detailed information</p>
        </div>

        {/* Scrollable Driver Cards */}
        <div className="overflow-x-auto pb-4">
          <div className="flex gap-6" style={{ minWidth: 'min-content' }}>
            {drivers.map((driver, index) => (
              <motion.div
                key={driver.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.02, y: -4 }}
                onClick={() => handleDriverClick(driver)}
                className="rounded-2xl p-6 border flex-shrink-0 cursor-pointer"
                style={{
                  width: '320px',
                  backgroundColor: '#1a1f2e',
                  borderColor: driver.connectionStatus === 'online' ? '#38b6ff' : '#2a2f3e'
                }}
              >
                {/* Driver Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl flex items-center justify-center text-lg font-bold" style={{ backgroundColor: '#38b6ff', color: '#12161e' }}>
                      {driver.avatar}
                    </div>
                    <div>
                      <h3 className="font-bold" style={{ color: '#ffffff' }}>{driver.name}</h3>
                      <p className="text-sm" style={{ color: '#a0a0a0' }}>{driver.arduinoId}</p>
                    </div>
                  </div>
                  {driver.connectionStatus === 'online' && (
                    <div className="flex items-center gap-1 text-green-500">
                      <Wifi className="w-4 h-4" />
                      <span className="text-xs font-medium">LIVE</span>
                    </div>
                  )}
                  {driver.connectionStatus === 'offline' && (
                    <WifiOff className="w-4 h-4 text-gray-500" />
                  )}
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-xs mb-1" style={{ color: '#a0a0a0' }}>Safety Score</p>
                    <p className={`text-2xl font-bold ${getSafetyScoreColor(driver.safetyScore)}`}>
                      {driver.safetyScore}%
                    </p>
                  </div>
                  <div>
                    <p className="text-xs mb-1" style={{ color: '#a0a0a0' }}>Trips Today</p>
                    <p className="text-2xl font-bold" style={{ color: '#38b6ff' }}>
                      {driver.tripsToday}
                    </p>
                  </div>
                </div>

                {/* Status Badge */}
                <div className="flex items-center justify-between p-3 rounded-xl" style={{ backgroundColor: '#12161e' }}>
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${getStatusColor(driver.status)}`}></div>
                    <span className="text-sm font-medium" style={{ color: '#ffffff' }}>
                      {driver.status === 'active' ? 'Active' : driver.status === 'warning' ? 'Warning' : 'Inactive'}
                    </span>
                  </div>
                  <span className="text-xs" style={{ color: '#a0a0a0' }}>{driver.lastActive}</span>
                </div>

                {/* View Details */}
                <div className="mt-4 flex items-center justify-center gap-2 text-sm" style={{ color: '#38b6ff' }}>
                  View Details <ChevronRight className="w-4 h-4" />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}

export default Dashboard
