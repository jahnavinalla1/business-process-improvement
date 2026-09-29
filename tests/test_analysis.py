"""Behavioral tests for this standalone analytical project."""
import importlib.util,math,sqlite3,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from common import queries

def module(slug):
    spec=importlib.util.spec_from_file_location(slug,ROOT/'analyze.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def fixture(slug,table,rows):
    m=module(slug);db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    db.execute('CREATE TABLE '+table+' ('+m.SCHEMA+')')
    db.executemany('INSERT INTO '+table+' VALUES ('+','.join('?' for _ in rows[0])+')',rows)
    return queries(db,ROOT/'analysis.sql')

class AnalystTests(unittest.TestCase):
    def test_cash_model_distinguishes_build_and_running_costs(self):
        f=module('05-business-process-improvement').business_case
        s=f(1000,1,.5,50,10000,5000)
        self.assertEqual(s['annual_capacity_value'],25000)
        self.assertEqual(s['year1_net_value'],10000);self.assertEqual(s['payback_months'],6)
        self.assertIsNone(f(1000,1,0,50,10000,5000)['payback_months'])
    def test_sla_boundary_is_inclusive(self):
        t=fixture('05-business-process-improvement','requests',[
          ('a','Sales','Standard',10,30,20,12,0,0),('b','Sales','Standard',10,30,20,13,0,0)])
        self.assertEqual(t['team_performance'][0]['sla_pct'],50)
    def test_full_analysis_runs_and_exports(self):
        result=module('standalone').run()
        self.assertTrue(result)
        self.assertTrue((ROOT/'index.html').is_file())
        self.assertTrue((ROOT/'results/metrics.json').is_file())
if __name__=='__main__':unittest.main()
