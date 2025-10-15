from typing import Any, Dict, Optional, Literal

from utils import (
    KIM_PUSH_PULL_RISK,
    KIM_PUSH_PULL_RISK_MAX_SCORE,
    REBA_RISK,
    REBA_RISK_MAX_SCORE,
    STRAIN_INDEX_RISK,
    STRAIN_INDEX_RISK_MAX_SCORE,
    KIM_MHO_RISK,
    KIM_MHO_RISK_MAX_SCORE,
    KIM_MHO_HOLDING_MATRIX,
    KIM_MHO_MATRIX,
    KIM_MHO_HOLDING_FREQUENCIES,
    KIM_MHO_MOVING_FREQUENCIES,
    KIM_MHO_RATING_POINTS,
    KIM_MHO_INTENSITIES,
)

class RiskCalculator:

    _map_report_to_risk = {}

    @classmethod
    def calculate_risk(cls, report_name: Literal["reba", "niosh", "kim_push_pull", "strain_index", "kim_mho"], report: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        cls._map_report_to_risk = {
            "reba": cls._calculate_reba_risk,
            "niosh": cls._calculate_niosh_risk,
            "kim_pp": cls._calculate_kim_push_pull_risk,
            "strain_index": cls._calculate_strain_index_risk,
            "kim_mho": cls._calculate_kim_mho_risk
        }

        calculate_risk_fn = cls._map_report_to_risk.get(report_name)
        if not calculate_risk_fn or not report:
            return None

        risk = calculate_risk_fn(report)

        return {**report, "risk": risk}

    @staticmethod
    def _calculate_reba_risk(report: Dict[str, Any]):
        score_seconds = report.get("score_seconds")

        if score_seconds is None or score_seconds <= REBA_RISK_MAX_SCORE["LOW"]:
            return REBA_RISK["LOW"]
        if score_seconds <= REBA_RISK_MAX_SCORE["NEGLIGIBLE_RISK"]:
            return REBA_RISK["NEGLIGIBLE_RISK"]
        if score_seconds <= REBA_RISK_MAX_SCORE["MEDIUM"]:
            return REBA_RISK["MEDIUM"]
        if score_seconds <= REBA_RISK_MAX_SCORE["HIGH"]:
            return REBA_RISK["HIGH"]
        return REBA_RISK["VERY_HIGH_RISK"]

    @staticmethod
    def _calculate_kim_push_pull_risk(report: Dict[str, Any]):
        score = report.get("score")

        if score is None or score < KIM_PUSH_PULL_RISK_MAX_SCORE["LOW"]:
            return KIM_PUSH_PULL_RISK["LOW"]
        if score < KIM_PUSH_PULL_RISK_MAX_SCORE["MODERATE"]:
            return KIM_PUSH_PULL_RISK["MODERATE"]
        return KIM_PUSH_PULL_RISK["HIGH"]

    @staticmethod
    def _calculate_strain_index_risk(report: Dict[str, Any]):
        score_left_rsi = report.get("score_left_rsi")
        score_right_rsi = report.get("score_right_rsi")
        if score_left_rsi is None or score_right_rsi is None:
            return STRAIN_INDEX_RISK["SAFE"]

        if score_left_rsi < STRAIN_INDEX_RISK_MAX_SCORE["SAFE"] and score_right_rsi < STRAIN_INDEX_RISK_MAX_SCORE["SAFE"]:
            return STRAIN_INDEX_RISK["SAFE"]
        return STRAIN_INDEX_RISK["HAZARDOUS"]

    @staticmethod
    def _calculate_niosh_risk(report: Dict[str, Any]):
        risk_value = report.get("risk")
        return risk_value if risk_value is not None else "LOW"

    @staticmethod
    def _calculate_kim_mho_risk(report: Dict[str, Any]) -> str:
        duration = report.get("duration")
        if duration is None:
            return KIM_MHO_RISK["LOW"]
            
        score = RiskCalculator._calculate_kim_mho_score(report)
        total_score = score * duration

        if total_score < KIM_MHO_RISK_MAX_SCORE["LOW"]:
            return KIM_MHO_RISK["LOW"]
        if total_score < KIM_MHO_RISK_MAX_SCORE["SLIGHTLY_INCREASED"]:
            return KIM_MHO_RISK["SLIGHTLY_INCREASED"]
        if total_score < KIM_MHO_RISK_MAX_SCORE["SUBSTANTIALLY_INCREASED"]:
            return KIM_MHO_RISK["SUBSTANTIALLY_INCREASED"]
        
        return KIM_MHO_RISK["HIGH"]

    @staticmethod
    def _calculate_kim_mho_score(report: Dict[str, Any]) -> float:
        rating_points = KIM_MHO_RATING_POINTS
        subtotal_points = 0
        
        for key in rating_points:
            value = report.get(key)
            if value is not None and value in rating_points[key]:
                subtotal_points += rating_points[key][value]
                
        force_exertion_points = [
            RiskCalculator._calculate_force_exertion_points(report, side="left"),
            RiskCalculator._calculate_force_exertion_points(report, side="right"),
        ]

        return subtotal_points + max(force_exertion_points)

    @staticmethod
    def _calculate_force_exertion_points(report: Dict[str, Any], side: str) -> float:
        intensity = report.get(f"{side}_force_intensity")
        frequency = report.get(f"{side}_force_frequency")
        type_ = report.get(f"{side}_force_type")

        if intensity is None or frequency is None or type_ is None:
            return 0

        if type_ == "HOLDING":
            points_table = KIM_MHO_HOLDING_MATRIX
            frequencies = KIM_MHO_HOLDING_FREQUENCIES
        elif type_ == "MOVING":
            points_table = KIM_MHO_MATRIX
            frequencies = KIM_MHO_MOVING_FREQUENCIES
        else:
            return 0

        try:
            intensity_index = KIM_MHO_INTENSITIES.index(intensity)
        except ValueError:
            return 0

        frequency_index = next((i for i, f in enumerate(frequencies) if f >= frequency), None)
        if frequency_index is None:
            return 0

        points = points_table[intensity_index][frequency_index]
        if points is None:
            return 0

        return points