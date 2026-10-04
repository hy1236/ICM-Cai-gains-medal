"""Export numerical macros and bilingual LaTeX tables from saved model results."""
from pathlib import Path
import json
import pandas as pd
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'results/metrics.json').read_text())
s=m['state']; c=m['chain']; o=m['optimization']
nums={'StateRMSE':f"{s['test_filtered_rmse']:.4f}",'RawRMSE':f"{s['test_raw_rmse']:.4f}",'ZeroRMSE':f"{s['test_zero_lag_rmse']:.4f}",'ForecastRMSE':f"{s['test_forecast_rmse']:.4f}",'Coverage':f"{100*s['conditional_90_coverage']:.1f}",'BrierImport':f"{c['metrics'][0]['brier']:.4f}",'BrierExport':f"{c['metrics'][1]['brier']:.4f}",'BaseMaturity':f"{c['baseline_maturity']:.2f}",'PlanCost':f"{sum(o['quarter_spend']):.2f}",'PlanDollars':f"{10000*sum(o['quarter_spend']):,.0f}",'WorstNet':f"{o['worst_net_units']:.4f}",'EqualNet':f"{o['equal_worst_net_units']:.4f}",'FinalMaturity':f"{o['final_maturity']:.2f}",'MaturityGain':f"{o['final_maturity']-c['baseline_maturity']:.2f}"}
(R/'results/metrics.tex').write_text('\n'.join('\\newcommand{\\'+k+'}{'+v+'}' for k,v in nums.items()),encoding='utf-8')
def table(path,caption,cols,head,rows):
    text='\\par\\begin{table}[!htbp]\\centering\\small\\caption{'+caption+'}\n\\begin{tabular}{'+cols+'}\\toprule\n'+head+r'\\\midrule'+'\n'+'\n'.join(' & '.join(row)+r'\\' for row in rows)+'\n\\bottomrule\\end{tabular}\\end{table}\\par\n'
    (R/'results'/path).write_text(text,encoding='utf-8')
df=pd.read_csv(R/'results/optimal_plan.csv'); trans={'Training':'培训','Hiring':'招聘','Integration':'系统集成','Governance':'数据治理','Recovery':'恢复能力'}
table('plan_table.tex',r'\bi{Selected project menu; inactive projects have no start date.}{选定项目菜单；未启动项目不指定时间。}','lrrr',r'\bi{Project}{项目}&\bi{Units}{投入单位}&\bi{Start quarter}{启动季度}&\bi{Cost}{成本}',[[r'\bi{'+r.project+'}{'+trans[r.project]+'}',str(int(r.units)),str(int(r.start_quarter)) if r.units else '--',f'{r.nominal_cost_units:.2f}'] for r in df.itertuples()])
df=pd.read_csv(R/'results/plan_comparison.csv'); tr={'Robust':'稳健','Nominal':'名义','Equal':'等额','Greedy':'贪心'}
table('comparison_table.tex',r'\bi{Finite-menu comparison in USD 10,000 units.}{有限菜单比较，单位为万美元。}','lrrr',r'\bi{Plan}{方案}&\bi{Nominal net}{名义净收益}&\bi{Worst net}{最坏净收益}&\bi{Q1 spend}{首季支出}',[[r'\bi{'+r.plan+'}{'+tr[r.plan]+'}',f'{r.nominal_net:.4f}',f'{r.worst_net:.4f}',f'{r.Q1_cost:.2f}'] for r in df.itertuples()])
table('heldout_table.tex',r'\bi{Wider held-out scenarios: budget reliability and feasible regret.}{更宽留出情景中的预算可靠性与可行时后悔值。}','lrrr',r'\bi{Plan}{方案}&\bi{Mean net}{平均净收益}&\bi{Violation rate}{违约率}&\bi{Mean feasible regret}{可行时平均后悔值}',[[r'\bi{'+name+'}{'+tr[name]+'}',f"{z['mean_net']:.3f}",f"{100*z['violation']:.1f}"+r'\%',f"{z['mean_feasible_regret']:.3f}"] for name,z in m['heldout'].items()])
print('Exported macros and 3 tables.')
