from flask import Flask, render_template, jsonify

# ResQ simulation engine
from simulation.hazard_simulation import (
    generate_sensor_data,
    calculate_hazard
)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# RESQ DATA PIPELINE
# ============================================================

def get_sensor_data():
    """
    Get sensor data and process it through
    the ResQ hazard engine.

    CURRENT:
        Uses simulated sensor data.

    FUTURE:
        Replace generate_sensor_data() with
        real Raspberry Pi sensor readings.
    """

    # --------------------------------------------------------
    # 1. GET SENSOR DATA
    # --------------------------------------------------------

    sensor_data = generate_sensor_data()


    # --------------------------------------------------------
    # 2. RUN HAZARD ALGORITHM
    # --------------------------------------------------------

    hazard_data = calculate_hazard(
        sensor_data
    )


    # --------------------------------------------------------
    # 3. COMBINE SENSOR + ALGORITHM DATA
    # --------------------------------------------------------

    return {
        **sensor_data,
        **hazard_data
    }


# ============================================================
# MAIN DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    return render_template(
        "dashboard.html"
    )


# ============================================================
# SENSOR API
# ============================================================

@app.route("/api/sensor-data")
def sensor_data():

    data = get_sensor_data()

    return jsonify(data)


# ============================================================
# SYSTEM STATUS API
# ============================================================

@app.route("/api/status")
def system_status():

    return jsonify({

        "system": "ResQ",

        "status": "ONLINE",

        "mode": "SIMULATION",

        "hardware_connected": False

    })


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    print()
    print("========================================")
    print("              RESQ SYSTEM")
    print("========================================")
    print()
    print("Mode: SIMULATION")
    print("Hardware: NOT CONNECTED")
    print()
    print("Dashboard:")
    print("http://127.0.0.1:5000")
    print()
    print("API:")
    print("http://127.0.0.1:5000/api/sensor-data")
    print()
    print("========================================")
    print()


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )