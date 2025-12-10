from reliablerag_cyber.client import Client

client = Client("http://127.0.0.1:8000")

response = client.ask(
    "How to revoke HSM keys?",
    context={
        "revocation_time_hours": 5,
        "siem_log_recorded": False
    }
)

print("ANSWER:", response.answer)
print("CONFIDENCE:", response.confidence)
print("RISK:", response.risk)
print("REASONS:", response.reasons)
print("SOURCES:", response.sources)
