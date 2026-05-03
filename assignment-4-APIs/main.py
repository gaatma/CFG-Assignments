# main.py
# ------------------------------------------------------------
# Client-side simulation for the EVCS Threat Intelligence API.
# Demonstrates real-life usage of all 3 API endpoints by
# simulating an operator dashboard and station threat reports.
#
# Run this file AFTER starting app.py in a separate terminal.
# ------------------------------------------------------------

import requests

# Base URL of the running Flask API
BASE_URL = "http://127.0.0.1:5000"


def print_separator():
    """Prints a visual divider for readability in the console."""
    print("\n" + "=" * 60 + "\n")


def report_threat(station_id, threat_type, severity, description):
    """
    Client function for Endpoint 1: POST /report-threat
    Sends a threat report from a charging station to the API.

    Args:
        station_id  (str): ID of the reporting station.
        threat_type (str): Type of threat detected.
        severity    (str): Severity level.
        description (str): Details about the incident.
    """
    payload = {
        "station_id": station_id,
        "threat_type": threat_type,
        "severity": severity,
        "description": description
    }

    response = requests.post(f"{BASE_URL}/report-threat", json=payload)

    if response.status_code == 201:
        data = response.json()
        print(f"  [REPORTED] Threat ID #{data['threat_id']} logged for station {station_id}.")
    else:
        print(f"  [ERROR] Failed to report threat: {response.json()}")


def get_all_threats(status=None):
    """
    Client function for Endpoint 2: GET /threats
    Fetches and displays all threats, optionally filtered by status.

    Args:
        status (str, optional): 'active' or 'resolved', or None for all.
    """
    params = {}
    if status:
        params["status"] = status

    response = requests.get(f"{BASE_URL}/threats", params=params)

    if response.status_code == 200:
        data = response.json()
        label = f"(filter: {status})" if status else "(all)"
        print(f"  Threats found {label}: {data['count']}")
        for threat in data["threats"]:
            print(
                f"    ID #{threat['id']} | Station: {threat['station_id']} "
                f"| {threat['threat_type'].upper()} | {threat['severity'].upper()} "
                f"| Status: {threat['status']} | {threat['detected_at']}"
            )
    else:
        print(f"  [ERROR] {response.json()}")


def get_station_threats(station_id):
    """
    Client function for Endpoint 3: GET /threats/<station_id>
    Fetches all threats for a specific station and displays a summary.

    Args:
        station_id (str): The station to query.
    """
    response = requests.get(f"{BASE_URL}/threats/{station_id}")

    if response.status_code == 200:
        data = response.json()
        print(f"  Station: {data['station_id']} — Total threats: {data['total_threats']}")
        print("  Severity breakdown:")
        for entry in data["severity_summary"]:
            print(f"    {entry['severity'].upper()}: {entry['count']} incident(s)")
        print("  Incidents:")
        for threat in data["threats"]:
            print(
                f"    [{threat['severity'].upper()}] {threat['threat_type']} "
                f"— {threat['description']} (Status: {threat['status']})"
            )
    elif response.status_code == 404:
        print(f"  No threats found for station '{station_id}'.")
    else:
        print(f"  [ERROR] {response.json()}")


def run():
    """
    Simulates a real-life operator session with the EVCS Threat API.
    Demonstrates all three endpoints in a logical sequence.
    """

    print_separator()
    print("  EVCS THREAT INTELLIGENCE SYSTEM — OPERATOR CONSOLE")
    print("  Monitoring EV Charging Station Security in Real Time")
    print_separator()

    # --- Phase 1: Stations reporting threats ---
    print("PHASE 1: Incoming threat reports from EVCS stations...\n")

    report_threat(
        station_id="EVCS-UK-001",
        threat_type="ransomware",
        severity="critical",
        description="Ransomware detected on billing subsystem. Files encrypted. Payment portal offline."
    )

    report_threat(
        station_id="EVCS-UK-002",
        threat_type="dos",
        severity="high",
        description="Denial-of-service attack on OCPP communication layer. Station unreachable."
    )

    report_threat(
        station_id="EVCS-UK-001",
        threat_type="unauthorised_access",
        severity="medium",
        description="Repeated failed login attempts detected on management interface. Possible brute force."
    )

    report_threat(
        station_id="EVCS-UK-003",
        threat_type="mitm",
        severity="high",
        description="Man-in-the-middle attack suspected on EV-to-grid communication protocol."
    )

    print_separator()

    # --- Phase 2: Operator views all active threats ---
    print("PHASE 2: Operator dashboard — all active threats...\n")
    get_all_threats(status="active")

    print_separator()

    # --- Phase 3: Deep-dive into a specific station ---
    print("PHASE 3: Investigating station EVCS-UK-001 in detail...\n")
    get_station_threats("EVCS-UK-001")

    print_separator()

    # --- Phase 4: Check a station with no incidents ---
    print("PHASE 4: Checking station EVCS-UK-999 (no incidents expected)...\n")
    get_station_threats("EVCS-UK-999")

    print_separator()
    print("  Session complete. All reports logged. Stay secure.")
    print_separator()


if __name__ == "__main__":
    run()