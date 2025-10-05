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
import CircularProgress from './ui/CircularProgress'

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

      // Fetch current active session (most recent one)
      const { data: sessionData, error: sessionError } = await supabase
        .from('driving_sessions')
        .select('*')
        .eq('driver_id', driverId)
        .eq('status', 'active')
        .order('started_at', { ascending: false })
        .limit(1)
        .maybeSingle()  // Changed from .single() to handle multiple active sessions

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

    // Count ALL events from events array (not from session counters)
    const swervingCount = events.filter(e => e.event_type === 'SWERVING').length
    const harshBrakeCount = events.filter(e => e.event_type === 'HARSH_BRAKE').length
    const aggressiveCount = events.filter(e => e.event_type === 'AGGRESSIVE').length
    const distractedCount = events.filter(e => e.event_type === 'DISTRACTED').length
    // Combine DROWSY and EYES_CLOSED into "Drowsy"
    const drowsyCount = events.filter(e => e.event_type === 'DROWSY' || e.event_type === 'EYES_CLOSED').length

    console.log('🔢 Event counts from events array:', {
      totalEvents: events.length,
      swerving: swervingCount,
      harsh_brake: harshBrakeCount,
      aggressive: aggressiveCount,
      distracted: distractedCount,
      drowsy: drowsyCount
    })

    return {
      swerving: swervingCount,
      harsh_brake: harshBrakeCount,
      aggressive: aggressiveCount,
      distracted: distractedCount,
      drowsy: drowsyCount
    }
  }

  const getRecentEventTypes = () => {
    // Get the most recent event and return its type
    if (events.length === 0) return new Set()

    const mostRecentEvent = events[0]
    const eventTypes = new Set()

    if (mostRecentEvent.event_type === 'SWERVING') eventTypes.add('swerving')
    if (mostRecentEvent.event_type === 'HARSH_BRAKE') eventTypes.add('harsh_brake')
    if (mostRecentEvent.event_type === 'AGGRESSIVE') eventTypes.add('aggressive')
    if (mostRecentEvent.event_type === 'DISTRACTED') eventTypes.add('distracted')
    if (mostRecentEvent.event_type === 'DROWSY' || mostRecentEvent.event_type === 'EYES_CLOSED') eventTypes.add('drowsy')

    return eventTypes
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
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#12161e' }}>
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-t-transparent rounded-full animate-spin mx-auto mb-4" style={{ borderColor: '#38b6ff', borderTopColor: 'transparent' }}></div>
          <p style={{ color: '#a0a0a0' }}>Loading driver details...</p>
        </div>
      </div>
    )
  }

  if (!driver) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#12161e' }}>
        <div className="text-center">
          <p style={{ color: '#a0a0a0' }}>Driver not found</p>
          <button onClick={() => navigate('/dashboard')} className="mt-4 px-4 py-2 rounded-lg" style={{ backgroundColor: '#38b6ff', color: '#12161e' }}>
            Back to Dashboard
          </button>
        </div>
      </div>
    )
  }

  const eventCounts = getEventCounts()
  const recentEventTypes = getRecentEventTypes()

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#12161e' }}>
      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur-lg" style={{ backgroundColor: '#12161e', borderBottom: '1px solid #2a2f3e' }}>
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/dashboard')}
              className="p-2 rounded-lg transition-colors"
              style={{ backgroundColor: '#1a1f2e', color: '#ffffff' }}
            >
              <ArrowLeft className="w-6 h-6" />
            </motion.button>
            <div>
              <h1 className="text-2xl font-bold" style={{ color: '#ffffff' }}>Driver Details</h1>
              <p className="text-sm" style={{ color: '#a0a0a0' }}>Real-time session monitoring</p>
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
          className="rounded-2xl shadow-lg p-8 mb-8"
          style={{ backgroundColor: '#1a1f2e', border: '1px solid #2a2f3e' }}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <div className="w-20 h-20 rounded-2xl flex items-center justify-center text-2xl font-bold shadow-lg" style={{ backgroundColor: '#38b6ff', color: '#12161e' }}>
                {driver.name.split(' ').map(n => n[0]).join('').toUpperCase()}
              </div>
              <div>
                <h2 className="text-3xl font-bold mb-1" style={{ color: '#ffffff' }}>{driver.name}</h2>
                <p style={{ color: '#a0a0a0' }}>{driver.email}</p>
                <div className="flex items-center gap-3 mt-2">
                  <span className="font-mono text-sm px-3 py-1 rounded-lg" style={{ backgroundColor: '#12161e', color: '#a0a0a0' }}>
                    {driver.arduino_id}
                  </span>
                  {driver.connection_status === 'online' ? (
                    <div className="flex items-center gap-1 text-green-500">
                      <CheckCircle className="w-4 h-4" />
                      <Wifi className="w-4 h-4" />
                      <span className="text-sm font-medium">Live</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-1 text-gray-500">
                      <WifiOff className="w-4 h-4" />
                      <span className="text-sm">Offline</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
            <div className="flex items-center justify-center">
              <CircularProgress value={driver.safety_score} size={160} strokeWidth={14} />
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
              className="rounded-2xl shadow-lg p-6 mb-8"
              style={{ backgroundColor: '#38b6ff', color: '#12161e' }}
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
            <h3 className="text-lg font-bold text-white mb-4">Driving Events</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Sharp Turns / Swerving */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="rounded-2xl shadow-lg p-6 relative"
                style={{
                  backgroundColor: '#1a1f2e',
                  border: recentEventTypes.has('swerving') ? '2px solid #ef4444' : '1px solid #2a2f3e',
                  boxShadow: recentEventTypes.has('swerving') ? '0 0 20px rgba(239, 68, 68, 0.3)' : undefined
                }}
              >
                {recentEventTypes.has('swerving') && (
                  <motion.div
                    className="absolute inset-0 rounded-2xl"
                    style={{ border: '2px solid #ef4444' }}
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                )}
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ backgroundColor: 'rgba(202, 138, 4, 0.2)' }}>
                    <TrendingDown className="w-6 h-6 text-yellow-500" />
                  </div>
                  <span className="text-4xl font-bold text-yellow-500">{eventCounts.swerving}</span>
                </div>
                <h4 className="font-semibold text-white">Sharp Turns</h4>
                <p className="text-sm" style={{ color: '#a0a0a0' }}>Swerving events detected</p>
              </motion.div>

              {/* Hard Brakes */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="rounded-2xl shadow-lg p-6 relative"
                style={{
                  backgroundColor: '#1a1f2e',
                  border: recentEventTypes.has('harsh_brake') ? '2px solid #ef4444' : '1px solid #2a2f3e',
                  boxShadow: recentEventTypes.has('harsh_brake') ? '0 0 20px rgba(239, 68, 68, 0.3)' : undefined
                }}
              >
                {recentEventTypes.has('harsh_brake') && (
                  <motion.div
                    className="absolute inset-0 rounded-2xl"
                    style={{ border: '2px solid #ef4444' }}
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                )}
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ backgroundColor: 'rgba(239, 68, 68, 0.2)' }}>
                    <AlertTriangle className="w-6 h-6 text-red-500" />
                  </div>
                  <span className="text-4xl font-bold text-red-500">{eventCounts.harsh_brake}</span>
                </div>
                <h4 className="font-semibold text-white">Hard Brakes</h4>
                <p className="text-sm" style={{ color: '#a0a0a0' }}>Harsh braking events</p>
              </motion.div>

              {/* Aggressive Acceleration */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="rounded-2xl shadow-lg p-6 relative"
                style={{
                  backgroundColor: '#1a1f2e',
                  border: recentEventTypes.has('aggressive') ? '2px solid #ef4444' : '1px solid #2a2f3e',
                  boxShadow: recentEventTypes.has('aggressive') ? '0 0 20px rgba(239, 68, 68, 0.3)' : undefined
                }}
              >
                {recentEventTypes.has('aggressive') && (
                  <motion.div
                    className="absolute inset-0 rounded-2xl"
                    style={{ border: '2px solid #ef4444' }}
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                )}
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ backgroundColor: 'rgba(249, 115, 22, 0.2)' }}>
                    <Zap className="w-6 h-6 text-orange-500" />
                  </div>
                  <span className="text-4xl font-bold text-orange-500">{eventCounts.aggressive}</span>
                </div>
                <h4 className="font-semibold text-white">Aggressive Driving</h4>
                <p className="text-sm" style={{ color: '#a0a0a0' }}>Aggressive acceleration</p>
              </motion.div>
            </div>

            {/* Attention Event Statistics Grid */}
            <h3 className="text-lg font-bold text-white mb-4 mt-8">Attention Events</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Distracted */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="rounded-2xl shadow-lg p-6 relative"
                style={{
                  backgroundColor: '#1a1f2e',
                  border: recentEventTypes.has('distracted') ? '2px solid #ef4444' : '1px solid #2a2f3e',
                  boxShadow: recentEventTypes.has('distracted') ? '0 0 20px rgba(239, 68, 68, 0.3)' : undefined
                }}
              >
                {recentEventTypes.has('distracted') && (
                  <motion.div
                    className="absolute inset-0 rounded-2xl"
                    style={{ border: '2px solid #ef4444' }}
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                )}
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ backgroundColor: 'rgba(56, 182, 255, 0.2)' }}>
                    <Eye className="w-6 h-6" style={{ color: '#38b6ff' }} />
                  </div>
                  <span className="text-4xl font-bold" style={{ color: '#38b6ff' }}>{eventCounts.distracted}</span>
                </div>
                <h4 className="font-semibold text-white">Distracted</h4>
                <p className="text-sm" style={{ color: '#a0a0a0' }}>Looking away from road</p>
              </motion.div>

              {/* Drowsy (combines DROWSY and EYES_CLOSED) */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="rounded-2xl shadow-lg p-6 relative"
                style={{
                  backgroundColor: '#1a1f2e',
                  border: recentEventTypes.has('drowsy') ? '2px solid #ef4444' : '1px solid #2a2f3e',
                  boxShadow: recentEventTypes.has('drowsy') ? '0 0 20px rgba(239, 68, 68, 0.3)' : undefined
                }}
              >
                {recentEventTypes.has('drowsy') && (
                  <motion.div
                    className="absolute inset-0 rounded-2xl"
                    style={{ border: '2px solid #ef4444' }}
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                )}
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ backgroundColor: 'rgba(239, 68, 68, 0.2)' }}>
                    <EyeOff className="w-6 h-6 text-red-500" />
                  </div>
                  <span className="text-4xl font-bold text-red-500">{eventCounts.drowsy}</span>
                </div>
                <h4 className="font-semibold text-white">Drowsy</h4>
                <p className="text-sm" style={{ color: '#a0a0a0' }}>Eyes closing or closed</p>
              </motion.div>
            </div>

            {/* Safety Score Visualization */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="rounded-2xl shadow-lg p-8 mb-8" style={{ backgroundColor: '#1a1f2e', border: '1px solid #2a2f3e' }}
            >
              <h3 className="text-xl font-bold text-white mb-6">Safety Score Over Time</h3>
              <div className="relative pt-1">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium" style={{ color: '#a0a0a0' }}>Current Session Score</span>
                  <span className="text-sm font-bold text-white">{currentSession.safety_score || driver.safety_score}%</span>
                </div>
                <div className="overflow-hidden h-4 text-xs flex rounded-full" style={{ backgroundColor: '#2a2f3e' }}>
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
                className="rounded-2xl shadow-lg p-8" style={{ backgroundColor: '#1a1f2e', border: '1px solid #2a2f3e' }}
              >
                <h3 className="text-xl font-bold text-white mb-6">Recent Events</h3>
                <div className="space-y-4">
                  {events.slice(0, 10).map((event, index) => {
                    // Check if this is a driving event (has accelerometer data) or attention event
                    const isDrivingEvent = ['SWERVING', 'HARSH_BRAKE', 'AGGRESSIVE'].includes(event.event_type)
                    const isAttentionEvent = ['DISTRACTED', 'DROWSY', 'EYES_CLOSED'].includes(event.event_type)

                    return (
                      <div
                        key={event.id}
                        className="flex items-center gap-4 p-4 rounded-xl transition-colors"
                        style={{ backgroundColor: '#12161e', border: '1px solid #2a2f3e' }}
                        onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#1a1f2e'}
                        onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#12161e'}
                      >
                        <div className={`w-2 h-2 rounded-full ${
                          event.severity === 'high' ? 'bg-red-500' :
                          event.severity === 'medium' ? 'bg-yellow-500' :
                          'bg-blue-500'
                        }`}></div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-white">
                              {event.event_type.replace(/_/g, ' ')}
                            </span>
                            <span className={`text-xs px-2 py-1 rounded-full ${
                              event.severity === 'high' ? 'bg-red-500 bg-opacity-20 text-red-500' :
                              event.severity === 'medium' ? 'bg-yellow-500 bg-opacity-20 text-yellow-500' :
                              'bg-blue-500 bg-opacity-20 text-blue-500'
                            }`}>
                              {event.severity}
                            </span>
                            {isAttentionEvent && (
                              <span className="text-xs px-2 py-1 rounded-full text-purple-400" style={{ backgroundColor: 'rgba(168, 85, 247, 0.2)' }}>
                                Attention
                              </span>
                            )}
                            {isDrivingEvent && (
                              <span className="text-xs px-2 py-1 rounded-full" style={{ backgroundColor: 'rgba(56, 182, 255, 0.2)', color: '#38b6ff' }}>
                                Driving
                              </span>
                            )}
                          </div>
                          <p className="text-sm" style={{ color: '#a0a0a0' }}>
                            {new Date(event.timestamp).toLocaleString()}
                          </p>
                        </div>
                        {isDrivingEvent && (event.x !== 0 || event.y !== 0 || event.z !== 0) && (
                          <div className="text-right text-sm" style={{ color: '#a0a0a0' }}>
                            <p>X: {event.x.toFixed(2)}</p>
                            <p>Y: {event.y.toFixed(2)}</p>
                            <p>Z: {event.z.toFixed(2)}</p>
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              </motion.div>
            )}
          </>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="rounded-2xl shadow-lg p-12 text-center" style={{ backgroundColor: '#1a1f2e', border: '1px solid #2a2f3e' }}
          >
            <Activity className="w-16 h-16 mx-auto mb-4" style={{ color: '#a0a0a0' }} />
            <h3 className="text-2xl font-bold text-white mb-2">No Active Session</h3>
            <p className="mb-6" style={{ color: '#a0a0a0' }}>
              This driver doesn't have an active driving session right now.
            </p>
            <p className="text-sm" style={{ color: '#a0a0a0' }}>
              Start the Arduino and run <code className="px-2 py-1 rounded" style={{ backgroundColor: '#12161e', color: '#38b6ff' }}>ble_supabase.py</code> to begin monitoring.
            </p>
          </motion.div>
        )}
      </main>
    </div>
  )
}

export default DriverDetail
