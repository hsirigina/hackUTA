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
  const [typewriterText, setTypewriterText] = useState('DASH')
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

        // Check if supervisor entry exists, create if not
        await ensureSupervisorExists(data.user)

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

        // Create supervisor entry for new user
        if (data.user) {
          await ensureSupervisorExists(data.user, formData.fullName)
        }

        setMessage({ type: 'success', text: 'Account created! You can now sign in.' })
      }
    } catch (error) {
      setMessage({ type: 'error', text: error.message })
    } finally {
      setLoading(false)
    }
  }

  const ensureSupervisorExists = async (user, fullName = null) => {
    try {
      // Check if supervisor exists
      const { data: existingSupervisor } = await supabase
        .from('supervisors')
        .select('*')
        .eq('user_id', user.id)
        .single()

      if (!existingSupervisor) {
        // Create supervisor entry
        const name = fullName || user.user_metadata?.full_name || user.email.split('@')[0]
        await supabase
          .from('supervisors')
          .insert({
            user_id: user.id,
            name: name,
            email: user.email,
            role: 'Fleet Supervisor'
          })
      }
    } catch (error) {
      console.error('Error ensuring supervisor exists:', error)
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
    <div className="min-h-screen flex overflow-hidden" style={{ backgroundColor: '#030624' }}>
      {/* Left Panel - Decorative */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden" style={{ backgroundColor: '#030624' }}>
        <Squares 
          direction="diagonal"
          speed={0.5}
          squareSize={40}
          borderColor="#333" 
          hoverFillColor="#222"
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
              fontFamily: 'Orbitron, monospace', 
              color: '#ffffff',
              letterSpacing: '3px',
              textTransform: 'uppercase',
              fontWeight: '900',
              textShadow: '0 0 2px #ffffff, 0 0 4px #38b6ff, 0 0 8px #38b6ff'
            }}>
              {typewriterText}
            </h2>
            
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="text-lg"
              style={{ 
                color: '#ffffff',
                letterSpacing: '1px',
                fontFamily: 'Fira Code, monospace',
                textTransform: 'lowercase'
              }}
            >
              {descriptionText}<span style={{ opacity: showDescriptionCursor ? 1 : 0 }}>|</span>
            </motion.div>
          </motion.div>
        </div>
      </div>

      {/* Right Panel - Auth Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 relative z-10" style={{ backgroundColor: '#12161e' }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-md"
        >
          {/* Logo/Brand */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-semibold" style={{
              color: '#38b6ff',
              fontFamily: 'Orbitron, monospace',
              fontWeight: '900',
              letterSpacing: '2px',
              textTransform: 'uppercase',
              textShadow: '0 0 2px #ffffff, 0 0 4px #38b6ff, 0 0 8px #38b6ff'
            }}>
              Welcome to <span style={{
                fontFamily: 'Orbitron, monospace',
                letterSpacing: '2px',
                textTransform: 'uppercase',
                fontWeight: '900'
              }}>DASH</span>
            </h1>
            <p className="mt-2" style={{
              color: '#a0a0a0',
              fontFamily: 'Fira Code, monospace',
              textTransform: 'lowercase'
            }}>
              {isLogin ? 'sign in to continue your journey' : 'create your account to get started'}
            </p>
          </div>

          {/* Tab Switcher */}
          <div className="flex gap-2 mb-8 p-1 rounded-xl" style={{ 
            backgroundColor: '#1a1f2e',
            border: '2px solid #38b6ff',
            boxShadow: '0 0 20px rgba(56, 182, 255, 0.3)'
          }}>
            <button
              onClick={() => setIsLogin(true)}
              className={`flex-1 py-3 rounded-lg font-medium transition-all duration-300 ${
                isLogin
                  ? ''
                  : 'hover:opacity-80'
              }`}
              style={isLogin ? { 
                color: '#38b6ff', 
                backgroundColor: '#12161e', 
                fontFamily: 'Fira Code, monospace',
                textTransform: 'lowercase',
                fontWeight: '700'
              } : { 
                color: '#888888', 
                fontFamily: 'Fira Code, monospace',
                textTransform: 'lowercase'
              }}
            >
              sign in
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`flex-1 py-3 rounded-lg font-medium transition-all duration-300 ${
                !isLogin
                  ? ''
                  : 'hover:opacity-80'
              }`}
              style={!isLogin ? { 
                color: '#38b6ff', 
                backgroundColor: '#12161e', 
                fontFamily: 'Fira Code, monospace',
                textTransform: 'lowercase',
                fontWeight: '700'
              } : { 
                color: '#888888', 
                fontFamily: 'Fira Code, monospace',
                textTransform: 'lowercase'
              }}
            >
              sign up
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
                  <label className="block text-sm font-medium mb-2" style={{
                    color: '#ffffff',
                    fontFamily: 'Fira Code, monospace',
                    textTransform: 'lowercase'
                  }}>
                    full name
                  </label>
                  <div className="relative">
                    <User className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5" style={{ color: '#38b6ff' }} />
                    <input
                      type="text"
                      name="fullName"
                      value={formData.fullName}
                      onChange={handleChange}
                      className="w-full pl-12 pr-4 py-3 rounded-xl focus:outline-none transition-colors" 
                      style={{ 
                        backgroundColor: '#ffffff', 
                        color: '#12161e', 
                        fontFamily: 'Fira Code, monospace',
                        border: '2px solid #38b6ff',
                        boxShadow: '0 0 10px rgba(56, 182, 255, 0.2)'
                      }}
                      placeholder="john doe"
                      required={!isLogin}
                    />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <div>
              <label className="block text-sm font-medium mb-2" style={{
                color: '#ffffff',
                fontFamily: 'Fira Code, monospace',
                textTransform: 'lowercase'
              }}>
                email address
              </label>
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5" style={{ color: '#38b6ff' }} />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full pl-12 pr-4 py-3 rounded-xl focus:outline-none transition-colors" 
                  style={{ 
                    backgroundColor: '#ffffff', 
                    color: '#12161e', 
                    fontFamily: 'Fira Code, monospace',
                    border: '2px solid #38b6ff',
                    boxShadow: '0 0 10px rgba(56, 182, 255, 0.2)'
                  }}
                  placeholder="you@example.com"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2" style={{
                color: '#ffffff',
                fontFamily: 'Fira Code, monospace',
                textTransform: 'lowercase'
              }}>
                password
              </label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5" style={{ color: '#38b6ff' }} />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full pl-12 pr-12 py-3 rounded-xl focus:outline-none transition-colors" 
                  style={{ 
                    backgroundColor: '#ffffff', 
                    color: '#12161e', 
                    fontFamily: 'Fira Code, monospace',
                    border: '2px solid #38b6ff',
                    boxShadow: '0 0 10px rgba(56, 182, 255, 0.2)'
                  }}
                  placeholder="••••••••"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 hover:opacity-80"
                  style={{ color: '#38b6ff' }}
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {isLogin && (
              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center">
                  <input type="checkbox" className="w-4 h-4 rounded border-2 focus:ring-2 bg-white" style={{ borderColor: '#38b6ff', accentColor: '#38b6ff' }} />
                  <span className="ml-2" style={{
                    color: '#ffffff',
                    fontFamily: 'Fira Code, monospace',
                    textTransform: 'lowercase'
                  }}>remember me</span>
                </label>
                <a href="#" className="font-medium hover:opacity-80" style={{
                  color: '#38b6ff',
                  fontFamily: 'Fira Code, monospace',
                  textTransform: 'lowercase'
                }}>
                  forgot password?
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
                  className="p-4 rounded-xl"
                  style={{
                    backgroundColor: '#ffffff',
                    color: '#12161e',
                    border: '2px solid #38b6ff',
                    boxShadow: '0 0 10px rgba(56, 182, 255, 0.2)',
                    fontFamily: 'Fira Code, monospace',
                    textTransform: 'lowercase'
                  }}
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
              className="w-full py-3 rounded-xl font-medium transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ 
                backgroundColor: '#38b6ff', 
                color: '#ffffff',
                fontFamily: 'Fira Code, monospace',
                textTransform: 'lowercase',
                fontWeight: '700',
                border: '2px solid #38b6ff',
                boxShadow: '0 0 20px rgba(56, 182, 255, 0.3)'
              }}
            >
              {loading ? (
                <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <>
                  {isLogin ? 'sign in' : 'create account'}
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </motion.button>
          </form>

          {/* Divider */}
          <div className="my-8 flex items-center">
            <div className="flex-1 border-t" style={{ borderColor: '#38b6ff' }}></div>
            <span className="px-4 text-sm" style={{
              color: '#a0a0a0',
              fontFamily: 'Fira Code, monospace',
              textTransform: 'lowercase'
            }}>or continue with</span>
            <div className="flex-1 border-t" style={{ borderColor: '#38b6ff' }}></div>
          </div>

          {/* Social Login */}
          <div className="grid grid-cols-3 gap-3">
            {['Google', 'GitHub', 'Apple'].map((provider) => (
              <motion.button
                key={provider}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="py-3 px-4 rounded-xl transition-colors font-medium"
                style={{
                  backgroundColor: '#1a1f2e',
                  color: '#ffffff',
                  fontFamily: 'Fira Code, monospace',
                  textTransform: 'lowercase',
                  border: '2px solid #38b6ff',
                  boxShadow: '0 0 10px rgba(56, 182, 255, 0.2)'
                }}
              >
                {provider.toLowerCase()}
              </motion.button>
            ))}
          </div>
        </motion.div>
      </div>

    </div>
  )
}

export default AuthPage
