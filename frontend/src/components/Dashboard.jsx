import { useState } from 'react'
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
  Settings
} from 'lucide-react'

const Dashboard = () => {
  // Mock supervisor data
  const supervisor = {
    name: 'Sarah Johnson',
    email: 'sarah.johnson@company.com',
    role: 'Fleet Supervisor',
    avatar: 'SJ'
  }

  // Mock drivers data with Arduino associations
  const drivers = [
    {
      id: 1,
      name: 'Michael Chen',
      email: 'mchen@company.com',
      arduinoId: 'ARD-001',
      status: 'active',
      lastActive: '2 mins ago',
      tripsToday: 5,
      safetyScore: 95,
      avatar: 'MC'
    },
    {
      id: 2,
      name: 'Emily Rodriguez',
      email: 'erodriguez@company.com',
      arduinoId: 'ARD-002',
      status: 'active',
      lastActive: '5 mins ago',
      tripsToday: 3,
      safetyScore: 88,
      avatar: 'ER'
    },
    {
      id: 3,
      name: 'James Wilson',
      email: 'jwilson@company.com',
      arduinoId: 'ARD-003',
      status: 'inactive',
      lastActive: '1 hour ago',
      tripsToday: 7,
      safetyScore: 92,
      avatar: 'JW'
    },
    {
      id: 4,
      name: 'Aisha Patel',
      email: 'apatel@company.com',
      arduinoId: 'ARD-004',
      status: 'warning',
      lastActive: 'Just now',
      tripsToday: 4,
      safetyScore: 76,
      avatar: 'AP'
    },
    {
      id: 5,
      name: 'David Kim',
      email: 'dkim@company.com',
      arduinoId: 'ARD-005',
      status: 'active',
      lastActive: '10 mins ago',
      tripsToday: 6,
      safetyScore: 98,
      avatar: 'DK'
    },
    {
      id: 6,
      name: 'Sofia Martinez',
      email: 'smartinez@company.com',
      arduinoId: 'ARD-006',
      status: 'active',
      lastActive: '3 mins ago',
      tripsToday: 2,
      safetyScore: 91,
      avatar: 'SM'
    }
  ]

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
                className="p-2 rounded-lg transition-colors relative"
                style={{ backgroundColor: '#1a1f2e' }}
              >
                <Bell className="w-5 h-5 text-white" />
                <span className="absolute top-1 right-1 w-2 h-2 rounded-full" style={{ backgroundColor: '#38b6ff' }}></span>
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 rounded-lg transition-colors"
                style={{ backgroundColor: '#1a1f2e' }}
              >
                <Settings className="w-5 h-5 text-white" />
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 rounded-lg transition-colors"
                style={{ backgroundColor: '#1a1f2e' }}
              >
                <LogOut className="w-5 h-5 text-white" />
              </motion.button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-6" style={{ overflow: 'visible' }}>
        {/* Supervisor Info Card */}
        <div
          className="rounded-xl p-6 mb-8"
          style={{ 
            backgroundColor: '#1a1f2e',
            border: '2px solid #38b6ff',
            boxShadow: '0 0 20px rgba(56, 182, 255, 0.3)'
          }}
        >
          <div className="flex items-center gap-6">
            <div className="w-16 h-16 rounded-lg flex items-center justify-center text-white text-xl font-bold" style={{ backgroundColor: '#38b6ff' }}>
              {supervisor.avatar}
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold mb-1" style={{ 
                color: '#ffffff',
                fontFamily: 'Fira Code, monospace',
                letterSpacing: '1px',
                textTransform: 'lowercase',
                fontWeight: '700'
              }}>{supervisor.name}</h2>
              <div className="flex items-center gap-4" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  <span>{supervisor.email}</span>
                </div>
                <div className="flex items-center gap-2">
                  <User className="w-4 h-4" />
                  <span>{supervisor.role}</span>
                </div>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="text-center px-4 py-2 rounded-lg" style={{ 
                backgroundColor: '#12161e',
                border: '1px solid #38b6ff',
                boxShadow: '0 0 10px rgba(56, 182, 255, 0.2)'
              }}>
                <div className="text-xl font-bold" style={{ color: '#38b6ff' }}>{drivers.length}</div>
                <div className="text-xs" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>Total Drivers</div>
              </div>
              <div className="text-center px-4 py-2 rounded-lg" style={{ 
                backgroundColor: '#12161e',
                border: '1px solid #38b6ff',
                boxShadow: '0 0 10px rgba(56, 182, 255, 0.2)'
              }}>
                <div className="text-xl font-bold" style={{ color: '#38b6ff' }}>
                  {drivers.filter(d => d.status === 'active').length}
                </div>
                <div className="text-xs" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>Active Now</div>
              </div>
            </div>
          </div>
        </div>

        {/* Drivers Section */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold" style={{ 
              color: '#ffffff',
              fontFamily: 'Orbitron, monospace',
              textShadow: '0 0 1px #ffffff, 0 0 3px #38b6ff, 0 0 6px #38b6ff',
              letterSpacing: '1px',
              textTransform: 'uppercase',
              fontWeight: '700'
            }}>YOUR DRIVERS</h3>
            <span className="text-sm" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>Scroll to see more →</span>
          </div>
        </div>

        {/* Horizontally Scrollable Driver Cards */}
        <div className="relative" style={{ zIndex: 10, overflow: 'visible' }}>
          <div className="flex gap-6 overflow-x-auto scrollbar-hide snap-x snap-mandatory" style={{ scrollbarWidth: 'none', overflowY: 'visible', paddingBottom: '2rem' }}>
            {drivers.map((driver, index) => (
              <motion.div
                key={driver.id}
                whileHover={{ 
                  scale: 1.05, 
                  y: -10, 
                  rotateY: 5,
                  boxShadow: '0 0 40px rgba(56, 182, 255, 0.6)',
                  transition: { duration: 0.2 }
                }}
                className="flex-shrink-0 w-80 snap-start relative"
                style={{ zIndex: 1 }}
              >
                <div className="rounded-xl p-4 transition-all duration-300 h-full" style={{ 
                  backgroundColor: '#1a1f2e',
                  border: '2px solid #38b6ff',
                  boxShadow: '0 0 20px rgba(56, 182, 255, 0.3)'
                }}>
                  {/* Driver Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-lg flex items-center justify-center text-white text-sm font-bold" style={{ backgroundColor: '#38b6ff' }}>
                        {driver.avatar}
                      </div>
                      <div>
                        <h4 className="font-semibold" style={{ 
                          color: '#ffffff',
                          fontFamily: 'Fira Code, monospace',
                          letterSpacing: '0.5px',
                          textTransform: 'lowercase',
                          fontWeight: '700'
                        }}>{driver.name}</h4>
                        <p className="text-xs flex items-center gap-1" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>
                          <Mail className="w-3 h-3" />
                          {driver.email}
                        </p>
                      </div>
                    </div>
                    <div className="p-1 rounded" style={{ backgroundColor: '#38b6ff' }}>
                      <div className="text-white">
                        {getStatusIcon(driver.status)}
                      </div>
                    </div>
                  </div>

                  {/* Arduino ID */}
                  <div className="rounded-lg p-2 mb-3" style={{ 
                    backgroundColor: '#12161e',
                    border: '1px solid #38b6ff',
                    boxShadow: '0 0 10px rgba(56, 182, 255, 0.2)'
                  }}>
                    <div className="flex items-center justify-between">
                      <span className="text-xs" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>Arduino ID</span>
                      <span className="font-mono text-sm font-semibold" style={{ color: '#38b6ff' }}>{driver.arduinoId}</span>
                    </div>
                  </div>

                  {/* Stats Grid */}
                  <div className="grid grid-cols-2 gap-2 mb-3">
                    <div className="rounded-lg p-2" style={{ 
                      backgroundColor: '#12161e',
                      border: '1px solid #38b6ff',
                      boxShadow: '0 0 10px rgba(56, 182, 255, 0.2)'
                    }}>
                      <div className="flex items-center gap-1 mb-1">
                        <Car className="w-3 h-3" style={{ color: '#38b6ff' }} />
                        <span className="text-xs" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>Trips</span>
                      </div>
                      <div className="text-lg font-bold" style={{ color: '#38b6ff' }}>{driver.tripsToday}</div>
                    </div>
                    <div className="rounded-lg p-2" style={{ 
                      backgroundColor: '#12161e',
                      border: '1px solid #38b6ff',
                      boxShadow: '0 0 10px rgba(56, 182, 255, 0.2)'
                    }}>
                      <div className="flex items-center gap-1 mb-1">
                        <Activity className="w-3 h-3" style={{ color: '#38b6ff' }} />
                        <span className="text-xs" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>Safety</span>
                      </div>
                      <div className="text-lg font-bold" style={{ color: '#38b6ff' }}>
                        {driver.safetyScore}%
                      </div>
                    </div>
                  </div>

                  {/* Last Active */}
                  <div className="flex items-center justify-between pt-2" style={{ borderTop: '1px solid #38b6ff' }}>
                    <div className="flex items-center gap-1 text-xs" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>
                      <Clock className="w-3 h-3" />
                      <span>{driver.lastActive}</span>
                    </div>
                    <motion.button
                      whileHover={{ x: 2 }}
                      className="text-xs flex items-center gap-1"
                      style={{ color: '#38b6ff' }}
                    >
                      View
                      <ChevronRight className="w-3 h-3" />
                    </motion.button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Scroll Indicator - Left Gradient */}
          <div className="absolute left-0 top-0 bottom-4 w-20 pointer-events-none" style={{ background: 'linear-gradient(to right, #12161e, transparent)' }}></div>

          {/* Scroll Indicator - Right Gradient */}
          <div className="absolute right-0 top-0 bottom-4 w-20 pointer-events-none" style={{ background: 'linear-gradient(to left, #12161e, transparent)' }}></div>
        </div>

        {/* Quick Stats Section */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div 
            className="rounded-xl p-4" 
            style={{ 
              backgroundColor: '#12161e',
              border: '2px solid #38b6ff',
              boxShadow: '0 0 20px rgba(56, 182, 255, 0.3)'
            }}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs mb-1" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>Total Trips Today</p>
                <p className="text-2xl font-bold" style={{ color: '#38b6ff' }}>
                  {drivers.reduce((acc, d) => acc + d.tripsToday, 0)}
                </p>
              </div>
              <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#38b6ff' }}>
                <Car className="w-5 h-5 text-white" />
              </div>
            </div>
          </div>

          <div 
            className="rounded-xl p-4" 
            style={{ 
              backgroundColor: '#12161e',
              border: '2px solid #38b6ff',
              boxShadow: '0 0 20px rgba(56, 182, 255, 0.3)'
            }}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs mb-1" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>Average Safety Score</p>
                <p className="text-2xl font-bold" style={{ color: '#38b6ff' }}>
                  {Math.round(drivers.reduce((acc, d) => acc + d.safetyScore, 0) / drivers.length)}%
                </p>
              </div>
              <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#38b6ff' }}>
                <Activity className="w-5 h-5 text-white" />
              </div>
            </div>
          </div>

          <div 
            className="rounded-xl p-4" 
            style={{ 
              backgroundColor: '#12161e',
              border: '2px solid #38b6ff',
              boxShadow: '0 0 20px rgba(56, 182, 255, 0.3)'
            }}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs mb-1" style={{ color: '#ffffff', fontFamily: 'Fira Code, monospace' }}>Active Alerts</p>
                <p className="text-2xl font-bold" style={{ color: '#38b6ff' }}>
                  {drivers.filter(d => d.status === 'warning').length}
                </p>
              </div>
              <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#38b6ff' }}>
                <AlertCircle className="w-5 h-5 text-white" />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Dashboard
