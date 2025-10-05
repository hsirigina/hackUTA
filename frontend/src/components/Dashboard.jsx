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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 backdrop-blur-lg bg-white/80">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <Car className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Fleet Dashboard
                </h1>
                <p className="text-sm text-gray-500">Monitor your drivers in real-time</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors relative"
              >
                <Bell className="w-5 h-5 text-gray-600" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <Settings className="w-5 h-5 text-gray-600" />
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <LogOut className="w-5 h-5 text-gray-600" />
              </motion.button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Supervisor Info Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-100"
        >
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center text-white text-2xl font-bold shadow-lg">
              {supervisor.avatar}
            </div>
            <div className="flex-1">
              <h2 className="text-3xl font-bold text-gray-900 mb-1">{supervisor.name}</h2>
              <div className="flex items-center gap-4 text-gray-600">
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
              <div className="text-center px-6 py-3 bg-blue-50 rounded-xl">
                <div className="text-2xl font-bold text-blue-600">{drivers.length}</div>
                <div className="text-sm text-gray-600">Total Drivers</div>
              </div>
              <div className="text-center px-6 py-3 bg-green-50 rounded-xl">
                <div className="text-2xl font-bold text-green-600">
                  {drivers.filter(d => d.status === 'active').length}
                </div>
                <div className="text-sm text-gray-600">Active Now</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Drivers Section */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-2xl font-bold text-gray-900">Your Drivers</h3>
            <span className="text-sm text-gray-500">Scroll to see more →</span>
          </div>
        </div>

        {/* Horizontally Scrollable Driver Cards */}
        <div className="relative">
          <div className="flex gap-6 overflow-x-auto pb-4 scrollbar-hide snap-x snap-mandatory" style={{ scrollbarWidth: 'none' }}>
            {drivers.map((driver, index) => (
              <motion.div
                key={driver.id}
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
                whileHover={{ scale: 1.02, y: -5 }}
                className="flex-shrink-0 w-80 snap-start"
              >
                <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-all duration-300 h-full">
                  {/* Driver Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-14 h-14 bg-gradient-to-br from-blue-400 to-purple-500 rounded-xl flex items-center justify-center text-white text-lg font-bold">
                        {driver.avatar}
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-900 text-lg">{driver.name}</h4>
                        <p className="text-sm text-gray-500 flex items-center gap-1">
                          <Mail className="w-3 h-3" />
                          {driver.email}
                        </p>
                      </div>
                    </div>
                    <div className={`p-2 rounded-lg ${getStatusColor(driver.status)} bg-opacity-10`}>
                      <div className={`${getStatusColor(driver.status)} text-white`}>
                        {getStatusIcon(driver.status)}
                      </div>
                    </div>
                  </div>

                  {/* Arduino ID */}
                  <div className="bg-gray-50 rounded-lg p-3 mb-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Arduino ID</span>
                      <span className="font-mono font-semibold text-gray-900">{driver.arduinoId}</span>
                    </div>
                  </div>

                  {/* Stats Grid */}
                  <div className="grid grid-cols-2 gap-3 mb-4">
                    <div className="bg-blue-50 rounded-lg p-3">
                      <div className="flex items-center gap-2 mb-1">
                        <Car className="w-4 h-4 text-blue-600" />
                        <span className="text-xs text-gray-600">Trips Today</span>
                      </div>
                      <div className="text-xl font-bold text-blue-600">{driver.tripsToday}</div>
                    </div>
                    <div className="bg-purple-50 rounded-lg p-3">
                      <div className="flex items-center gap-2 mb-1">
                        <Activity className="w-4 h-4 text-purple-600" />
                        <span className="text-xs text-gray-600">Safety Score</span>
                      </div>
                      <div className={`text-xl font-bold ${getSafetyScoreColor(driver.safetyScore)}`}>
                        {driver.safetyScore}%
                      </div>
                    </div>
                  </div>

                  {/* Last Active */}
                  <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                    <div className="flex items-center gap-2 text-sm text-gray-500">
                      <Clock className="w-4 h-4" />
                      <span>Last active: {driver.lastActive}</span>
                    </div>
                    <motion.button
                      whileHover={{ x: 5 }}
                      className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center gap-1"
                    >
                      View Details
                      <ChevronRight className="w-4 h-4" />
                    </motion.button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Scroll Indicator - Left Gradient */}
          <div className="absolute left-0 top-0 bottom-4 w-20 bg-gradient-to-r from-gray-50 to-transparent pointer-events-none"></div>

          {/* Scroll Indicator - Right Gradient */}
          <div className="absolute right-0 top-0 bottom-4 w-20 bg-gradient-to-l from-gray-50 to-transparent pointer-events-none"></div>
        </div>

        {/* Quick Stats Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.5 }}
          className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Trips Today</p>
                <p className="text-3xl font-bold text-gray-900">
                  {drivers.reduce((acc, d) => acc + d.tripsToday, 0)}
                </p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                <Car className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Average Safety Score</p>
                <p className="text-3xl font-bold text-gray-900">
                  {Math.round(drivers.reduce((acc, d) => acc + d.safetyScore, 0) / drivers.length)}%
                </p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                <Activity className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Active Alerts</p>
                <p className="text-3xl font-bold text-gray-900">
                  {drivers.filter(d => d.status === 'warning').length}
                </p>
              </div>
              <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center">
                <AlertCircle className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </div>
        </motion.div>
      </main>
    </div>
  )
}

export default Dashboard
