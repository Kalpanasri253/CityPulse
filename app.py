from flask import Flask, render_template, jsonify
import random
import time
from datetime import datetime

app = Flask(__name__)

# Simple mock data (no engine folder needed)
ASSETS = {
    "bridge-01": {"location": "Main Bridge", "health": "healthy", "score": 92},
    "road-01": {"location": "Highway 101", "health": "warning", "score": 65},
    "pipe-01": {"location": "Water Main", "health": "critical", "score": 10}
}

@app.route('/')
def dashboard():
    return '''
    <h1>🏙️ CityPulse - Infrastructure Health Monitor</h1>
    <button onclick="location.reload()">🔄 Update Sensors</button>
    <div id="assets"></div>
    <script>
        fetch("/api/assets").then(r=>r.json()).then(data=>{
            document.getElementById("assets").innerHTML = 
                Object.entries(data.assets).map(([id,asset])=>
                    `<div style="border-left:5px solid ${
                        asset.health=="healthy"?"green":asset.health=="warning"?"orange":"red"
                    }; padding:10px; margin:10px;">
                        <h3>${id} - ${asset.location}</h3>
                        <strong>${asset.health.toUpperCase()}</strong> | Score: ${asset.score}
                    </div>`
                ).join("")
        });
    </script>
    '''

@app.route('/api/assets')
def get_assets():
    # Simulate health changes
    for asset_id in ASSETS:
        if random.random() < 0.3:  # 30% chance to change
            states = ["healthy", "warning", "critical"]
            current = ASSETS[asset_id]["health"]
            new_state = random.choice([s for s in states if s != current])
            ASSETS[asset_id]["health"] = new_state
            ASSETS[asset_id]["score"] = {"healthy":90, "warning":60, "critical":10}[new_state]
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'assets': ASSETS,
        'summary': {
            'healthy_count': sum(1 for a in ASSETS.values() if a['health']=='healthy'),
            'critical_count': sum(1 for a in ASSETS.values() if a['health']=='critical')
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)