import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"scripts"))
from proof_lib import validate_proof,assert_publishable

class ProofTests(unittest.TestCase):
    def sample(self):
        return {"id":"x","client":"Example","project":"Test","problem":"Problem","work_completed":["Did work"],"before":{},"after":{},"metrics":{"m":{"value":1,"unit":"count","source":"e1","verification":"verified"}},"evidence":[{"id":"e1","type":"report","source":"sample","proves":"metric"}],"claim_status":"verified","content_ready":True}
    def test_verified_sample_passes(self):
        d=self.sample();self.assertEqual(validate_proof(d),[]);assert_publishable(d)
    def test_unverified_metric_blocks_publish(self):
        d=self.sample();d["metrics"]["m"]["verification"]="unverified";self.assertTrue(validate_proof(d));
        with self.assertRaises(ValueError): assert_publishable(d)
    def test_draft_blocks_publish(self):
        d=self.sample();d["claim_status"]="draft"
        with self.assertRaises(ValueError): assert_publishable(d)
if __name__=="__main__": unittest.main()
