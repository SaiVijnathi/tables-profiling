print("hi")

import json
from pathlib import Path
import time
from gemini_client import client

print("hi")



# 1. Load the anonymized dataset
DATA_FILE = Path("data") / "erp_dataset.json"

with DATA_FILE.open("r", encoding="utf-8") as file:
    dataset = json.load(file)

tables = dataset["tables"]

print(f"Loaded {len(tables)} tables.")


# 2. Prepare compact dataset
table_data = json.dumps(
    tables,
    separators=(",", ":"),
    ensure_ascii=False
)



# 3. Prepare a shorter prompt
prompt = f"""
You are an expert in SAP data migration.

Identify the likely business purpose and SAP table
for each anonymous legacy database table.

Analyze column names, descriptions and sample records.

Rules:
- Do not assume any particular table order.
- Do not invent unsupported information.
- Use "Unknown" if identification is uncertain.
- Classify every table separately.
- Be concise.

Return ONLY valid JSON in this format:

{{
  "classifications": [
    {{
      "table_id": "SRC_001",
      "predicted_domain": "Customer Master",
      "predicted_sap_table": "KNA1",
      "confidence": 90,
      "evidence": "Brief reason",
      "ambiguities": "None"
    }}
  ]
}}

Dataset:
{table_data}
"""


# 3. Call Gemini and measure time
print("\nSending request to Gemini...")

start_time = time.perf_counter()

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    reasoning_effort="low",
    max_tokens=2000
)

end_time = time.perf_counter()



# 4. Display Gemini's response
result = response.choices[0].message.content

print("\nGemini's classification results:\n")
print(result)

print(
    f"\nAPI response time: {end_time - start_time:.2f} seconds"
)
