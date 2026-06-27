# ── M12 CALCULATE — API ROUTES ───────────────────────
# SafeEdge Flask API — KPI Calculation Blueprint
# Endpoints:
#   POST /api/calculate  — compute TRIR, LTIFR, LTISR
#   GET  /api/kpis       — current KPI summary

from flask import Blueprint, jsonify, request

calculate_bp = Blueprint('calculate', __name__)

# ── KPI FORMULAS ─────────────────────────────────────
# TRIR  = (Recordable Incidents × 200,000) / Exposure Hours
# LTIFR = (Lost Time Injuries × 1,000,000) / Exposure Hours
# LTISR = (Lost Days × 1,000,000) / Exposure Hours

def calculate_trir(recordable_incidents, exposure_hours):
    if exposure_hours <= 0:
        return 0
    return round((recordable_incidents * 200000) / exposure_hours, 2)

def calculate_ltifr(lost_time_injuries, exposure_hours):
    if exposure_hours <= 0:
        return 0
    return round((lost_time_injuries * 1000000) / exposure_hours, 2)

def calculate_ltisr(lost_days, exposure_hours):
    if exposure_hours <= 0:
        return 0
    return round((lost_days * 1000000) / exposure_hours, 2)

@calculate_bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Validate
    required = ['recordable_incidents', 'lost_time_injuries',
                'lost_days', 'exposure_hours']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

    ri     = float(data['recordable_incidents'])
    lti    = float(data['lost_time_injuries'])
    ld     = float(data['lost_days'])
    hours  = float(data['exposure_hours'])

    if hours <= 0:
        return jsonify({'error': 'Exposure hours must be greater than 0'}), 400

    return jsonify({
        'trir':          calculate_trir(ri, hours),
        'ltifr':         calculate_ltifr(lti, hours),
        'ltisr':         calculate_ltisr(ld, hours),
        'exposure_hours': hours,
        'period':        data.get('period', ''),
        'site':          data.get('site', ''),
        'standard':      'ISO 45001 Cl. 9.1',
    })

@calculate_bp.route('/kpis', methods=['GET'])
def get_kpis():
    # Static KPIs for now — will pull from DB in Phase 2
    return jsonify({
        'trir':                0.42,
        'ltifr':               0.18,
        'ltisr':               0.00,
        'days_lti_free':       47,
        'open_actions':        7,
        'near_misses':         3,
        'training_compliance': 94,
        'period':              'June 2026',
        'site':                'Site A',
        'standard':            'ISO 45001 Cl. 9.1',
    })