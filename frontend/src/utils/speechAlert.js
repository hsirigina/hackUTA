/**
 * Speech Alert System
 * Provides verbal warnings for critical driving events
 */

class SpeechAlertService {
  constructor() {
    this.synth = window.speechSynthesis
    this.lastAlertTime = {}
    this.alertCooldown = 10000 // 10 seconds between same alert types
    this.useElevenLabs = !!import.meta.env.VITE_ELEVENLABS_API_KEY && import.meta.env.VITE_ELEVENLABS_API_KEY !== 'your_api_key_here'
    this.elevenLabsApiKey = import.meta.env.VITE_ELEVENLABS_API_KEY
    this.elevenLabsVoiceId = import.meta.env.VITE_ELEVENLABS_VOICE_ID || '21m00Tcm4TlvDq8ikWAM' // Rachel voice
  }

  /**
   * Speak a message using either ElevenLabs or Web Speech API
   * @param {string} message - The message to speak
   * @param {Object} options - Voice options (rate, pitch, volume)
   */
  async speak(message, options = {}) {
    if (this.useElevenLabs) {
      await this.speakWithElevenLabs(message)
    } else {
      this.speakWithWebSpeech(message, options)
    }
  }

  /**
   * Speak using Web Speech API (TTS) - Free, built-in
   */
  speakWithWebSpeech(message, options = {}) {
    if (!this.synth) {
      console.error('Speech synthesis not supported')
      return
    }

    // Cancel any ongoing speech
    this.synth.cancel()

    const utterance = new SpeechSynthesisUtterance(message)

    // Configure voice settings
    utterance.rate = options.rate || 1.1 // Slightly faster for urgency
    utterance.pitch = options.pitch || 1.0
    utterance.volume = options.volume || 1.0
    utterance.lang = 'en-US'

    // Try to use a clear, authoritative voice
    const voices = this.synth.getVoices()
    const preferredVoice = voices.find(voice =>
      voice.name.includes('Samantha') ||
      voice.name.includes('Google US English') ||
      voice.name.includes('Microsoft David')
    )
    if (preferredVoice) {
      utterance.voice = preferredVoice
    }

    this.synth.speak(utterance)
  }

  /**
   * Check if enough time has passed since last alert of this type
   */
  canAlert(alertType) {
    const now = Date.now()
    const lastTime = this.lastAlertTime[alertType] || 0

    if (now - lastTime < this.alertCooldown) {
      return false
    }

    this.lastAlertTime[alertType] = now
    return true
  }

  /**
   * Alert for critical driving behavior
   */
  alertCritical(driverName, issue) {
    if (!this.canAlert('critical')) return

    const messages = [
      `Critical alert! ${driverName} is driving dangerously. Immediate intervention required.`,
      `Warning! Unsafe driving detected. ${issue}. Pull over immediately.`,
      `Danger! Critical safety violation. ${driverName} must stop driving now.`
    ]

    const message = messages[Math.floor(Math.random() * messages.length)]
    this.speak(message, { rate: 1.2, volume: 1.0 })
  }

  /**
   * Alert for specific dangerous events
   */
  alertDangerousEvent(eventType, driverName) {
    if (!this.canAlert(eventType)) return

    let message = ''

    switch(eventType) {
      case 'DROWSY':
      case 'EYES_CLOSED':
        message = `Alert! ${driverName} is showing signs of drowsiness. Pull over immediately and rest.`
        break
      case 'HARSH_BRAKE':
        message = `Warning! Harsh braking detected for ${driverName}. Maintain safe following distance.`
        break
      case 'SWERVING':
        message = `Alert! Erratic steering detected. ${driverName}, focus on the road.`
        break
      case 'AGGRESSIVE':
        message = `Warning! Aggressive driving detected. ${driverName}, reduce speed and drive safely.`
        break
      case 'DISTRACTED':
        message = `Attention! ${driverName} appears distracted. Keep eyes on the road.`
        break
      default:
        message = `Safety alert for ${driverName}. Please drive carefully.`
    }

    this.speak(message, { rate: 1.1 })
  }

  /**
   * Alert for warning status
   */
  alertWarning(driverName, issues) {
    if (!this.canAlert('warning')) return

    const message = `Attention! ${driverName} is showing concerning driving patterns. Monitor closely.`
    this.speak(message, { rate: 1.0 })
  }

  /**
   * Stop any ongoing speech
   */
  stop() {
    if (this.synth) {
      this.synth.cancel()
    }
  }

  /**
   * Speak using ElevenLabs API - High quality, realistic voices
   */
  async speakWithElevenLabs(message) {
    try {
      const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${this.elevenLabsVoiceId}`, {
        method: 'POST',
        headers: {
          'Accept': 'audio/mpeg',
          'Content-Type': 'application/json',
          'xi-api-key': this.elevenLabsApiKey
        },
        body: JSON.stringify({
          text: message,
          model_id: 'eleven_monolingual_v1',
          voice_settings: {
            stability: 0.6,
            similarity_boost: 0.8,
            style: 0.3,
            use_speaker_boost: true
          }
        })
      })

      if (!response.ok) {
        console.error('ElevenLabs API error:', response.statusText)
        // Fallback to Web Speech API
        this.speakWithWebSpeech(message, { rate: 1.1 })
        return
      }

      const audioBlob = await response.blob()
      const audioUrl = URL.createObjectURL(audioBlob)
      const audio = new Audio(audioUrl)

      // Play the audio
      await audio.play()

      // Clean up the blob URL after playing
      audio.addEventListener('ended', () => {
        URL.revokeObjectURL(audioUrl)
      })

    } catch (error) {
      console.error('ElevenLabs error:', error)
      // Fallback to Web Speech API
      this.speakWithWebSpeech(message, { rate: 1.1 })
    }
  }
}

// Export singleton instance
export const speechAlert = new SpeechAlertService()
