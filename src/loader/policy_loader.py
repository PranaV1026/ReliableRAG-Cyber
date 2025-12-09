import os
import yaml
from typing import Any, Dict, List

# Type hints for clarity
Policy = Dict[str, Any]


def load_policy(file_path: str) -> Policy:
    """
    Load a single YAML policy file and return it as a Python dict.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def load_all_policies(policies_dir: str = "policies") -> List[Policy]:
    """
    Load all YAML policies from the given directory.
    Returns a list of policy dicts.
    """
    policies: List[Policy] = []

    # List all .yml or .yaml files in the directory
    for filename in os.listdir(policies_dir):
        if filename.endswith(".yml") or filename.endswith(".yaml"):
            full_path = os.path.join(policies_dir, filename)
            policy = load_policy(full_path)
            policies.append(policy)

    return policies


def pretty_print_policy(policy: Policy) -> None:
    """
    Print policy information in a readable way.
    """
    print("Policy ID:", policy.get("policy_id"))
    print("Title    :", policy.get("title"))
    print("Version  :", policy.get("version"))
    print("SLA (hrs):", policy.get("sla_hours"))
    print("Domain   :", policy.get("domain"))
    print("\nSteps:")
    for step in policy.get("steps", []):
        print(f"  - [{step.get('category')}] {step.get('id')}: {step.get('description')}")

    print("\nRisk Rules:")
    for rule in policy.get("risk_rules", []):
        print(f"  - {rule.get('id')} ({rule.get('risk')}): {rule.get('message')}")


if __name__ == "__main__":
    # This block will run when you do: python src/loader/policy_loader.py
    policies = load_all_policies("policies")

    print(f"Loaded {len(policies)} policy file(s).\n")

    for p in policies:
        pretty_print_policy(p)
        print("\n" + "=" * 60 + "\n")
