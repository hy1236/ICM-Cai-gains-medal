"""Reproducible, entirely synthetic ICM 2022 D experiment. Python 3.12.
Run from any directory. Outputs are relative to this script's parent folder.
No corporate observations or expert interviews are represented by these data.
"""
from pathlib import Path
import json, itertools
import numpy as np
import pandas as pd
from scipy.special import expit, logit
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
for p in ['data','results','figures']: (ROOT/p).mkdir(exist_ok=True)
rng = np.random.default_rng(2022)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'savefig.bbox':'tight'})
COL = ['#235789','#D18B25','#218B79']
out = {'seed':2022, 'evidence_class':'synthetic scenario; no ICM observations'}

# Indicator coverage: distinct mechanisms are retained even when correlated.
ids = ['P1','P2','P3','P4','T1','T2','T3','T4','R1','R2','R3','R4','R5','R6','C1','C2']
coverage = [[0],[1],[0],[1],[2],[3],[3],[2,5],[4],[4],[3,4],[5],[6],[5,7],[8],[8]]
cost = np.array([2,1,3,2,1,1,2,2,1,3,2,1,1,2,2,3])
mandatory = [1,4,7,9,11,13,15]
def screen(cost):
    best=None
    for bits in itertools.product([0,1],repeat=16):
        z=np.array(bits)
        if not z[mandatory].all(): continue
        covered=set(g for i in np.flatnonzero(z) for g in coverage[i])
        if len(covered)==9 and (best is None or cost@z<best[0]): best=(float(cost@z),z)
    return best
screen_cost, selected=screen(cost)
out['screen']={'selected':[ids[i] for i in np.flatnonzero(selected)],'cost':screen_cost,'full_cost':int(cost.sum()),'coverage':1.0}
jac=[]
for idx in range(16):
    c=cost.astype(float).copy(); c[idx]*=1.2
    s=screen(c)[1]
    jac.append(float((s&selected).sum()/(s|selected).sum()))
out['screen']['min_jaccard']=min(jac)
pd.DataFrame({'indicator':ids,'cost_units':cost,'selected':selected,'requirements':[','.join(map(str,g)) for g in coverage]}).to_csv(ROOT/'data/indicator_coverage.csv',index=False)

# Raw audit events. One independent anchor per dimension; other KPIs remain
# operational diagnostics rather than being declared independent measurements.
T=48; month=np.arange(T); load=np.sin(2*np.pi*month/12)
actions=np.zeros((T,3))
for d in range(3):
    actions[:,d]=((month+2*d)%12<4).astype(float)
def lag_action(u,delay):
    w=np.array([1.,.6,.36]); w/=w.sum()
    return np.array([sum(w[l]*u[t-delay-l] for l in range(3) if t-delay-l>=0) for t in range(len(u))])
true_delay=[2,1,2]; mus=np.array([-.65,.05,-.9]); true=np.zeros((T,3))
rows=[]
for d in range(3):
    v=lag_action(actions[:,d],true_delay[d]); z=mus[d]
    for t in range(T):
        z=.88*z+.12*mus[d]+.24*v[t]+rng.normal(0,.08)
        true[t,d]=z
        p=expit(z-.25*load[t]); yy=rng.binomial(1,p,240)
        for i,y in enumerate(yy):
            missing = rng.random()<(.20 if t in [39,40] and y==0 else .025)
            rows.append((f'{d}-{t}-{i}',t+1,d,int(y) if not missing else np.nan,int(rng.random()<.025), 'sim'))
raw=pd.DataFrame(rows,columns=['event_id','month','dimension','passed','late','evidence'])
dups=raw.sample(frac=.03,random_state=2022)
raw=pd.concat([raw,dups],ignore_index=True)
raw.to_csv(ROOT/'data/synthetic_audits_raw.csv',index=False)
clean=raw.drop_duplicates('event_id')
y=np.zeros((T,3)); n=np.zeros((T,3)); m=np.zeros((T,3))
for (t,d),g in clean.groupby(['month','dimension']):
    y[t-1,d]=g.passed.sum(); n[t-1,d]=g.passed.notna().sum(); m[t-1,d]=g.passed.isna().sum()
