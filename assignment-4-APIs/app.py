# app.py
# ------------------------------------------------------------
# EVCS Threat Intelligence API — Flask application.
# Provides endpoints for EV Charging Stations to report
# security threats and for operators to query threat data.
#
# Endpoints:
#   POST /report-threat          — Station reports a new threat
#   GET  /threats                — Retrieve all active threats
#   GET  /threats/<station_id>   — Retrieve threats for one station
# ------------------------------------------------------------

from flask import Flask, request, jsonify
import db_utils
import config

app = Flask(__name__)

# Valid threat types accepted by the API
VALID_THREAT_TYPES = {"ransomware", "dos", "mitm", "unauthorised_access", "malware", "unknown"}

# Valid severity levels
VALID_SEVERITIES = {"low", "medium", "high", "critical"}


# ------------------------------------------------------------------
# ENDPOINT 1: POST /report-threat
# Receives a JSON payload from a charging station describing a
# detected security threat and stores it in the database.
# ------------------------------------------------------------------

@app.route("/report-threat", methods=["POST"])
def report_threat():
    """
    Accepts a JSON body with:
        - station_id   (str)  : Unique ID of the reporting station
        - threat_type  (str)  : Type of threat detected
        - severity     (str)  : Severity level (low/medium/high/critical)
        - description  (str)  : Human-readable description of the threat

    Returns 201 on success, 400 on bad input, 500 on DB error.
    """
    data = request.get_json()

    # Validate that required fields are present
    required_fields = ["station_id", "threat_type", "severity", "description"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    # Validate threat_type and severity against allowed values
    if data["threat_type"].lower() not in VALID_THREAT_TYPES:
        return jsonify({"error": f"Invalid threat_type. Allowed: {VALID_THREAT_TYPES}"}), 400

    if data["severity"].lower() not in VALID_SEVERITIES:
        return jsonify({"error": f"Invalid severity. Allowed: {VALID_SEVERITIES}"}), 400

    insert_query = """
        INSERT INTO threats (station_id, threat_type, severity, description, status)
        VALUES (%s, %s, %s, %s, 'active')
    """
    params = (
        data["station_id"],
        data["threat_type"].lower(),
        data["severity"].lower(),
        data["description"]
    )

    try:
        new_id = db_utils.execute_query(insert_query, params)
        return jsonify({
            "message": "Threat reported successfully.",
            "threat_id": new_id,
            "station_id": data["station_id"]
        }), 201

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------------------
# ENDPOINT 2: GET /threats
# Returns all threats in the database, optionally filtered by
# status (active/resolved) via a query parameter.
# ------------------------------------------------------------------

@app.route("/threats", methods=["GET"])
def get_all_threats():
    """
    Optional query parameter:
        - status (str): Filter by 'active' or 'resolved'. Defaults to all.

    Returns a JSON list of all matching threat records.
    """
    status_filter = request.args.get("status")

    if status_filter:
        # Query 1: Filtered SELECT with WHERE clause
        query = """
            SELECT id, station_id, threat_type, severity, description,
                   status, detected_at
            FROM threats
            WHERE status = %s
            ORDER BY detected_at DESC
        """
        params = (status_filter.lower(),)
    else:
        # Query 2: Full table SELECT ordered by most recent
        query = """
            SELECT id, station_id, threat_type, severity, description,
                   status, detected_at
            FROM threats
            ORDER BY detected_at DESC
        """
        params = None

    try:
        threats = db_utils.fetch_query(query, params)

        # Convert datetime objects to strings for JSON serialisation
        for threat in threats:
            if threat.get("detected_at"):
                threat["detected_at"] = str(threat["detected_at"])

        return jsonify({
            "count": len(threats),
            "threats": threats
        }), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------------------
# ENDPOINT 3 (additional): GET /threats/<station_id>
# Returns all threats reported by a specific charging station,
# along with a summary count broken down by severity.
# ------------------------------------------------------------------

@app.route("/threats/<station_id>", methods=["GET"])
def get_threats_by_station(station_id):
    """
    Path parameter:
        - station_id (str): The unique ID of the charging station.

    Returns all threats for that station plus a severity summary.
    """
    # Query 3: Parameterised SELECT filtered by station_id
    threat_query = """
        SELECT id, threat_type, severity, description, status, detected_at
        FROM threats
        WHERE station_id = %s
        ORDER BY detected_at DESC
    """

    # Query 4: Aggregate query — count threats grouped by severity
    summary_query = """
        SELECT severity, COUNT(*) AS count
        FROM threats
        WHERE station_id = %s
        GROUP BY severity
    """

    try:
        threats = db_utils.fetch_query(threat_query, (station_id,))
        summary = db_utils.fetch_query(summary_query, (station_id,))

        if not threats:
            return jsonify({"message": f"No threats found for station '{station_id}'."}), 404

        # Convert datetime objects to strings
        for threat in threats:
            if threat.get("detected_at"):
                threat["detected_at"] = str(threat["detected_at"])

        return jsonify({
            "station_id": station_id,
            "total_threats": len(threats),
            "severity_summary": summary,
            "threats": threats
        }), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------------------
# Entry point — runs the Flask development server
# ------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.FLASK_DEBUG)