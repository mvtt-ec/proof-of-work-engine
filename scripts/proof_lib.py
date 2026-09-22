from __future__ import annotations
import json
from pathlib import Path

REQUIRED={"id","client","project","problem","work_completed","before","after","metrics","evidence","claim_status","content_ready"}

def load_proof(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate_proof(data):
    errors=[]
    missing=REQUIRED-set(data)
    if missing:
        return [f"missing required fields: {sorted(missing)}"]
    if data["claim_status"] not in {"draft","needs_review","verified","rejected"}:
        errors.append("invalid claim_status")
    if not isinstance(data["content_ready"],bool):
        errors.append("content_ready must be boolean")
    if data["claim_status"]=="verified":
        if not data["evidence"]:
            errors.append("verified proof must include evidence")
        for name,metric in data.get("metrics",{}).items():
            if not metric.get("source"):
                errors.append(f"metric {name!r} is missing source")
            if metric.get("verification")!="verified":
                errors.append(f"metric {name!r} is not verified")
    return errors

def assert_publishable(data):
    errors=validate_proof(data)
    if data.get("claim_status")!="verified": errors.append("claim_status must be verified")
    if data.get("content_ready") is not True: errors.append("content_ready must be true")
    if not data.get("evidence"): errors.append("at least one evidence reference is required")
    if errors: raise ValueError("; ".join(errors))
