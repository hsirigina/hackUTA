import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  ArrowLeft,
  Activity,
  AlertTriangle,
  TrendingDown,
  Zap,
  Clock,
  CheckCircle,
  WifiOff,
  Wifi,
  Eye,
  EyeOff,
  AlertCircle
} from 'lucide-react'
import { supabase } from '../lib/supabase'

const DriverDetail = () => {
  const { driverId } = useParams()
  const navigate = useNavigate()
  const [driver, setDriver] = useState(null)
  const [currentSession, setCurrentSession] = useState(null)
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [user, setUser] = useState(null)

  // Check auth on mount
  useEffect(() => {
    checkAuth()
  }, [])

  // Fetch driver details with polling
  useEffect(() => {
    if (user && driverId) {
      fetchDriverDetails()

      // Poll every 2 seconds
      const interval = setInterval(() => {
        fetchDriverDetails()
      }, 2000)

      return () => {
        clearInterval(interval)
      }
    }
  }, [driverId, user])

  const checkAuth = async () => {
    const { data: { user: currentUser }, error } = await supabase.auth.getUser()

    if (error || !currentUser) {
      navigate('/')
      return
    }

    setUser(currentUser)
  }

  const fetchDriverDetails = async () => {
    try {
      // Fetch driver info
      const { data: driverData, error: driverError } = await supabase
        .from('drivers')
        .select('*')
        .eq('id', driverId)
        .single()

      if (driverError) throw driverError

      setDriver(driverData)

      // Fetch current active session
      const { data: sessionData, error: sessionError } = await supabase
        .from('driving_sessions')
        .select('*')
        .eq('driver_id', driverId)
        .eq('status', 'active')
        .order('started_at', { ascending: false })
        .limit(1)
        .single()

      setCurrentSession(sessionData)

      // Fetch events for current session
      if (sessionData) {
        const { data: eventsData, error: eventsError } = await supabase
          .from('events')
          .select('*')
          .eq('session_id', sessionData.id)
          .order('timestamp', { ascending: false })

        if (!eventsError) {
          console.log('📊 Fetched events:', eventsData?.length || 0)
          console.log('Event types:', eventsData?.map(e => e.event_type))
          setEvents(eventsData || [])
        } else {
          console.error('Error fetching events:', eventsError)
        }
      }

    } catch (error) {
      console.error('Error fetching driver details:', error)
    } finally {
      setLoading(false)
    }
  }

  const getEventCounts = () => {
    if (!currentSession) return {
      swerving: 0,
      harsh_brake: 0,
      aggressive: 0,
      distracted: 0,
      drowsy: 0,
      eyes_closed: 0
    }

    // Count attention events from events array
    const distractedCount = events.filter(e => e.event_type === 'DISTRACTED').length
    const drowsyCount = events.filter(e => e.event_type === 'DROWSY').length
    const eyesClosedCount = events.filter(e => e.event_type === 'EYES_CLOSED').length

    console.log('🔢 Event counts:', {
      totalEvents: events.length,
      distracted: distractedCount,
      drowsy: drowsyCount,
      eyes_closed: eyesClosedCount
    })

    return {
      swerving: currentSession.total_swerving || 0,
      harsh_brake: currentSession.total_harsh_brake || 0,
      aggressive: currentSession.total_aggressive || 0,
      distracted: distractedCount,
      drowsy: drowsyCount,
      eyes_closed: eyesClosedCount
    }
  }

  const formatDuration = (startTime) => {
    if (!startTime) return '0m'
    const start = new Date(startTime)
    const now = new Date()
    const diffMinutes = Math.floor((now - start) / 60000)

    if (diffMinutes < 60) return `${diffMinutes}m`
    const hours = Math.floor(diffMinutes / 60)
    const minutes = diffMinutes % 60
    return `${hours}h ${minutes}m`
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading driver details...</p>
        </div>
      </div>
    )
  }

  if (!driver) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Driver not found</p>
          <button onClick={() => navigate('/dashboard')} className="mt-4 text-blue-600">
            Back to Dashboard
          </button>
        </div>
      </div>
    )
  }

  const eventCounts = getEventCounts()

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 backdrop-blur-lg bg-white/80">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/dashboard')}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-6 h-6" />
            </motion.button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Driver Details</h1>
              <p className="text-sm text-gray-500">Real-time session monitoring</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Driver Info Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-100"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                {driver.name.split(' ').map(n => n[0]).join('').toUpperCase()}
              </div>
              <div>
                <h2 className="text-3xl font-bold text-gray-900 mb-1">{driver.name}</h2>
                <p className="text-gray-600">{driver.email}</p>
                <div className="flex items-center gap-3 mt-2">
                  <span className="font-mono text-sm bg-gray-100 px-3 py-1 rounded-lg">
                    {driver.arduino_id}
                  </span>
                  {driver.connection_status === 'online' ? (
                    <div className="flex items-center gap-1 text-green-600">
                      <CheckCircle className="w-4 h-4" />
                      <Wifi className="w-4 h-4" />
                      <span className="text-sm font-medium">Live</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-1 text-gray-400">
                      <WifiOff className="w-4 h-4" />
                      <span className="text-sm">Offline</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-5xl font-bold text-gray-900 mb-1">{driver.safety_score}%</div>
              <p className="text-gray-600">Safety Score</p>
            </div>
          </div>
        </motion.div>

        {/* Current Session Status */}
        {currentSession ? (
          <>
            {/* Session Header */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl shadow-lg p-6 mb-8 text-white"
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-2xl font-bold mb-2">Current Session Active</h3>
                  <p className="opacity-90">Real-time monitoring in progress</p>
                </div>
                <div className="text-right">
                  <div className="flex items-center gap-2 mb-2">
                    <Clock className="w-5 h-5" />
                    <span className="text-lg font-semibold">
                      {formatDuration(currentSession.started_at)}
                    </span>
                  </div>
                  <p className="opacity-90 text-sm">Session Duration</p>
                </div>
              </div>
            </motion.div>

            {/* Driving Event Statistics Grid */}
            <h3 className="text-lg font-bold text-gray-900 mb-4">🚗 Driving Events</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Sharp Turns / Swerving */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center">
                    <TrendingDown className="w-6 h-6 text-yellow-600" />
                  </div>
                  <span className="text-4xl font-bold text-yellow-600">{eventCounts.swerving}</span>
                </div>
                <h4 className="font-semibold text-gray-900">Sharp Turns</h4>
                <p className="text-sm text-gray-500">Swerving events detected</p>
              </motion.div>

              {/* Hard Brakes */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center">
                    <AlertTriangle className="w-6 h-6 text-red-600" />
                  </div>
                  <span className="text-4xl font-bold text-red-600">{eventCounts.harsh_brake}</span>
                </div>
                <h4 className="font-semibold text-gray-900">Hard Brakes</h4>
                <p className="text-sm text-gray-500">Harsh braking events</p>
              </motion.div>

              {/* Aggressive Acceleration */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
                    <Zap className="w-6 h-6 text-orange-600" />
                  </div>
                  <span className="text-4xl font-bold text-orange-600">{eventCounts.aggressive}</span>
                </div>
                <h4 className="font-semibold text-gray-900">Aggressive Driving</h4>
                <p className="text-sm text-gray-500">Aggressive acceleration</p>
              </motion.div>
            </div>

            {/* Attention Event Statistics Grid */}
            <h3 className="text-lg font-bold text-gray-900 mb-4 mt-8">👁️ Attention Events</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Distracted */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                    <Eye className="w-6 h-6 text-blue-600" />
                  </div>
                  <span className="text-4xl font-bold text-blue-600">{eventCounts.distracted}</span>
                </div>
                <h4 className="font-semibold text-gray-900">Distracted</h4>
                <p className="text-sm text-gray-500">Looking away from road</p>
              </motion.div>

              {/* Drowsy */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                    <AlertCircle className="w-6 h-6 text-purple-600" />
                  </div>
                  <span className="text-4xl font-bold text-purple-600">{eventCounts.drowsy}</span>
                </div>
                <h4 className="font-semibold text-gray-900">Drowsy</h4>
                <p className="text-sm text-gray-500">Eyes closing - drowsy</p>
              </motion.div>

              {/* Eyes Closed */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 }}
                className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center">
                    <EyeOff className="w-6 h-6 text-red-600" />
                  </div>
                  <span className="text-4xl font-bold text-red-600">{eventCounts.eyes_closed}</span>
                </div>
                <h4 className="font-semibold text-gray-900">Eyes Closed</h4>
                <p className="text-sm text-gray-500">No eyes detected</p>
              </motion.div>
            </div>

            {/* Safety Score Visualization */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-100"
            >
              <h3 className="text-xl font-bold text-gray-900 mb-6">Safety Score Over Time</h3>
              <div className="relative pt-1">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Current Session Score</span>
                  <span className="text-sm font-bold text-gray-900">{currentSession.safety_score || driver.safety_score}%</span>
                </div>
                <div className="overflow-hidden h-4 text-xs flex rounded-full bg-gray-200">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${currentSession.safety_score || driver.safety_score}%` }}
                    transition={{ duration: 1, delay: 0.6 }}
                    className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${
                      (currentSession.safety_score || driver.safety_score) >= 90
                        ? 'bg-green-500'
                        : (currentSession.safety_score || driver.safety_score) >= 75
                        ? 'bg-yellow-500'
                        : 'bg-red-500'
                    }`}
                  ></motion.div>
                </div>
              </div>
            </motion.div>

            {/* Recent Events Timeline */}
            {events.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100"
              >
                <h3 className="text-xl font-bold text-gray-900 mb-6">Recent Events</h3>
                <div className="space-y-4">
                  {events.slice(0, 10).map((event, index) => (
                    <div
                      key={event.id}
                      className="flex items-center gap-4 p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors"
                    >
                      <div className={`w-2 h-2 rounded-full ${
                        event.severity === 'high' ? 'bg-red-500' :
                        event.severity === 'medium' ? 'bg-yellow-500' :
                        'bg-blue-500'
                      }`}></div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-gray-900">{event.event_type.replace('_', ' ')}</span>
                          <span className={`text-xs px-2 py-1 rounded-full ${
                            event.severity === 'high' ? 'bg-red-100 text-red-700' :
                            event.severity === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-blue-100 text-blue-700'
                          }`}>
                            {event.severity}
                          </span>
                        </div>
                        <p className="text-sm text-gray-500">
                          {new Date(event.timestamp).toLocaleString()}
                        </p>
                      </div>
                      <div className="text-right text-sm text-gray-600">
                        <p>X: {event.x.toFixed(2)}</p>
                        <p>Y: {event.y.toFixed(2)}</p>
                        <p>Z: {event.z.toFixed(2)}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}
          </>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-2xl shadow-lg p-12 text-center border border-gray-100"
          >
            <Activity className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-gray-900 mb-2">No Active Session</h3>
            <p className="text-gray-600 mb-6">
              This driver doesn't have an active driving session right now.
            </p>
            <p className="text-sm text-gray-500">
              Start the Arduino and run <code className="bg-gray-100 px-2 py-1 rounded">ble_supabase.py</code> to begin monitoring.
            </p>
          </motion.div>
        )}
      </main>
    </div>
  )
}

export default DriverDetail
