import { motion } from 'framer-motion'

const CircularProgress = ({
  value = 0,
  size = 200,
  strokeWidth = 12,
  showPercentage = true,
  color = null // If null, auto-detect based on score
}) => {
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (value / 100) * circumference

  // Color based on score
  const getColor = () => {
    if (value >= 90) return '#10b981' // green
    if (value >= 80) return '#10b981' // green
    if (value >= 70) return '#eab308' // yellow
    return '#ef4444' // red
  }

  const progressColor = color || getColor()

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg
        width={size}
        height={size}
        className="transform -rotate-90"
      >
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#2a2f3e"
          strokeWidth={strokeWidth}
        />

        {/* Progress circle */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={progressColor}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: "easeOut" }}
        />
      </svg>

      {/* Center text */}
      {showPercentage && (
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="font-bold"
            style={{
              fontSize: size * 0.25,
              color: progressColor
            }}
          >
            {Math.round(value)}%
          </motion.span>
          <span
            className="text-sm mt-1"
            style={{
              color: '#a0a0a0',
              fontSize: size * 0.08
            }}
          >
            Safety Score
          </span>
        </div>
      )}
    </div>
  )
}

export default CircularProgress
