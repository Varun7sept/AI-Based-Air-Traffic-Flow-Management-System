from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import requests
import math
import threading
import time
from rtree import index as rtree_index

app = Flask(__name__)
socketio = SocketIO(app)
API_URL = 'https://opensky-network.org/api/states/all'
API_USERNAME = "your_username"
API_PASSWORD = "your_password"

# Global variables
positions = []
collisions = []
rtree = rtree_index.Index()
lock = threading.Lock()

# Thresholds
THRESHOLD_DISTANCE = 2000  # meters (2 km)
ALTITUDE_THRESHOLD = 500   # meters
TIME_WINDOW = 60           # seconds

def fetch_data_with_retries():
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(API_URL, auth=(API_USERNAME, API_PASSWORD), timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API error: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching data (attempt {attempt+1}): {e}")
        time.sleep(5)
    return None

def calculate_distance(pos1, pos2):
    R = 6371e3
    lat1, lon1 = math.radians(pos1['lat']), math.radians(pos1['lon'])
    lat2, lon2 = math.radians(pos2['lat']), math.radians(pos2['lon'])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

def detect_collisions(positions, rtree):
    warnings = []
    for pos1 in positions:
        nearby_ids = list(rtree.intersection((pos1['lat']-0.1, pos1['lon']-0.1,
                                              pos1['lat']+0.1, pos1['lon']+0.1)))
        for id in nearby_ids:
            pos2 = next((p for p in positions if p['id'] == id), None)
            if pos2 and pos1['id'] != pos2['id']:
                distance = calculate_distance(pos1, pos2)
                altitude_diff = abs(pos1['alt'] - pos2['alt'])
                if distance < THRESHOLD_DISTANCE and altitude_diff < ALTITUDE_THRESHOLD:
                    warnings.append({
                        'aircraft1': pos1['id'],
                        'aircraft2': pos2['id'],
                        'distance': round(distance, 2),
                        'altitude_diff': altitude_diff,
                        'time_to_collision': "N/A"  # simplified
                    })
    return warnings

def update_positions():
    global positions, collisions, rtree
    while True:
        data = fetch_data_with_retries()
        if data and "states" in data and data["states"]:
            with lock:
                positions.clear()
                rtree = rtree_index.Index()
                for state in data["states"]:
                    if state[6] is not None and state[5] is not None and state[13] is not None:
                        aircraft_id = str(state[0])
                        pos = {
                            'id': aircraft_id,
                            'lat': state[6],
                            'lon': state[5],
                            'alt': state[13],
                            'velocity': state[9],
                            'course': state[10]
                        }
                        positions.append(pos)
                        rtree.insert(hash(aircraft_id),
                                     (state[6]-0.1, state[5]-0.1, state[6]+0.1, state[5]+0.1))
                print(f"Fetched {len(positions)} aircraft positions")
        else:
            print("No valid aircraft data received")

        with lock:
            collisions = detect_collisions(positions, rtree)
            print(f"Detected {len(collisions)} potential collisions")

        time.sleep(15)

@app.route('/api/positions')
def get_positions():
    return jsonify({'positions': positions, 'collisions': collisions})

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    socketio.emit('update', {'positions': positions, 'collisions': collisions})

def emit_updates():
    while True:
        socketio.emit('update', {'positions': positions, 'collisions': collisions})
        time.sleep(15)

if __name__ == '__main__':
    threading.Thread(target=update_positions, daemon=True).start()
    threading.Thread(target=emit_updates, daemon=True).start()
    socketio.run(app, debug=True)
