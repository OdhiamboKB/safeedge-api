# ── KB SAFEEDGE FLASK API ────────────────────────────
# Backend for SafeEdge QHSE Management System
# Charter v2.3 — Phase 1 MVP
# Endpoints: /incidents, /calculate, /hazards
# AI Engine: Claude API (Phase 4)

from flask import Flask
from flask_cors import CORS
from routes.incidents import incidents_bp
from routes.calculate import calculate_bp

app = Flask(__name__)
CORS(app)  # Allow React frontend to call this API

# ── REGISTER BLUEPRINTS ──────────────────────────────
app.register_blueprint(incidents_bp, url_prefix='/api')
app.register_blueprint(calculate_bp, url_prefix='/api')

# ── HEALTH CHECK ─────────────────────────────────────
@app.route('/api/health')
def health():
    return {
        'status': 'ok',
        'system': 'KB SafeEdge API',
        'version': '1.0.0',
        'modules': ['M1', 'M2', 'M8', 'M12']
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)