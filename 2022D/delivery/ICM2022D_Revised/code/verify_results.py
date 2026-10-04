"""Independent checks of saved results and the final PDF deliverables."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.special import expit
import pymupdf

root=Path(__file__).resolve().parents[1]
m=json.loads((root/'results/metrics.json').read_text())
raw=pd.read_csv(root/'data/synthetic_audits_raw.csv')
unique=raw.drop_duplicates('event_id')
assert len(raw)==35597 and len(unique)==34560
assert unique.passed.isna().sum()==987
counts=pd.read_csv(root/'data/kpi_counts.csv')
assert (counts.n+counts.unknown==240).all()
assert int(counts.y.sum())==int(unique.passed.sum())
assert (counts.lower<=counts.upper).all()
state=pd.read_csv(root/'results/state_estimates.csv'); test=state[state.month>=37]
rmse=float(np.sqrt(np.mean((test['true']-test.estimate)**2)))
assert np.isclose(rmse,m['state']['test_filtered_rmse'])
coverage=((test['true']>=test.lower90)&(test['true']<=test.upper90)).mean()
assert np.isclose(coverage,m['state']['conditional_90_coverage'])
cap=np.array(m['chain']['baseline_capability']); b=np.array(m['chain']['coefficients'])
design=np.r_[1.,cap,cap[0]*cap[2],0.,0.]
assert np.isclose(100*(expit(b@design)@np.array([.6,.4])),m['chain']['baseline_maturity'])
assert (b[:,1:5]>=0).all() and (b[:,5:]<=0).all()
plan=pd.read_csv(root/'results/optimal_plan.csv')
cost=(plan.units+.15*(plan.units>0)).sum()
assert np.isclose(cost,sum(m['optimization']['quarter_spend']))
assert cost*1.2<=7 and plan.loc[plan.project=='Recovery','units'].iloc[0]>=1
assert m['optimization']['worst_net_units']>=m['optimization']['equal_worst_net_units']
td=pd.read_csv(root/'results/heldout_decisions.csv')
assert len(td)==800 and td.groupby('plan').size().eq(200).all()
assert (td.loc[td.feasible,'regret']>=-1e-8).all()
assert td.loc[~td.feasible,'regret'].isna().all()
pdfs={}
for lang in ['en','zh']:
    doc=pymupdf.open(root/f'main_{lang}.pdf')
    assert len(doc)<=25
    txt='\n'.join(p.get_text() for p in doc)
    assert '??' not in txt and '\ufffd' not in txt
    assert all(len(p.get_text())>100 for p in doc)
    if lang=='en':
        starts=[i for i,p in enumerate(doc) if "Letter to ICM Corporation" in p.get_text() and 'Dear Port Users' in p.get_text()]
        assert len(starts)==1
        assert 'Sincerely' in doc[starts[0]].get_text()
        assert 'Summary Sheet' in doc[0].get_text()
    pdfs[lang]=len(doc)
print(json.dumps({'numerical_checks':'passed','pdf_pages':pdfs,'coverage_disclosed':float(coverage),'data_class':'synthetic only'},indent=2))
