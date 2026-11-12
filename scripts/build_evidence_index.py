"""Build a readable index from the inspected-source ledgers; no network calls."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"


def source_ids(text):
    result = set()
    for prefix, first, last in re.findall(r"\b(MKT|SOC|FIN|CHK|T)(\d+)(?:[–-](?:MKT|SOC|FIN|CHK|T)?(\d+))?", text):
        width = len(first)
        for number in range(int(first), int(last or first)+1):
            result.add(f"{prefix}{number:0{width}d}")
    return result


def cell(value):
    if value is None:
        return "Undated / unspecified"
    if isinstance(value, (list, dict)):
        value = json.dumps(value, ensure_ascii=False)
    return str(value).replace("|", "\\|").replace("\n", " ")


def main():
    references = {}
    for file in ("landscape.md", "social-media.md"):
        for line in (RESEARCH/file).read_text(encoding="utf-8-sig").splitlines():
            match = re.match(r"\| ([NS]\d+)\b", line)
            if match:
                for key in source_ids(line):
                    references.setdefault(key,set()).add(match[1])
    records = []
    for path in sorted(RESEARCH.glob("*-sources.json")):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        entries = data if isinstance(data,list) else data.get("sources",data.get("entries",[]))
        for entry in entries:
            e = dict(entry)
            e["source_file"] = path.name
            e["candidate_index"] = ", ".join(sorted(references.get(e["id"],set()))) or e.get("candidate",e.get("decision_affected","Cross-cutting"))
            records.append(e)
    ids=[e["id"] for e in records]
    if len(ids)!=len(set(ids)):
        raise ValueError("duplicate evidence ID")
    rows = ["# Evidence ledger", "", "Research/access date: 12 November 2026. This is an index of scoped claims, not an assertion that every source is independent or every capability tested. Repeated URLs are repeated checks/uses, not independent corroboration. Publication dates and accessed dates are distinct; relative/unknown dates stay unresolved. Read each source JSON for inspection details and access failures.", "",
        f"**{len(records)} ledger records; {len({e['url'].rstrip('/') for e in records})} distinct URL strings after trailing-slash normalization.** Some records preserve failed access. Counts do not indicate evidence quality.", "",
        "| ID / candidate | Claim | Source / source date | What it establishes | Evidence type | Uncertainty / contradiction | Decision affected |",
        "|---|---|---|---|---|---|---|"]
    for e in records:
        date=e.get("source_date",e.get("date","undated")) or "undated"
        title=e.get("title",e["id"])
        establishes=e.get("what_it_establishes",e.get("establishes",e.get("claim","")))
        evidence=e.get("evidence_type",e.get("evidence_class",e.get("type","unknown")))
        uncertain=e.get("uncertainty_or_contradiction",e.get("uncertainty",e.get("limits","Not specified")))
        decision=e.get("decision_affected",e["candidate_index"])
        fields=[e["id"]+" / "+e["candidate_index"],e.get("claim",""),f"[{title}]({e['url']}) — {date}",establishes,evidence,uncertain,decision]
        rows.append("| "+" | ".join(map(cell,fields))+" |")
    (RESEARCH/"evidence-ledger.md").write_text("\n".join(rows)+"\n",encoding="utf-8")
    print(f"Indexed {len(records)} records; {len(set(e['url'].rstrip('/') for e in records))} URL strings.")


if __name__=="__main__":
    main()