out['cleaning']={'raw':len(raw),'unique':len(clean),'duplicates':len(raw)-len(clean),'unknown':int(m.sum()),'late':int(clean.late.sum())}
pd.DataFrame([{'month':t+1,'dimension':d,'y':y[t,d],'n':n[t,d],'unknown':m[t,d], 'lower':y[t,d]/240,'upper':(y[t,d]+m[t,d])/240} for t in range(T) for d in range(3)]).to_csv(ROOT/'data/kpi_counts.csv',index=False)

# Model I: empirical-logit Gaussian working filter, not an exact binomial filter.
obs=np.log((y+.5)/(n-y+.5))+.25*load[:,None]
R=1/(y+.5)+1/(n-y+.5)
def kfilter(par,d,delay,noise=.08):
    phi,mu,beta=par; v=lag_action(actions[:,d],delay)
    zz=mu; V=.5; means=[]; variances=[]; preds=[]; scores=[]
    for t in range(T):
        prior=phi*zz+(1-phi)*mu+beta*v[t]; vp=phi**2*V+noise**2
        err=obs[t,d]-prior; S=vp+R[t,d]
        scores.append(.5*(np.log(S)+err*err/S))
        K=vp/S; zz=prior+K*err; V=(1-K)*vp
        preds.append(prior); means.append(zz); variances.append(V)
    return np.array(means),np.array(variances),np.array(preds),np.array(scores)
fits=[]; mh=np.zeros_like(true); vv=np.zeros_like(true); pred=np.zeros_like(true); pred0=np.zeros_like(true)
for d in range(3):
    candidates=[]
    for delay in range(4):
        fit=minimize(lambda p:kfilter(p,d,delay)[3][:24].sum(), [.85,-.5,.2], method='L-BFGS-B',bounds=[(.5,.98),(-2,2),(0,.6)])
        assert fit.success, fit.message
        result=kfilter(fit.x,d,delay)
        candidates.append((result[3][24:36].sum(),delay,fit.x,result))
    chosen=min(candidates,key=lambda a:a[0]); _,delay,pars,res=chosen
    mh[:,d],vv[:,d],pred[:,d],_=res
    pred0[:,d]=candidates[0][3][2]
    fits.append({'dimension':d,'delay':delay,'true_delay':true_delay[d],'phi':pars[0],'mu':pars[1],'beta':pars[2]})
ahat=expit(mh); lo=expit(mh-1.645*np.sqrt(vv)); hi=expit(mh+1.645*np.sqrt(vv))
truth=expit(true); test=np.s_[36:48]
rmse=lambda a,b:float(np.sqrt(np.mean((a-b)**2)))
out['state']={'fits':fits,'test_filtered_rmse':rmse(ahat[test],truth[test]),'test_raw_rmse':rmse(expit(obs[test]),truth[test]),'test_forecast_rmse':rmse(expit(pred[test]),truth[test]),'test_zero_lag_rmse':rmse(expit(pred0[test]),truth[test]),'conditional_90_coverage':float(np.mean((truth[test]>=lo[test])&(truth[test]<=hi[test])))}
pd.DataFrame([{'month':t+1,'dimension':d,'true':truth[t,d],'estimate':ahat[t,d],'lower90':lo[t,d],'upper90':hi[t,d],'one_step':expit(pred[t,d])} for t in range(T) for d in range(3)]).to_csv(ROOT/'results/state_estimates.csv',index=False)
fig,axs=plt.subplots(3,1,figsize=(8,6.5),sharex=True)
for d,ax in enumerate(axs):
    ax.axvspan(37,48,color='#e7ecf4'); ax.plot(month+1,truth[:,d],color='black',ls='--',label='Synthetic truth')
    ax.plot(month+1,ahat[:,d],color=COL[d],label='Filtered capability'); ax.fill_between(month+1,lo[:,d],hi[:,d],alpha=.22,color=COL[d],label='Conditional 90% interval')
    ax.set_ylabel(['People','Technology','Process'][d]); ax.set_ylim(.15,.95); ax.grid(alpha=.15)
