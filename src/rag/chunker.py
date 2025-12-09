from typing import Any, Dict, List

Policy = Dict[str, Any]


class TextChunk:
    """
    Represents a small piece of text we can embed and search.
    """
    def __init__(self, chunk_id: str, policy_id: str, source: str, text: str):
        self.chunk_id = chunk_id       # e.g., "PRIVILEGED_OFFBOARDING:step:disable_cloud_role"
        self.policy_id = policy_id     # e.g., "PRIVILEGED_OFFBOARDING"
        self.source = source           # e.g., "steps.disable_cloud_role"
        self.text = text               # the actual text content

    def __repr__(self) -> str:
        return f"TextChunk(id={self.chunk_id}, source={self.source}, text={self.text[:40]}...)"


def policy_to_chunks(policy: Policy) -> List[TextChunk]:
    """
    Convert a single policy dict into a list of TextChunk objects.
    We will chunk:
      - policy description
      - each step description
      - each risk rule message
    """
    chunks: List[TextChunk] = []

    policy_id = policy.get("policy_id", "UNKNOWN_POLICY")

    # 1) Overall policy description
    description = policy.get("description", "")
    if description:
        chunk_id = f"{policy_id}:description"
        chunks.append(
            TextChunk(
                chunk_id=chunk_id,
                policy_id=policy_id,
                source="description",
                text=description,
            )
        )

    # 2) Each step
    for step in policy.get("steps", []):
        step_id = step.get("id", "unknown_step")
        step_desc = step.get("description", "")
        if step_desc:
            chunk_id = f"{policy_id}:step:{step_id}"
            source = f"steps.{step_id}"
            chunks.append(
                TextChunk(
                    chunk_id=chunk_id,
                    policy_id=policy_id,
                    source=source,
                    text=step_desc,
                )
            )

    # 3) Each risk rule
    for rule in policy.get("risk_rules", []):
        rule_id = rule.get("id", "unknown_rule")
        rule_msg = rule.get("message", "")
        if rule_msg:
            chunk_id = f"{policy_id}:risk:{rule_id}"
            source = f"risk_rules.{rule_id}"
            chunks.append(
                TextChunk(
                    chunk_id=chunk_id,
                    policy_id=policy_id,
                    source=source,
                    text=rule_msg,
                )
            )

    return chunks


def policies_to_chunks(policies: List[Policy]) -> List[TextChunk]:
    """
    Convert a list of policies to a single flat list of chunks.
    """
    all_chunks: List[TextChunk] = []
    for policy in policies:
        policy_chunks = policy_to_chunks(policy)
        all_chunks.extend(policy_chunks)
    return all_chunks


if __name__ == "__main__":
    # Simple test: load policies and print chunks
    from src.loader.policy_loader import load_all_policies

    policies = load_all_policies("policies")
    chunks = policies_to_chunks(policies)

    print(f"Total chunks: {len(chunks)}")
    for c in chunks:
        print(c)
