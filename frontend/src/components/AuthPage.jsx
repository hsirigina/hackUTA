import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Mail, Lock, User, Eye, EyeOff, ArrowRight, Sparkles, Shield, Zap } from 'lucide-react'
import { supabase } from '../lib/supabase'
import { Squares } from './ui/squares-background'

const AuthPage = () => {
  const navigate = useNavigate()
  const [isLogin, setIsLogin] = useState(true)
  const [showPassword, setShowPassword] = useState(false)
  const [typewriterText, setTypewriterText] = useState('PARKER')
  const [showCursor, setShowCursor] = useState(false)
  const [descriptionText, setDescriptionText] = useState('')
  const [showDescriptionCursor, setShowDescriptionCursor] = useState(true)
  const [currentDescriptionIndex, setCurrentDescriptionIndex] = useState(0)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    fullName: ''
  })
  const [message, setMessage] = useState({ type: '', text: '' })

  // Rotating descriptions
  const descriptions = [
    'AI-Powered Driver Monitoring System',
    'Real-time Attention Detection',
    'Smart Driving Behavior Analysis',
    'Advanced Safety Monitoring',
    'Intelligent Alert System',
    'Next-Gen Driver Assistance'
  ]

  useEffect(() => {
    let typeInterval
    let timeoutId
    
    const rotateDescriptions = () => {
      const description = descriptions[currentDescriptionIndex]
      let index = 0
      
      // Clear current text first
      setDescriptionText('')
      
      typeInterval = setInterval(() => {
        if (index < description.length) {
          setDescriptionText(description.slice(0, index + 1))
          index++
        } else {
          clearInterval(typeInterval)
          // Wait 3 seconds then move to next description
          timeoutId = setTimeout(() => {
            setCurrentDescriptionIndex((prev) => (prev + 1) % descriptions.length)
          }, 3000)
        }
      }, 100)
    }

    rotateDescriptions()
    
    // Cleanup function
    return () => {
      if (typeInterval) clearInterval(typeInterval)
      if (timeoutId) clearTimeout(timeoutId)
    }
  }, [currentDescriptionIndex])

  // Cursor blinking effect
  useEffect(() => {
    const cursorInterval = setInterval(() => {
      setShowDescriptionCursor(prev => !prev)
    }, 500)

    return () => clearInterval(cursorInterval)
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage({ type: '', text: '' })

    try {
      if (isLogin) {
        const { data, error } = await supabase.auth.signInWithPassword({
          email: formData.email,
          password: formData.password,
        })
        if (error) throw error
        setMessage({ type: 'success', text: 'Welcome back! Redirecting...' })
        setTimeout(() => navigate('/dashboard'), 1000)
      } else {
        const { data, error } = await supabase.auth.signUp({
          email: formData.email,
          password: formData.password,
          options: {
            data: {
              full_name: formData.fullName,
            }
          }
        })
        if (error) throw error
        setMessage({ type: 'success', text: 'Account created! Please check your email to verify.' })
      }
    } catch (error) {
      setMessage({ type: 'error', text: error.message })
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const features = [
    { icon: Shield, text: 'Secure & encrypted', color: 'from-blue-500 to-cyan-500' },
    { icon: Zap, text: 'Lightning fast', color: 'from-purple-500 to-pink-500' },
    { icon: Sparkles, text: 'Modern experience', color: 'from-orange-500 to-red-500' }
  ]

  return (
    <div className="min-h-screen flex overflow-hidden">
      {/* Left Panel - Decorative */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-[#060606]">
        <Squares 
          direction="diagonal"
          speed={0.5}
          squareSize={40}
          borderColor="#333" 
          hoverFillColor="#444"
        />

        {/* Welcome Text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center w-full p-12 text-white pointer-events-none">
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2, duration: 0.8 }}
            className="text-center"
          >
            <h2 className="text-5xl font-bold mb-6" style={{ 
              fontFamily: 'Impact, "Arial Black", sans-serif', 
              textShadow: '3px 3px 6px rgba(0,0,0,0.8), 0 0 10px rgba(255,255,255,0.3)', 
              letterSpacing: '3px',
              textTransform: 'uppercase',
              fontWeight: '900'
            }}>
              {typewriterText}
            </h2>
            
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="text-lg font-mono text-gray-300"
              style={{ 
                textShadow: '1px 1px 2px rgba(0,0,0,0.8)',
                letterSpacing: '1px'
              }}
            >
              {descriptionText}<span style={{ opacity: showDescriptionCursor ? 1 : 0 }}>|</span>
            </motion.div>
          </motion.div>
        </div>
      </div>

      {/* Right Panel - Auth Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-gray-100 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-md"
        >
          {/* Logo/Brand */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-semibold" style={{ color: '#0C1E8B', fontFamily: 'Inter, system-ui, sans-serif' }}>
              Welcome to <span style={{ 
                fontFamily: 'Impact, "Arial Black", sans-serif',
                letterSpacing: '2px',
                textTransform: 'uppercase'
              }}>PARKER</span>
            </h1>
            <p className="text-gray-700 mt-2" style={{ fontFamily: 'Inter, system-ui, sans-serif' }}>
              {isLogin ? 'Sign in to continue your journey' : 'Create your account to get started'}
            </p>
          </div>

          {/* Tab Switcher */}
          <div className="flex gap-2 mb-8 p-1 bg-gray-200 rounded-xl">
            <button
              onClick={() => setIsLogin(true)}
              className={`flex-1 py-3 rounded-lg font-medium transition-all duration-300 ${
                isLogin
                  ? 'shadow-md'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              style={isLogin ? { color: '#0C1E8B', backgroundColor: 'white', fontFamily: 'Inter, system-ui, sans-serif' } : { fontFamily: 'Inter, system-ui, sans-serif' }}
            >
              Sign In
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`flex-1 py-3 rounded-lg font-medium transition-all duration-300 ${
                !isLogin
                  ? 'shadow-md'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              style={!isLogin ? { color: '#0C1E8B', backgroundColor: 'white', fontFamily: 'Inter, system-ui, sans-serif' } : { fontFamily: 'Inter, system-ui, sans-serif' }}
            >
              Sign Up
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            <AnimatePresence mode="wait">
              {!isLogin && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name
                  </label>
                  <div className="relative">
                    <User className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="text"
                      name="fullName"
                      value={formData.fullName}
                      onChange={handleChange}
                      className="w-full pl-12 pr-4 py-3 bg-white rounded-xl focus:outline-none transition-colors text-gray-900 placeholder-gray-500" style={{ fontFamily: 'Inter, system-ui, sans-serif' }}
                      placeholder="John Doe"
                      required={!isLogin}
                    />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                    className="w-full pl-12 pr-4 py-3 bg-white rounded-xl focus:outline-none transition-colors text-gray-900 placeholder-gray-500" style={{ fontFamily: 'Inter, system-ui, sans-serif' }}
                  placeholder="you@example.com"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full pl-12 pr-12 py-3 bg-white rounded-xl focus:outline-none transition-colors text-gray-900 placeholder-gray-500" style={{ fontFamily: 'Inter, system-ui, sans-serif' }}
                  placeholder="••••••••"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {isLogin && (
              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center">
                  <input type="checkbox" className="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 bg-white" />
                  <span className="ml-2 text-gray-700">Remember me</span>
                </label>
                <a href="#" className="font-medium" style={{ color: '#DA261C' }}>
                  Forgot password?
                </a>
              </div>
            )}

            {/* Message Display */}
            <AnimatePresence>
              {message.text && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className={`p-4 rounded-xl ${
                    message.type === 'success'
                      ? 'bg-green-50 text-green-700 border border-green-200'
                      : 'bg-blue-50 text-blue-700 border border-blue-200'
                  }`}
                >
                  {message.text}
                </motion.div>
              )}
            </AnimatePresence>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              disabled={loading}
              className="w-full text-white py-3 rounded-xl font-medium shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ backgroundColor: '#0C1E8B', fontFamily: 'Inter, system-ui, sans-serif' }}
            >
              {loading ? (
                <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <>
                  {isLogin ? 'Sign In' : 'Create Account'}
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </motion.button>
          </form>

          {/* Divider */}
          <div className="my-8 flex items-center">
            <div className="flex-1 border-t border-gray-300"></div>
            <span className="px-4 text-sm text-gray-500">or continue with</span>
            <div className="flex-1 border-t border-gray-300"></div>
          </div>

          {/* Social Login */}
          <div className="grid grid-cols-3 gap-3">
            {['Google', 'GitHub', 'Apple'].map((provider) => (
              <motion.button
                key={provider}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="py-3 px-4 rounded-xl transition-colors font-medium text-gray-700 bg-white" style={{ fontFamily: 'Inter, system-ui, sans-serif' }}
              >
                {provider}
              </motion.button>
            ))}
          </div>
        </motion.div>
      </div>

    </div>
  )
}

export default AuthPage