axs[0].legend(ncol=3,fontsize=10,loc='upper left'); axs[-1].set_xlabel('Month (shading: test period)')
fig.tight_layout(); fig.savefig(ROOT/'figures/state.pdf'); plt.close(fig)

# Model II. Independent synthetic pilot profiles supply variation to identify
# monotone chain response. No use of test outcomes in fitting or penalty choice.
N=1800; cap=rng.uniform(.2,.9,(N,3)); loading=rng.uniform(-1,1,N); shock=rng.binomial(1,.15,N)
def design(a,load=0,shock=0):
    a=np.atleast_2d(a); size=len(a)
    return np.column_stack([np.ones(size),a,a[:,0]*a[:,2],np.broadcast_to(load,size),np.broadcast_to(shock,size)])
X=design(cap,loading,shock)
bt=np.array([[-2.8,1.4,1.6,1.8,.8,-.5,-1.4],[-3.0,1.7,1.3,2.0,.6,-.7,-1.7]])
probs=expit(X@bt.T); outcome=rng.binomial(1,probs)
train=np.arange(1200); valid=np.arange(1200,1500); te=np.arange(1500,1800)
def fit_chain(k,pen):
    def fun(b):
        eta=X[train]@b; p=expit(eta)
        val=np.mean(np.logaddexp(0,eta)-outcome[train,k]*eta)+pen*np.sum(b[1:]**2)/2
        grad=X[train].T@(p-outcome[train,k])/len(train); grad[1:]+=pen*b[1:]
        return val,grad
    f=minimize(fun,[-2,1,1,1,.2,-.3,-1],jac=True,bounds=[(-8,3)]+[(0,6)]*4+[(-4,0),(-6,0)],method='L-BFGS-B')
    assert f.success
    return f.x
bet=[]; chain_metrics=[]
for k in range(2):
    candidates=[]
    for pen in [0,.001,.01]:
        b=fit_chain(k,pen); p=expit(X[valid]@b)
        candidates.append((np.mean((p-outcome[valid,k])**2),pen,b))
    _,pen,b=min(candidates,key=lambda z:z[0]); bet.append(b)
    p=expit(X[te]@b); null=outcome[train,k].mean()
    chain_metrics.append({'chain':k,'penalty':pen,'brier':float(np.mean((p-outcome[te,k])**2)),'null_brier':float(np.mean((null-outcome[te,k])**2)),'logloss':float(-np.mean(outcome[te,k]*np.log(p)+(1-outcome[te,k])*np.log1p(-p))),'truth_rmse':rmse(p,probs[te,k])})
