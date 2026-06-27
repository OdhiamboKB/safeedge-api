# ── M2 INCIDENT MANAGEMENT — API ROUTES ─────────────
# SafeEdge Flask API — Incidents Blueprint
# Endpoints:
#   GET  /api/incidents       — list all incidents
#   POST /api/incidents       — create new incident
#   GET  /api/incidents/<id>  — get single incident

from flask import Blueprint, jsonify, request
import json
import os
import uuid
from datetime import datetime

incidents_bp = Blueprint('incidents', __name__)

# ── DATA STORE ───────────────────────────────────────
# JSON file as dev database — will migrate to
# PostgreSQL in Phase 2 (Charter v2.3 Month 8-11)
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'incidents.json')

def load_incidents():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_incidents(incidents):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(incidents, f, indent=2)

# ── SEED DATA ─────────────────────────────────────────
SEED_INCIDENTS = [
    {
        'id': 'INC-2026-047',
        'title': 'Slip on Wet Surface — Loading Bay Entrance',
        'type': 'injury',
        'severity': 'High',
        'site': 'site-a',
        'date': '2026-05-02',
        'time': '09:14',
        'location': 'Loading Bay Entrance',
        'description': 'Worker reported a slip and fall near the loading bay entrance following overnight rainfall.',
        'reporter_name': 'James Omondi',
        'reporter_email': 'j.omondi@company.com',
        'lost_time': False,
        'rca_required': True,
        'status': 'Open',
        'created_at': '2026-05-02T09:14:00Z',
    },
    {
        'id': 'NM-2026-048',
        'title': 'Unsecured Load — Forklift Operation Area',
        'type': 'near-miss',
        'severity': 'NearMiss',
        'site': 'site-a',
        'date': '2026-05-01',
        'time': '14:32',
        'location': 'Warehouse B',
        'description': 'Supervisor observed a pallet stack exceeding safe height in the active forklift zone.',
        'reporter_name': 'Amina Wanjiku',
        'reporter_email': 'a.wanjiku@company.com',
        'lost_time': False,
        'rca_required': True,
        'status': 'Under Review',
        'created_at': '2026-05-01T14:32:00Z',
    },
    {
        'id': 'INC-2026-046',
        'title': 'Chemical Spill — Battery Charging Room',
        'type': 'environmental',
        'severity': 'Medium',
        'site': 'site-a',
        'date': '2026-04-30',
        'time': '07:55',
        'location': 'Workshop · Battery Room',
        'description': 'Small electrolyte spill during battery top-up procedure. Spill kit deployed within 4 minutes.',
        'reporter_name': 'Kamau Mutua',
        'reporter_email': 'k.mutua@company.com',
        'lost_time': False,
        'rca_required': True,
        'status': 'Closed',
        'created_at': '2026-04-30T07:55:00Z',
    },
]

def init_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) <= 2:
        save_incidents(SEED_INCIDENTS)

# ── ROUTES ───────────────────────────────────────────

@incidents_bp.route('/incidents', methods=['GET'])
def get_incidents():
    init_data()
    incidents = load_incidents()

    # Optional filters
    severity = request.args.get('severity')
    status = request.args.get('status')
    site = request.args.get('site')

    if severity:
        incidents = [i for i in incidents if i.get('severity') == severity]
    if status:
        incidents = [i for i in incidents if i.get('status') == status]
    if site:
        incidents = [i for i in incidents if i.get('site') == site]

    return jsonify({
        'count': len(incidents),
        'incidents': incidents,
    })

@incidents_bp.route('/incidents', methods=['POST'])
def create_incident():
    init_data()
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Validate required fields
    required = ['title', 'type', 'severity', 'date', 'description',
                'reporter_name', 'reporter_email']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f'Missing required fields: {missing}'}), 400

    # Generate incident ID
    year = datetime.now().year
    incidents = load_incidents()
    count = len(incidents) + 1
    incident_id = f"INC-{year}-{str(count).zfill(3)}"

    new_incident = {
        'id': incident_id,
        'title': data['title'],
        'type': data['type'],
        'severity': data['severity'],
        'site': data.get('site', 'site-a'),
        'date': data['date'],
        'time': data.get('time', ''),
        'location': data.get('location', ''),
        'description': data['description'],
        'reporter_name': data['reporter_name'],
        'reporter_email': data['reporter_email'],
        'lost_time': data.get('lost_time', False),
        'rca_required': data.get('rca_required', True),
        'status': 'Open',
        'created_at': datetime.utcnow().isoformat() + 'Z',
    }

    incidents.append(new_incident)
    save_incidents(incidents)

    return jsonify({
        'message': 'Incident created successfully',
        'incident': new_incident,
    }), 201

@incidents_bp.route('/incidents/<incident_id>', methods=['GET'])
def get_incident(incident_id):
    init_data()
    incidents = load_incidents()
    incident = next((i for i in incidents if i['id'] == incident_id), None)

    if not incident:
        return jsonify({'error': f'Incident {incident_id} not found'}), 404

    return jsonify(incident)