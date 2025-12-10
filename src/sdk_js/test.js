import { ReliableRAG } from "./dist/index.js";

const client = new ReliableRAG("http://127.0.0.1:8000");

const run = async () => {
  const response = await client.ask(
    "How do I revoke HSM keys?",
    {
      revocation_time_hours: 6,
      siem_log_recorded: false
    }
  );

  console.log("ANSWER:", response.answer);
  console.log("RISK:", response.risk);
  console.log("REASONS:", response.reasons);
};

run();
