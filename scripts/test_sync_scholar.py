import unittest
from unittest.mock import patch, Mock
import tempfile
from pathlib import Path
import json
import requests
import sync_scholar as m
HTML='''<div id="gsc_prf_in">Xiaofei Wang</div><table><tr class="gsc_a_tr"><td><a class="gsc_a_at" href="/citations?view_op=view_citation&amp;citation_for_view=abc">A paper</a><div class="gs_gray">X Wang</div><div class="gs_gray">Ocean Engineering</div></td><td class="gsc_a_ac">12*</td><td class="gsc_a_y">2026</td></tr></table><button id="gsc_bpf_more" disabled>More</button>'''
class SyncTests(unittest.TestCase):
 def test_parse(self):
  rows, more=m.parse_page(HTML);self.assertFalse(more);self.assertEqual(rows[0]['citations'],12);self.assertEqual(rows[0]['year'],2026)
 def test_blocked(self):
  with self.assertRaises(ValueError):m.parse_page('<html>unusual traffic</html>')
 def test_atomic_failure_and_success(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'data').mkdir();(root/'data/scholar.json').write_text('{"scholar_id":"Gq2ORzoAAAAJ"}')
   path=root/'data/publications.json';path.write_text(json.dumps({'papers':[{'title':'A paper','authors':'X. Wang','type':'journal'}]}));original=path.read_bytes()
   session=Mock();session.__enter__=Mock(return_value=session);session.__exit__=Mock(return_value=False)
   response=Mock();response.raise_for_status.side_effect=requests.HTTPError('429');session.get.return_value=response
   with patch.object(m,'ROOT',root),patch.object(m.requests,'Session',return_value=session):
    with self.assertRaises(requests.HTTPError):m.sync()
    self.assertEqual(original,path.read_bytes())
    response.raise_for_status.side_effect=None;response.text=HTML;m.sync()
    data=json.loads(path.read_text());self.assertEqual(data['papers'][0]['type'],'journal');self.assertTrue(data['updated_at'])
if __name__=='__main__':unittest.main()
