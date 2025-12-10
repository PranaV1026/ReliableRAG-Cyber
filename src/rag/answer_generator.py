import json
from typing import List, Tuple
from src.rag.chunker import TextChunk
from src.loader.policy_loader import load_all_policies
from src.reliability.risk_evaluator import evaluate_risk

def generate_answer(question: str, retrieved_chunks: List[Tuple[TextChunk, float]], context=None):
    if context is None:
        context = {}

    steps_texts = []
    sources = []
    scores = []

    # -------------------
    # Extract relevant chunks cleanly
    # -------------------
    for chunk, score in retrieved_chunks:
        scores.append(score)

        # Track sources for transparency
        sources.append(chunk.source)

        # Only list actionable IAM steps, skip description in bullets
        if chunk.source.startswith("steps."):
            if chunk.text not in steps_texts:
                steps_texts.append(chunk.text)

    # -------------------
    # Build formatted action answer
    # -------------------
    bullet_steps = "\n- ".join(steps_texts)
    answer_text = (
        "Required Offboarding Actions:\n"
        f"- {bullet_steps}\n\n"
        "Ensure SIEM timestamp + SOC ticket reference are attached."
    )

    # -------------------
    # Similarity-based confidence → risk
    # -------------------
    max_score = max(scores) if scores else 0.0
    confidence = round(max(0.0, min(max_score, 1.0)), 3)

    # soften thresholds: realistic SecOps
    if confidence >= 0.7:
        base_risk = "low"
    elif confidence >= 0.4:
        base_risk = "medium"
    else:
        base_risk = "high"

    # -------------------
    # YAML policy rule evaluation
    # -------------------
    policy = load_all_policies("policies")[0]
    policy_eval = evaluate_risk(policy, context)

    policy_risk = policy_eval["risk"]
    reasons = policy_eval["reasons"]

    # -------------------
    # Combine risks (take more severe)
    # -------------------
    risk_order = {"low": 1, "medium": 2, "high": 3}
    final_risk = base_risk
    if risk_order[policy_risk] > risk_order[final_risk]:
        final_risk = policy_risk

    result = {
        "answer": answer_text,
        "sources": [s for s in sources if s.startswith("steps.")],  # fully hide description
        "confidence": confidence,
        "risk": final_risk,
        "reasons": reasons
    }

    return json.dumps(result, indent=2)