bet=np.array(bet); weights=np.array([.6,.4])
def score(a,load=0,shock=0,coef=bet): return 100*(expit(design(a,load,shock)@coef.T)@weights)
base=ahat[-1]; base_score=float(score(base)[0])
out['chain']={'metrics':chain_metrics,'coefficients':bet.tolist(),'baseline_capability':base.tolist(),'baseline_maturity':base_score}
pd.DataFrame(np.column_stack([cap,loading,shock,outcome]),columns=['aP','aT','aR','load','shared_outage','import_success','export_success']).assign(evidence='sim').to_csv(ROOT/'data/synthetic_pilot_profiles.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(8,3.3))
calrows=[]
for k,ax in enumerate(axs):
    p=expit(X[te]@bet[k]); bins=np.minimum((p*5).astype(int),4)
    for q in sorted(set(bins)):
        ix=bins==q; xp=p[ix].mean(); yp=outcome[te,k][ix].mean(); nn=int(ix.sum())
        ax.scatter(xp,yp,s=20+nn,color=COL[k],alpha=.8); calrows.append([k,q,xp,yp,nn])
    ax.plot([0,1],[0,1],'k--',lw=1); ax.set(xlim=(0,1),ylim=(0,1),xlabel='Mean predicted success',ylabel='Observed success',title=['Import chain','Export chain'][k]); ax.grid(alpha=.15)
fig.tight_layout(); fig.savefig(ROOT/'figures/calibration.pdf'); plt.close(fig)
pd.DataFrame(calrows,columns=['chain','bin','predicted','observed','n']).to_csv(ROOT/'results/calibration.csv',index=False)

# Conditional state uncertainty and coefficient uncertainty are sampled jointly
# within each vector; coefficients from the observed information approximation.
bdraw=[]
for k,b in enumerate(bet):
    p=expit(X[train]@b); info=X[train].T@((p*(1-p))[:,None]*X[train])+np.eye(7)*1e-5
    draws=rng.multivariate_normal(b,np.linalg.inv(info),size=1000)
    draws[:,1:5]=np.maximum(draws[:,1:5],0); draws[:,5:]=np.minimum(draws[:,5:],0); bdraw.append(draws)
adraw=expit(rng.normal(mh[-1],np.sqrt(vv[-1]),(1000,3)))
ms=np.array([score(adraw[i],coef=np.stack([bdraw[0][i],bdraw[1][i]]))[0] for i in range(1000)])
out['chain']['approx_joint90']=np.quantile(ms,[.05,.95]).tolist()

# Model III: exhaustive finite menu. Each project is off, or receives 1/2/3
# units at start quarter 1/2. A unit is USD 10,000; fixed cost .15 unit.
names=['Training','Hiring','Integration','Governance','Recovery']
maps=np.array([[1,0,0],[1,0,0],[0,1,0],[0,0,1],[0,.65,.35]])
G=np.array([.16,.18,.22,.24,.12]); rate=np.array([.8,.55,.6,.75,.65]); delays=np.array([1,2,1,0,1])
hours=np.array([1.2,.7,1.5,1.0,.8]); fixed=.15
options=[(0,0)]+[(lev,start) for lev in [1,2,3] for start in [0,1]]
menus=np.array(list(itertools.product(options,repeat=5)))
levels=menus[:,:,0].astype(float); starts=menus[:,:,1].astype(int); active=levels>0
costs=(levels+fixed*active)
spend=np.stack([(costs*(starts==q)).sum(1) for q in range(2)],axis=1)
staff=np.stack([(levels*hours*(starts==q)).sum(1) for q in range(2)],axis=1)
dependency=(~active[:,2]) | (active[:,3] & (starts[:,3]<=starts[:,2]))
recovery=levels[:,4]>=1
scenarios=[('Nominal',1.,1.,0,1.),('Overrun',1.2,.9,0,1.),('Delay',1.1,.8,1,1.),('Low value',1.05,.85,0,.8)]
budgets=np.array([7.,4.]); capacity=np.array([8.,6.])
def evaluate(cmult=1,gmult=1,delayextra=0,value=1,form='exponential',base_a=base,coef=bet):
    lev=levels; st=starts
    def caps_at(q):
        effective=np.maximum(q-st-delays-delayextra+1,0)/2
        fraction=np.minimum(1,effective); E=lev*fraction
        g=G*gmult*(1-np.exp(-rate*E)) if form=='exponential' else G*gmult*np.minimum(rate*E,.85)
        return np.clip(base_a+g@maps,0,.995)
    basep=expit(design(base_a)@coef.T)[0]
    gain=np.zeros(len(lev)); final=None
    for q in range(4):
        ca=caps_at(q); p=expit(design(ca)@coef.T)
        # Reference quarterly transactions [6000,4000], avoided loss [$40,$60].
        gain+=((p-basep)*np.array([24.,24.])*value).sum(1)/(1.02**q)
        final=ca
    net=gain-(spend/np.array([1,1.02])).sum(1)*cmult
    return net,final
Z=np.array([evaluate(c,g,d,v)[0] for _,c,g,d,v in scenarios])
joint_indices=[int(np.argsort(ms)[q]) for q in [50,950]]
Z=np.vstack([Z]+[evaluate(1.1,.85,0,.9,base_a=adraw[i],coef=np.stack([bdraw[0][i],bdraw[1][i]]))[0][None,:] for i in joint_indices])
out['chain']['planning_joint_draw_indices']=joint_indices
feasible=(spend*1.2<=budgets+1e-9).all(1)&(staff<=capacity+1e-9).all(1)&dependency&recovery
assert feasible.any()
worst=Z.min(0); opt=int(np.argmax(np.where(feasible,worst,-np.inf)))
nomfeas=(spend<=budgets).all(1)&(staff<=capacity).all(1)&dependency&recovery
nom=int(np.argmax(np.where(nomfeas,Z[0],-np.inf)))
# Equal feasible allocation: all five receive one unit in first quarter.
eq=int(np.flatnonzero(np.all(levels==1,axis=1)&np.all(starts==0,axis=1))[0])
# Greedy menu: repeatedly select feasible single-step increase with best nominal
# incremental profit, starting from mandatory recovery; timing fixed to Q1.
cur=np.array([0,0,0,0,1]); gi=int(np.flatnonzero(np.all(levels==cur,1)&np.all(starts==0,1))[0])
while True:
    cand=[]
    for j in range(5):
        nxt=cur.copy(); nxt[j]+=1
        if nxt[j]>3: continue
        ix=np.flatnonzero(np.all(levels==nxt,1)&np.all(starts==0,1))
        if len(ix) and feasible[ix[0]] and Z[0,ix[0]]>Z[0,gi]: cand.append((Z[0,ix[0]]-Z[0,gi],int(ix[0]),nxt))
    if not cand: break
    _,gi,cur=max(cand,key=lambda a:a[0])
out['optimization']={'menu_size':len(menus),'feasible':int(feasible.sum()),'optimality_gap_finite_menu':0,'levels':levels[opt].tolist(),'starts_quarter':(starts[opt]+1).tolist(),'quarter_spend':spend[opt].tolist(),'quarter_staff':staff[opt].tolist(),'worst_net_units':float(worst[opt]),'nominal_net_units':float(Z[0,opt]),'final_maturity':float(score(evaluate()[1][opt])[0]),'equal_worst_net_units':float(worst[eq]),'greedy_worst_net_units':float(worst[gi]),'nominal_plan_worst_net_units':float(worst[nom]),'nominal_plan_overrun':bool((spend[nom]*1.2>budgets).any())}
plan=pd.DataFrame({'project':names,'units':levels[opt],'start_quarter':starts[opt]+1,'nominal_cost_units':costs[opt]}); plan.to_csv(ROOT/'results/optimal_plan.csv',index=False)
comparison=pd.DataFrame([{'plan':label,'nominal_net':Z[0,i],'worst_net':worst[i],'Q1_cost':spend[i,0],'Q2_cost':spend[i,1]} for label,i in [('Robust',opt),('Nominal',nom),('Equal',eq),('Greedy',gi)]]); comparison.to_csv(ROOT/'results/plan_comparison.csv',index=False)

# Held-out joint uncertainty: shared cost/effect shock; never used to optimize.
testrows=[]
for r in range(200):
    sev=rng.uniform(0,1); c=1+.3*sev; g=1-.3*sev; dd=int(rng.random()<.3); val=rng.uniform(.75,1.15)
    net,_=evaluate(c,g,dd,val,form='piecewise' if r%2 else 'exponential')
    f=(spend*c<=budgets).all(1)&(staff<=capacity).all(1)&dependency&recovery
    oracle=net[f].max()
    for label,i in [('Robust',opt),('Nominal',nom),('Equal',eq),('Greedy',gi)]:
        testrows.append({'draw':r,'plan':label,'net':net[i],'feasible':bool(f[i]),'regret':float(oracle-net[i]) if f[i] else np.nan})
td=pd.DataFrame(testrows); td.to_csv(ROOT/'results/heldout_decisions.csv',index=False)
out['heldout']=td.groupby('plan').agg(mean_net=('net','mean'),violation=('feasible',lambda x:1-x.mean()),mean_feasible_regret=('regret','mean')).round(6).to_dict('index')

# Seven scenario families plus budget/effect sensitivity.
sc=[('Balanced',np.array([.7,.7,.7]),0,0),('Weak governance',np.array([.7,.9,.3]),0,0),('Training pending',np.array([.45,.7,.7]),0,0),('Peak demand',np.array([.7,.7,.7]),1,0),('Shared outage',np.array([.7,.7,.7]),0,1)]
out['scenarios']=[{'scenario':lab,'score':float(score(a,l,s)[0])} for lab,a,l,s in sc]
out['diminishing']={'first_training_increment':float(G[0]*(1-np.exp(-rate[0]))),'third_training_increment':float(G[0]*(np.exp(-2*rate[0])-np.exp(-3*rate[0])))}
out['missing_bounds']={'month':40,'dimension':2,'low':float(y[39,2]/240),'high':float((y[39,2]+m[39,2])/240),'observed_only':float(y[39,2]/n[39,2])}
sens=[]
for factor in [.8,.9,1,1.1,1.2]:
    mask=(spend*1.2<=budgets*factor).all(1)&(staff<=capacity).all(1)&dependency&recovery
    ib=int(np.argmax(np.where(mask,worst,-np.inf)))
    sens.append({'budget_factor':factor,'best_worst_net':worst[ib],'fixed_plan_feasible':bool(mask[opt]),'selected_units':','.join(map(str,levels[ib].astype(int)))})
pd.DataFrame(sens).to_csv(ROOT/'results/budget_sensitivity.csv',index=False)
out['sensitivity']=sens
fig,axs=plt.subplots(1,2,figsize=(8,3.4))
ix=np.arange(4); axs[0].bar(ix-.18,comparison.nominal_net,width=.36,label='Nominal',color=COL[0]); axs[0].bar(ix+.18,comparison.worst_net,width=.36,label='Worst scenario',color=COL[2]); axs[0].set_xticks(ix,comparison.plan); axs[0].set_ylabel('Net benefit (USD 10,000)'); axs[0].legend(fontsize=10)
axs[1].plot([r['budget_factor'] for r in sens],[r['best_worst_net'] for r in sens],'o-',color=COL[0]); axs[1].set(xlabel='Budget multiplier',ylabel='Optimal worst net benefit'); axs[1].grid(alpha=.2)
fig.tight_layout(); fig.savefig(ROOT/'figures/decisions.pdf'); plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(8,3.4))
axs[0].barh([s['scenario'] for s in out['scenarios']],[s['score'] for s in out['scenarios']],color=[COL[0],COL[1],COL[2],COL[1],'#B94E48']); axs[0].set_xlim(0,100); axs[0].set_xlabel('Maturity / service score')
xx=np.linspace(0,4,150)
for j in [0,2,3]: axs[1].plot(xx,G[j]*(1-np.exp(-rate[j]*xx)),label=names[j],color=COL[[0,2,3].index(j)])
axs[1].legend(fontsize=10); axs[1].set(xlabel='Effective investment units',ylabel='Capability gain'); axs[1].grid(alpha=.2)
fig.tight_layout(); fig.savefig(ROOT/'figures/scenarios.pdf'); plt.close(fig)

# Structural tests: failure-selective missingness and extra measurement noise.
checks=[]
for noise in [.064,.08,.096]:
    aa=[]
    for d,fit in enumerate(fits):
        pp=[fit['phi'],fit['mu'],fit['beta']]; aa.append(expit(kfilter(pp,d,fit['delay'],noise)[0]))
    aa=np.array(aa).T; checks.append({'process_noise_sd':noise,'test_rmse':rmse(aa[test],truth[test]),'final_maturity':float(score(aa[-1])[0])})
out['noise_sensitivity']=checks
out['units']='Capability/probability: dimensionless; maturity: 0-100; cost/net: USD 10,000; staffing: capacity units.'
(ROOT/'results/metrics.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
