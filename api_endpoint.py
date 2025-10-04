"""
API endpoint for Arduino to send driving data.
This is a simple Flask API that can run alongside Streamlit.

To run: python api_endpoint.py
"""
from flask import Flask, request, jsonify
from datetime import datetime
from database.models import db, DrivingMetric, DrivingEvent, DrivingSession
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Simple API key authentication for Arduino
API_KEY = os.getenv('ARDUINO_API_KEY', 'your_secret_api_key')


def verify_api_key():
    """Verify API key from request headers."""
    api_key = request.headers.get('X-API-Key')
    return api_key == API_KEY


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})


@app.route('/api/driving/metric', methods=['POST'])
def submit_metric():
    """
    Submit driving metrics from Arduino.

    Expected JSON payload:
    {
        "session_id": 123,
        "speed": 60.5,
        "acceleration": 2.3,
        "latitude": 32.7767,
        "longitude": -96.7970,
        "heading": 180.0,
        "rpm": 3000,
        "fuel_level": 75.5,
        "engine_temp": 90.0
    }
    """
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.json

        # Validate required fields
        if 'session_id' not in data:
            return jsonify({'error': 'session_id is required'}), 400

        # Get session to verify it exists and is active
        db_session = db.get_session()
        session = db_session.query(DrivingSession).filter_by(
            id=data['session_id'],
            is_active=True
        ).first()

        if not session:
            db_session.close()
            return jsonify({'error': 'Invalid or inactive session'}), 400

        # Create metric record
        metric = DrivingMetric(
            session_id=data['session_id'],
            timestamp=datetime.utcnow(),
            speed=data.get('speed', 0.0),
            acceleration=data.get('acceleration', 0.0),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            heading=data.get('heading'),
            rpm=data.get('rpm'),
            fuel_level=data.get('fuel_level'),
            engine_temp=data.get('engine_temp')
        )

        db_session.add(metric)

        # Update session distance if GPS data available
        if data.get('latitude') and data.get('longitude'):
            # Simple distance calculation (you'd want to use proper GPS distance in production)
            # This is a placeholder - implement haversine formula for accurate distance
            session.distance += data.get('speed', 0) / 3600  # rough estimate

        db_session.commit()
        db_session.close()

        return jsonify({
            'status': 'success',
            'metric_id': metric.id,
            'timestamp': metric.timestamp.isoformat()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/driving/event', methods=['POST'])
def submit_event():
    """
    Submit driving events from Arduino.

    Expected JSON payload:
    {
        "session_id": 123,
        "event_type": "harsh_brake",
        "severity": "high",
        "description": "Hard braking detected",
        "speed_at_event": 65.0,
        "latitude": 32.7767,
        "longitude": -96.7970
    }
    """
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.json

        # Validate required fields
        if 'session_id' not in data or 'event_type' not in data:
            return jsonify({'error': 'session_id and event_type are required'}), 400

        # Get session to verify it exists and is active
        db_session = db.get_session()
        session = db_session.query(DrivingSession).filter_by(
            id=data['session_id'],
            is_active=True
        ).first()

        if not session:
            db_session.close()
            return jsonify({'error': 'Invalid or inactive session'}), 400

        # Create event record
        event = DrivingEvent(
            session_id=data['session_id'],
            timestamp=datetime.utcnow(),
            event_type=data['event_type'],
            severity=data.get('severity', 'low'),
            description=data.get('description'),
            speed_at_event=data.get('speed_at_event'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )

        db_session.add(event)
        db_session.commit()
        db_session.close()

        return jsonify({
            'status': 'success',
            'event_id': event.id,
            'timestamp': event.timestamp.isoformat()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/session/start', methods=['POST'])
def start_session():
    """
    Start a new driving session.

    Expected JSON payload:
    {
        "driver_id": "auth0|123456789"
    }
    """
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.json

        if 'driver_id' not in data:
            return jsonify({'error': 'driver_id is required'}), 400

        db_session = db.get_session()

        # Check for existing active session
        active = db_session.query(DrivingSession).filter_by(
            driver_id=data['driver_id'],
            is_active=True
        ).first()

        if active:
            db_session.close()
            return jsonify({
                'status': 'already_active',
                'session_id': active.id
            }), 200

        # Create new session
        new_session = DrivingSession(
            driver_id=data['driver_id'],
            start_time=datetime.utcnow(),
            is_active=True
        )

        db_session.add(new_session)
        db_session.commit()

        session_id = new_session.id
        db_session.close()

        return jsonify({
            'status': 'success',
            'session_id': session_id,
            'start_time': new_session.start_time.isoformat()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/session/end', methods=['POST'])
def end_session():
    """
    End an active driving session.

    Expected JSON payload:
    {
        "session_id": 123
    }
    """
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.json

        if 'session_id' not in data:
            return jsonify({'error': 'session_id is required'}), 400

        db_session = db.get_session()

        session = db_session.query(DrivingSession).filter_by(
            id=data['session_id']
        ).first()

        if not session:
            db_session.close()
            return jsonify({'error': 'Session not found'}), 404

        if not session.is_active:
            db_session.close()
            return jsonify({'error': 'Session already ended'}), 400

        # End session
        session.is_active = False
        session.end_time = datetime.utcnow()
        session.duration = (session.end_time - session.start_time).seconds

        db_session.commit()
        db_session.close()

        return jsonify({
            'status': 'success',
            'session_id': session.id,
            'end_time': session.end_time.isoformat(),
            'duration': session.duration
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Initialize database
    db.create_tables()

    # Run Flask app
    port = int(os.getenv('API_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
