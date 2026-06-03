#!/usr/bin/env python3
"""Run the REAL AirPost_Station code (run.py + Sensors/ + Actuator/) in SIMULATION — no Raspberry Pi.

It injects `sim_hw/` (simulated RPi.GPIO, spidev, gps, adafruit_dht, board, apriltag) onto the import
path so the unchanged station code runs on any machine, reading modelled sensor values and publishing
the SAME MQTT `data/<STATION_ID>` messages a real station would. Those flow through AirPost_Sink ->
Kafka -> logic-core -> Elasticsearch exactly like production. When a real station board exists, run
plain `run.py` on it (without this shim) and nothing else changes.

Usage:
    python3 run_station_sim.py <station_id>      # e.g. 1 -> publishes as STA1, positioned at station 1
Env:
    MQTT_BROKER_HOST (default 127.0.0.1)         # the mosquitto broker the Sink also listens on
"""
import json
import math
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Conversion + station coords mirror the simulated world (gen_world / station_iot): ENU metres about
# a fixed lat/lon origin, so the station's "GPS" matches where it sits in Gazebo.
ORIGIN_LAT, ORIGIN_LON, EARTH_R = 37.5, 127.0, 6371000.0


def en_to_latlon(e, n):
    rad = math.pi / 180
    return (ORIGIN_LAT + (n / EARTH_R) / rad,
            ORIGIN_LON + (e / (EARTH_R * math.cos(ORIGIN_LAT * rad))) / rad)


def main():
    sid_num = sys.argv[1] if len(sys.argv) > 1 else "1"
    # Find this station's world position from the generated sites file (falls back to origin).
    sites = os.path.join(HERE, "..", "simulation", "tests", "airpost_sites.json")
    lat, lon, alt = ORIGIN_LAT, ORIGIN_LON, 0.0
    try:
        st = {str(s["id"]): s for s in json.load(open(sites))["stations"]}
        if sid_num in st:
            s = st[sid_num]
            lat, lon = en_to_latlon(s["E"], s["N"])
            alt = s.get("Z", 0.0)
    except Exception as e:
        print(f"(could not load station coords from {sites}: {e}; using origin)", flush=True)

    os.environ.setdefault("MQTT_BROKER_HOST", "127.0.0.1")
    os.environ["STATION_ID"] = f"STA{sid_num}"
    os.environ["STATION_LAT"], os.environ["STATION_LON"], os.environ["STATION_ALT"] = str(lat), str(lon), str(alt)

    # Put the simulated hardware shims FIRST on the path so `import RPi.GPIO`, `import spidev`, etc.
    # resolve to them, then run the real station entrypoint unchanged.
    sys.path.insert(0, os.path.join(HERE, "sim_hw"))
    os.chdir(HERE)
    print(f"AirPost_Station SITL: running real run.py as STA{sid_num} @ ({lat:.5f},{lon:.5f}) "
          f"-> MQTT data/STA{sid_num} on {os.environ['MQTT_BROKER_HOST']}", flush=True)
    runpy.run_path(os.path.join(HERE, "run.py"), run_name="__main__")


if __name__ == "__main__":
    main()
