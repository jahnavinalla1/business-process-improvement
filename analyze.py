import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import database,queries,publish
F=Path(__file__).resolve().parent
SCHEMA='request_id TEXT PRIMARY KEY,team TEXT,route TEXT,intake_hours INTEGER CHECK(intake_hours>=0),review_hours INTEGER CHECK(review_hours>=0),approval_hours INTEGER CHECK(approval_hours>=0),execution_hours INTEGER CHECK(execution_hours>=0),rework_hours INTEGER CHECK(rework_hours>=0),rework INTEGER CHECK(rework IN(0,1))'
def business_case(volume,touch_hours_saved,adoption,hourly_cost,build_cost,annual_running_cost):
    gross=volume*touch_hours_saved*adoption*hourly_cost
    annual_net=gross-annual_running_cost
    return {'annual_capacity_value':round(gross,2),'annual_net_value':round(annual_net,2),
      'year1_net_value':round(annual_net-build_cost,2),
      'payback_months':round(build_cost/(annual_net/12),2) if annual_net>0 else None}
def run():
    db=database(F,'requests',SCHEMA);t=queries(db,F/'analysis.sql');ranked=t.pop('ranked_cycle_times');n=len(ranked)
    assert n==1000
    assert db.execute('SELECT COUNT(*) FROM requests WHERE (rework=0 AND rework_hours>0) OR (rework=1 AND rework_hours=0)').fetchone()[0]==0
    p90=ranked[math.ceil(.9*n)-1]['cycle_hours'];mean=sum(r['cycle_hours'] for r in ranked)/n
    sla=100*sum(r['cycle_hours']<=72 for r in ranked)/n;review=next(r for r in t['stages'] if r['stage']=='Review')
    scenarios=[]
    for adoption in [.4,.65,.85]:
        scenarios.append({'adoption_pct':int(adoption*100),'assumed_annual_volume':12000,'touch_hours_saved':.20,
          'hourly_cost':45,'build_cost':25000,'annual_running_cost':12000,
          **business_case(12000,.20,adoption,45,25000,12000)})
    t['business_case_scenarios']=scenarios;t['cycle_summary']=[{'requests':n,'mean_hours':round(mean,2),'p90_hours':p90,'sla_pct':round(sla,2)}]
    publish(F,'Approval workflow and automation business case','Should a team pilot structured intake and approval routing?',
    {'Requests':'1,000','Mean cycle time':f'{mean:.1f} hours','72-hour SLA':f'{sla:.1f}%','90th percentile':f'{p90} hours'},t,
    [f"Review accounts for {review['mean_elapsed_hours']/mean*100:.1f}% of mean elapsed cycle time.",
     f"{t['team_performance'][0]['team']} has the highest average cycle time; route mix is exposed for a fairer comparison.",
     f"The 65%-adoption scenario values annual capacity at ${scenarios[1]['annual_capacity_value']:,.0f}, with a modeled {scenarios[1]['payback_months']}-month payback."],
    ['Pilot validated intake forms and explicit approval routing in one team, with exception handling and an audit log.',
     'Time actual employee touch work before accepting the 0.20-hour savings assumption; elapsed waiting time is not paid effort.',
     'Compare a pilot team with a matched control over four weeks; track p90 cycle time, rework, SLA compliance and overrides.'],
    'Synthetic completed requests only; open backlog and calendar effects are omitted. Stage durations are elapsed hours. All volumes, labor rates, adoption, effort savings and costs in the business case are planning assumptions, not inferred from elapsed time. Capacity value is not cash savings unless spending is actually reduced. No realized improvement is claimed.',
    {'title':'Where time accumulates','note':'Mean elapsed hours per completed request; stages are sequential and include waiting.','unit':' h',
     'rows':[{'label':r['stage'],'value':r['mean_elapsed_hours']} for r in t['stages']]})
    return t
if __name__=='__main__':run()
