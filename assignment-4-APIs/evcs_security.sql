
-- ------------------------------------------------------------
-- Database and table setup for the EVCS Threat Intelligence API.
-- Run this file in DBeaver (or MySQL CLI) before starting the API.
-- ------------------------------------------------------------

-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS evcs_security;

USE evcs_security;

-- threats table: stores all security incidents reported by EVCS stations
CREATE TABLE IF NOT EXISTS threats (
    id           INT AUTO_INCREMENT PRIMARY KEY,   -- Unique threat record ID
    station_id   VARCHAR(50)  NOT NULL,            -- ID of the reporting station (e.g. EVCS-UK-001)
    threat_type  VARCHAR(50)  NOT NULL,            -- Type of threat (ransomware, dos, mitm, etc.)
    severity     VARCHAR(20)  NOT NULL,            -- Severity level: low / medium / high / critical
    description  TEXT         NOT NULL,            -- Human-readable description of the incident
    status       VARCHAR(20)  NOT NULL DEFAULT 'active',  -- Current status: active / resolved
    detected_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP  -- Timestamp of detection
);