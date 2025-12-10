from typing import Dict, Any, List

def evaluate_risk(policy: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate YAML risk rules against runtime context.
    Returns final YAML-driven risk + reasons
    """
    rules = policy.get("risk_rules", [])
    sla_hours = policy.get("sla_hours", None)

    results: List[str] = []
    highest_risk = "low"  # default

    risk_order = {"low": 1, "medium": 2, "high": 3}

    for rule in rules:
        condition = rule.get("condition")
        risk_level = rule.get("risk", "low")
        message = rule.get("message", "")

        try:
            condition_met = eval(
                condition,
                {},  # no builtins
                {**context, "sla_hours": sla_hours}
            )
        except Exception:
            condition_met = False

        if condition_met:
            results.append(message)
            if risk_order[risk_level] > risk_order[highest_risk]:
                highest_risk = risk_level

    # If nothing triggered, explicitly confirm compliance
    if not results:
        results.append("No policy violations detected based on provided context.")

    return {
        "risk": highest_risk,
        "reasons": results
    }
