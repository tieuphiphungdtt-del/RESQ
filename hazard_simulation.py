import random


# ============================================================
# RESQ SIMULATION STATE
# ============================================================

# Keep previous values so the simulation
# behaves more like real sensor readings.

_current_distance = 2.5
_current_roll = 0.0
_current_pitch = 0.0
_current_movement = "LOW"


# ============================================================
# SENSOR SIMULATION
# ============================================================

def generate_sensor_data():
    """
    Generate realistic simulated sensor data.

    Instead of completely random values,
    each reading changes gradually over time.

    Simulates:
    - VL53L1X distance sensor
    - MPU6050 orientation
    - Movement estimation
    """

    global \
        _current_distance, \
        _current_roll, \
        _current_pitch, \
        _current_movement


    # --------------------------------------------------------
    # DISTANCE
    # --------------------------------------------------------

    distance_change = random.uniform(
        -0.25,
        0.25
    )

    _current_distance += distance_change

    _current_distance = max(
        0.3,
        min(
            _current_distance,
            5.0
        )
    )


    # --------------------------------------------------------
    # ROLL
    # --------------------------------------------------------

    roll_change = random.uniform(
        -5,
        5
    )

    _current_roll += roll_change

    _current_roll = max(
        -35,
        min(
            _current_roll,
            35
        )
    )


    # --------------------------------------------------------
    # PITCH
    # --------------------------------------------------------

    pitch_change = random.uniform(
        -5,
        5
    )

    _current_pitch += pitch_change

    _current_pitch = max(
        -35,
        min(
            _current_pitch,
            35
        )
    )


    # --------------------------------------------------------
    # MOVEMENT
    # --------------------------------------------------------

    movement = random.choices(

        [
            "LOW",
            "MEDIUM",
            "HIGH"
        ],

        weights=[
            5,
            3,
            1
        ]

    )[0]

    _current_movement = movement


    return {

        "distance":
            round(
                _current_distance,
                2
            ),

        "roll":
            round(
                _current_roll,
                1
            ),

        "pitch":
            round(
                _current_pitch,
                1
            ),

        "movement":
            _current_movement

    }


# ============================================================
# HAZARD CALCULATION
# ============================================================

def calculate_hazard(data):

    distance = data["distance"]
    roll = data["roll"]
    pitch = data["pitch"]
    movement = data["movement"]


    # ========================================================
    # DISTANCE RISK
    # ========================================================

    if distance <= 0.5:

        distance_risk = 100

    elif distance <= 1.0:

        distance_risk = 80

    elif distance <= 2.0:

        distance_risk = 50

    elif distance <= 3.0:

        distance_risk = 20

    else:

        distance_risk = 0


    # ========================================================
    # TILT RISK
    # ========================================================

    tilt = max(
        abs(roll),
        abs(pitch)
    )


    if tilt >= 30:

        tilt_risk = 100

    elif tilt >= 20:

        tilt_risk = 70

    elif tilt >= 10:

        tilt_risk = 40

    else:

        tilt_risk = 0


    # ========================================================
    # MOVEMENT RISK
    # ========================================================

    movement_risk = {

        "LOW": 10,

        "MEDIUM": 50,

        "HIGH": 90

    }[movement]


    # ========================================================
    # SENSOR FUSION
    # ========================================================

    hazard_score = (

        distance_risk * 0.50

        + tilt_risk * 0.25

        + movement_risk * 0.25

    )


    hazard_score = round(
        hazard_score,
        1
    )


    # ========================================================
    # HAZARD CLASSIFICATION
    # ========================================================

    if hazard_score < 30:

        hazard = "SAFE"

        recommendation = (
            "CONTINUE — path appears clear"
        )


    elif hazard_score < 60:

        hazard = "CAUTION"

        recommendation = (
            "SLOW DOWN — potential hazard detected"
        )


    else:

        hazard = "DANGER"

        recommendation = (
            "STOP — high-risk conditions detected"
        )


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "hazard_score":
            hazard_score,

        "hazard":
            hazard,

        "recommendation":
            recommendation,

        "distance_risk":
            distance_risk,

        "tilt_risk":
            tilt_risk,

        "movement_risk":
            movement_risk

    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n===== RESQ SIMULATION =====\n")


    for i in range(10):

        sensor_data = (
            generate_sensor_data()
        )

        result = calculate_hazard(
            sensor_data
        )


        print(
            f"Distance: "
            f"{sensor_data['distance']} m"
        )

        print(
            f"Roll: "
            f"{sensor_data['roll']}°"
        )

        print(
            f"Pitch: "
            f"{sensor_data['pitch']}°"
        )

        print(
            f"Movement: "
            f"{sensor_data['movement']}"
        )

        print(
            f"Hazard Score: "
            f"{result['hazard_score']}"
        )

        print(
            f"Hazard: "
            f"{result['hazard']}"
        )

        print(
            f"Recommendation: "
            f"{result['recommendation']}"
        )

        print(
            "---------------------------"
        )

    print(
        "\n===========================\n"
    )