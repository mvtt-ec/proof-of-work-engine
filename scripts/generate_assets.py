#!/usr/bin/env python3
import json,sys
from pathlib import Path
from proof_lib import load_proof,assert_publishable

def metrics_text(metrics):
    lines=[]
    for name,m in metrics.items():
        before,after=m.get("before"),m.get("after")
        if before is not None and after is not None:
            lines.append(f"- {name.replace('_',' ').title()}: {before} → {after} {m.get('unit','')} (source: {m['source']})")
        else:
            lines.append(f"- {name.replace('_',' ').title()}: {m.get('value')} {m.get('unit','')} (source: {m['source']})")
    return "\n".join(lines) or "- No quantitative metric supplied."

def main():
    if len(sys.argv)!=2:
        print("Usage: python3 scripts/generate_assets.py <proof.json>"); return 2
    data=load_proof(sys.argv[1]); assert_publishable(data)
    out=Path("output")/data["id"]; out.mkdir(parents=True,exist_ok=True)
    work="\n".join(f"- {x}" for x in data["work_completed"]); metrics=metrics_text(data["metrics"])
    assets={
      "case-study.md":f"# {data['project']} — {data['client']}\n\n## Problem\n{data['problem']}\n\n## Work completed\n{work}\n\n## Verified metrics\n{metrics}\n",
      "linkedin.md":f"# Social Post\n\nProblem: {data['problem']}\n\nWork:\n{work}\n\nVerified proof:\n{metrics}\n",
      "instagram-carousel.md":f"# Carousel Copy\n\nProblem: {data['problem']}\n\nWork:\n{work}\n\nProof:\n{metrics}\n",
      "reel-script.md":f"# Short-Form Script\n\nProblem: {data['problem']}\n\nWork:\n{work}\n\nProof:\n{metrics}\n",
      "website-proof-block.md":f"# Website Proof Block\n\n{data['problem']}\n\n{work}\n\n{metrics}\n",
      "proposal-proof.md":f"# Proposal Proof Block\n\n{data['problem']}\n\n{work}\n\n{metrics}\n",
      "outreach-email.md":f"# Outreach Draft\n\nProblem addressed: {data['problem']}\n\n{work}\n\nVerified evidence:\n{metrics}\n",
      "ad-creative-brief.md":f"# Ad Creative Brief\n\nProblem: {data['problem']}\n\nDemonstrate before/work/after using verified evidence only.\n\n{metrics}\n",
      "sales-deck-slide.md":f"# Sales Deck Proof Slide\n\nProblem: {data['problem']}\n\n{work}\n\n{metrics}\n"
    }
    for name,text in assets.items(): (out/name).write_text(text,encoding="utf-8")
    print(f"Generated {len(assets)} assets in {out}"); return 0
if __name__=="__main__": raise SystemExit(main())
