"""Self-contained original fictional input smoke tests, no proprietary files required."""
import tempfile
import unittest
from pathlib import Path
from src.parser import parse_file
from src.core import write_json
from run_pipeline import process_one
from src.presenter import flatten_promo

ROOT=Path(__file__).resolve().parents[1]

class PublicDemoTests(unittest.TestCase):
    def test_public_script_parses(self):
        ep,qa=parse_file(ROOT/'examples'/'episode-099-original-demo.txt')
        self.assertEqual(ep['_episode_id'],'099')
        self.assertTrue(qa['passed'])
        self.assertGreater(qa['event_count'],20)

    def test_public_script_generates_promo(self):
        ep,qa=parse_file(ROOT/'examples'/'episode-099-original-demo.txt')
        with tempfile.TemporaryDirectory() as td:
            ep.pop('_episode_id',None)
            src=Path(td)/'episode_099.json'
            write_json(src,ep)
            result,quality=process_one(src,Path(td)/'outputs',force=True,gate=True)
            self.assertTrue(quality['structural_pass'])
            self.assertGreaterEqual(len(result['promos']),1)
            for p in result['promos']:
                self.assertTrue(20<=float(p['duration_seconds'])<=60)
                r=flatten_promo(p)
                self.assertEqual(r['episode'],'099')
                self.assertTrue(r['start'].startswith('00:'))
                self.assertTrue(r['cliffhanger'])
                self.assertGreater(r['score'],0)

if __name__=='__main__':unittest.main()
