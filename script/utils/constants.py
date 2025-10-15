# constants.py

# KIM Push/Pull
KIM_PUSH_PULL_RISK = {
    "LOW": "LOW",
    "MODERATE": "MODERATE",
    "HIGH": "HIGH",
    "VERY_HIGH": "HIGH",
}

KIM_PUSH_PULL_RISK_MAX_SCORE = {
    "LOW": 10,
    "MODERATE": 100,
}

# REBA
REBA_RISK = {
    "NEGLIGIBLE_RISK": "NEGLIGIBLE_RISK",
    "LOW": "LOW",
    "MEDIUM": "MEDIUM",
    "HIGH": "HIGH",
    "VERY_HIGH_RISK": "VERY_HIGH_RISK",
}

REBA_RISK_MAX_SCORE = {
    "NEGLIGIBLE_RISK": 1,
    "LOW": 3,
    "MEDIUM": 7,
    "HIGH": 10,
    "VERY_HIGH_RISK": 10,
}

# NIOSH
NIOSH_RISK = {
    "LOW": "LOW",
    "MODERATE": "MODERATE",
    "HIGH": "HIGH",
}

# Strain Index
STRAIN_INDEX_RISK = {
    "SAFE": "SAFE",
    "HAZARDOUS": "HAZARDOUS",
}

STRAIN_INDEX_RISK_MAX_SCORE = {
    "SAFE": 10,
}

# Categories
CATEGORIES_ENUM = {
    "VERTICAL_MOVEMENT": "vertical_movement",
    "LATERAL_LONGITUDINAL_MOVEMENT": "lateral_longitudinal_movement",
}

# Kim MHO
KIM_MHO_HOLDING_MATRIX = [
    [1.5, 3, 5.5],
    [2.5, 4.5, 9],
    [3.5, 7, 14],
    [5.5, 11, 22],
    [35, 100, 100],
    [None, None, None],
]

KIM_MHO_MATRIX = [
    [0.5, 1, 2.5, 5, 7],
    [0.5, 2, 4, 7.5, 11],
    [1, 3, 6, 12, 18],
    [1.5, 5, 10, 19, None],
    [8, 30, 100, 100, 100],
    [8, 30, None, None, None],
]

KIM_MHO_RISK = {
    "LOW": "LOW",
    "SLIGHTLY_INCREASED": "SLIGHTLY_INCREASED",
    "SUBSTANTIALLY_INCREASED": "SUBSTANTIALLY_INCREASED",
    "HIGH": "HIGH",
}

KIM_MHO_RISK_MAX_SCORE = {
    "LOW": 20,
    "SLIGHTLY_INCREASED": 50,
    "SUBSTANTIALLY_INCREASED": 100,
    "HIGH": 101,
}
KIM_MHO_HOLDING_FREQUENCIES = [15, 30, 60]
KIM_MHO_MOVING_FREQUENCIES = [4, 15, 30, 60, 90]
KIM_MHO_INTENSITIES = ["VERY_LOW", "MODERATE", "HIGH", "VERY_HIGH", "PEAK", "POWERFUL_HITTING"]

KIM_MHO_RATING_POINTS = {
    "force_transfer": {"OPTIMUM": 0, "RESTRICTED": 2, "HINDERED": 4},
    "arm_posture": {"GOOD": 0, "RESTRICTED": 1, "UNFAVOURABLE": 2, "POOR": 3},
    "work_conditions": {"GOOD": 0, "RESTRICTED": 1, "UNFAVOURABLE": 2},
    "temporal_distribution": {"GOOD": 0, "RESTRICTED": 2, "UNFAVOURABLE": 4},
    "body_posture": {
        "ALTERNATED_SITTING_STANDING": 0,
        "OCCASIONAL_WALKING": 2,
        "NO_WALKING": 4,
        "SEVERELY_INCLINED": 6,
    },
}
