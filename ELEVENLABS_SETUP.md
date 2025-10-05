# ElevenLabs Text-to-Speech Setup Guide

This guide will help you set up ElevenLabs API for high-quality voice alerts in your driver monitoring system.

## Step 1: Get Your ElevenLabs API Key

1. Go to [ElevenLabs](https://elevenlabs.io)
2. Sign up or log in to your account
3. Navigate to your [API Keys page](https://elevenlabs.io/app/settings/api-keys)
4. Click "Create API Key" or copy your existing key

## Step 2: Add the API Key to Your Project

Open `frontend/.env` and replace `your_api_key_here` with your actual API key:

```bash
VITE_ELEVENLABS_API_KEY=sk_your_actual_api_key_here
```

## Step 3: (Optional) Choose a Different Voice

The default voice is "Rachel" (ID: `21m00Tcm4TlvDq8ikWAM`).

To use a different voice:

1. Go to [ElevenLabs Voice Library](https://elevenlabs.io/app/voice-library)
2. Browse and select a voice you like
3. Copy the Voice ID
4. Update your `.env` file:

```bash
VITE_ELEVENLABS_VOICE_ID=your_voice_id_here
```

### Recommended Voices for Alerts:
- **Rachel** (21m00Tcm4TlvDq8ikWAM) - Clear, professional female voice
- **Adam** (pNInz6obpgDQGcFmaJgB) - Deep, authoritative male voice
- **Antoni** (ErXwobaYiN019PkySvjV) - Warm, calm male voice
- **Bella** (EXAVITQu4vr4xnSDxMaL) - Energetic, friendly female voice

## Step 4: Restart Your Development Server

After adding the API key, restart your Vite dev server:

```bash
cd frontend
npm run dev
```

## How It Works

The system automatically detects if you have a valid ElevenLabs API key:
- **With ElevenLabs key**: Uses high-quality, realistic AI voices
- **Without key**: Falls back to free browser Text-to-Speech (Web Speech API)

If ElevenLabs API fails for any reason (network issues, quota exceeded, etc.), it automatically falls back to Web Speech API.

## Pricing

ElevenLabs offers:
- **Free Tier**: 10,000 characters/month
- **Starter**: $5/month for 30,000 characters
- **Creator**: $22/month for 100,000 characters

For reference:
- Average alert message: ~100 characters
- 10,000 characters = ~100 alerts/month

## Testing

Once configured, alerts will trigger when:
1. Driver shows drowsiness or eyes closed
2. High-severity driving events occur (harsh braking, swerving, etc.)
3. Driver status changes to "Critical" or "Warning"

Navigate to the Driver Detail page and wait for events to trigger alerts, or test by manually triggering events through the monitoring system.

## Troubleshooting

**Alerts not using ElevenLabs?**
- Check that your API key is correct in `.env`
- Make sure you've restarted the dev server
- Check browser console for errors

**API quota exceeded?**
- Monitor your usage at [ElevenLabs Dashboard](https://elevenlabs.io/app/usage)
- System will automatically fall back to Web Speech API

**No sound at all?**
- Check browser permissions for audio
- Ensure volume is not muted
- Check browser console for errors
