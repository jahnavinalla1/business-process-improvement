import random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import write_csv

def generate():
    rng=random.Random(5505);rows=[]
    for i in range(1000):
        team=rng.choice(['Sales','Operations','Finance']);route=rng.choice(['Standard','Complex']);rework=int(rng.random()<(.3 if route=='Complex' else .12))
        intake=rng.randint(1,8);review=rng.randint(4,20)+(24 if team=='Finance' else 0)+(18 if route=='Complex' else 0)
        approval=rng.randint(1,16);execution=rng.randint(2,12);rework_hours=rework*rng.randint(4,24)
        rows.append(dict(request_id=f'R{i:05}',team=team,route=route,intake_hours=intake,review_hours=review,
            approval_hours=approval,execution_hours=execution,rework_hours=rework_hours,rework=rework))
    write_csv(Path(__file__).with_name('data.csv'),rows)
if __name__=='__main__':generate()
