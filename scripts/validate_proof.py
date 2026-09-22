#!/usr/bin/env python3
import sys
from proof_lib import load_proof, validate_proof

def main():
    if len(sys.argv)!=2:
        print("Usage: python3 scripts/validate_proof.py <proof.json>"); return 2
    data=load_proof(sys.argv[1]); errors=validate_proof(data)
    if errors:
        print("VALIDATION FAILED")
        for e in errors: print("ERROR:",e)
        return 1
    print("VALIDATION PASSED")
    print("Proof ID:",data["id"])
    print("Claim status:",data["claim_status"])
    print("Content ready:",data["content_ready"])
    return 0
if __name__=="__main__": raise SystemExit(main())
