"""
Convert the rich JSON schemas we produced earlier into the
single-file format that TableCoT expects (one markdown block
per question).

Usage
-----
python convert_schema.py schema1.json schema2.json ...  out.json
"""
import json, sys


# ---------- helpers -------------------------------------------------
def md_table(tbl: dict) -> str:
    head = "| " + " | ".join(tbl["columns"]) + " |\n"
    sep  = "|" + "|".join("-" * len(c) for c in tbl["columns"]) + "|\n"
    rows = "\n".join(
        "| " + " | ".join(map(str, row)) + " |"
        for row in tbl["data"]
    )
    return head + sep + rows


def build_entry(schema: dict, q: dict) -> dict:
    blocks = []
    for i, tname in enumerate(q["table_names"], 1):
        tbl = next(t for t in schema["tables"] if t["name"] == tname)
        blocks.append(f"### T{i} = {tname}\n" + md_table(tbl))

    reasoning = ""
    if "intermediate_reasoning_steps" in q:
        reasoning_lines = [
            f"- **Step {step['step']}:** {step['description']}"
            for step in q["intermediate_reasoning_steps"]
        ]
        reasoning = "\n".join(reasoning_lines)

    return {
        "table_id": f'{schema["schema_id"]}_{q["question_id"]}',
        "title": f'{schema["schema_id"]} – {" + ".join(q["table_names"])}',
        "table_block": "\n\n".join(blocks),
        "question": q["question"],
        "answer": q["answer"][0] if isinstance(q["answer"], list) else q["answer"],
        "reasoning": reasoning,
    }


# ---------- main ----------------------------------------------------
if len(sys.argv) < 3:
    print("Usage: python convert_schema.py in1.json [in2.json ...] out.json")
    sys.exit(1)

_ = sys.argv        

out_path = sys.argv[-1]
out_dict = {}

for p in sys.argv[1:-1]:
    schemas = json.load(open(p))
    schemas = schemas if isinstance(schemas, list) else [schemas]
    for sch in schemas:
        for q in sch["questions"]:
            out_dict[q["question_id"]] = build_entry(sch, q)

json.dump(out_dict, open(out_path, "w"), indent=2)
print(f"Wrote {len(out_dict)} examples ➜  {out_path}")
