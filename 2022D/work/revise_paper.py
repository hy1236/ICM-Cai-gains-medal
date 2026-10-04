from pathlib import Path
R=Path('F:/ACMCM/2022D/delivery/ICM2022D_Revised')
p=(R/'paper.tex').read_text(encoding='utf-8-sig')
def replace(a,b):
 global p
 assert a in p,a[:100]
 p=p.replace(a,b)
start=p.index('\\bi{\nA port can own')
end=p.index('\\par\\smallskip\\noindent\\textbf{\\bi{Keywords}',start)
p=p[:start]+r'''\bi{
ICM Corporation needs to evaluate its data and analytics maturity, identify feasible improvements, establish monitoring protocols, and adapt the assessment to other ports and trucking firms. To address these tasks, we build four models: a coverage-constrained indicator selection model and three linked models for capability estimation, chain reliability, and robust resource allocation. Because the company withholds numerical records, the framework is demonstrated with explicitly labeled synthetic data.

First, we map port operations to nine information-management requirements and construct a dictionary of 16 indicators. The coverage model retains ten high-frequency indicators while reducing illustrative collection cost from 29 to 17 units. We then establish event identifiers, source records, missing-data bounds, and versioned processing rules. Deduplication yields 34,560 unique audit events, including 987 unknown outcomes that remain in the expected-event denominator.

Next, the Lag-aware Capability Filter (LCF) uses monthly audit counts to estimate people, technology, and process capability. The state equation combines persistence and delayed action effects, while the observation equation adjusts for workload and sample size. The resulting final capability profile is $(0.4823,0.5384,0.4070)$, providing a common input for the maturity assessment rather than three unrelated KPI scores.

Then, the Chain Reliability Maturity (CRM) model links those capabilities to timely, correct import and export handoffs. It incorporates a people--process interaction and a shared-outage effect. Fixed reference conditions give a comparable maturity score of \BaseMaturity/100 in the demonstration, while separate operational scores reveal current workload and outage risks. The score is not presented as ICM's observed maturity.

Furthermore, the Robust Improvement Portfolio (RIP) model combines diminishing returns, implementation delays, dependencies, staffing, and quarterly budgets. Enumerating 16,807 menus selects training, governance, and recovery investments costing \PlanCost\ units, with a worst planning-scenario net benefit of \WorstNet\ units; one unit represents USD 10,000. Nominal maturity rises to \FinalMaturity/100. We translate the decision process into a monitoring protocol and explain how compatible handoff measures support different port sizes and trucking partners.

Finally, model testing covers temporal prediction, probability calibration, parameter sensitivity, and held-out decision scenarios. Filtered capability RMSE is \StateRMSE, versus \RawRMSE\ for direct monthly estimates; delayed forecast RMSE is \ForecastRMSE, versus \ZeroRMSE\ without onset delay. The two chain Brier scores are \BrierImport\ and \BrierExport. Tests also identify boundaries: nominal 90\% state intervals cover only \Coverage\% of test states, and the robust menu violates budget in 5\% of wider stress cases. These results support the framework's comparative use while requiring recalibration before enterprise deployment.
}{
ICM公司需要评价数据与分析系统的成熟度，制定资源约束下的改进方案，建立持续监测协议，并将评价体系推广到不同规模港口及卡车运输企业。针对这些任务，本文建立四个模型：业务覆盖约束下的指标筛选模型，以及能力状态估计、业务链可靠性成熟度评价和稳健资源优化三个相互衔接的模型。由于企业没有提供数值记录，本文使用明确标记的情景数据演示模型运行过程。

首先，将港口业务映射为九类信息管理需求，构建16项指标字典，通过覆盖约束模型选出10项高频指标，将示例采集成本从29单位降至17单位。随后统一事件编号、来源记录、缺失边界和处理规则；去重得到34,560条唯一审核事件，并保留987条未知结果，使缺失记录不从应统计分母中消失。

然后，建立含滞后的能力滤波模型（LCF），以月度审核计数估计人员、技术和流程能力。状态方程同时描述能力持续性与行动延迟，观测方程调整负荷和样本量差异，得到期末能力画像$(0.4823,0.5384,0.4070)$，为后续成熟度评价提供统一输入。

在此基础上，建立业务链可靠性成熟度模型（CRM），将三维能力映射为进出口交接及时、准确完成的概率，并纳入人员与流程交互及共享故障效应。参考环境下的示例成熟度为\BaseMaturity/100；另行报告实际负荷和故障条件下的运营分数，以区分能力差异与当前运营风险。该示例评分不作为ICM的真实观测结果。

此外，建立稳健改进组合模型（RIP），综合考虑边际收益递减、实施延迟、项目依赖、人力和季度预算。枚举16,807种菜单后，选出培训、治理与恢复能力组合，名义投入\PlanCost\ 单位，最坏规划情景净收益\WorstNet\ 单位，每单位为1万美元；名义成熟度提高至\FinalMaturity/100。最后将决策流程落实为监测协议，并通过兼容的交接指标支持大小港口和运输企业迁移。

模型检验方面，分别开展时序预测、概率校准、参数灵敏度与留出决策情景检验。能力估计RMSE为\StateRMSE，低于直接月度估计的\RawRMSE；含延迟预测RMSE为\ForecastRMSE，低于无起效延迟的\ZeroRMSE；两条业务链Brier分数为\BrierImport\ 和\BrierExport。同时，名义90\%状态区间实际覆盖率仅为\Coverage\%，更宽压力情景下预算违约率为5\%。这些结果说明模型能够支持方案比较，但企业部署前仍需校准不确定性和风险边界。
}
''' +p[end:]
# Rebuild the hierarchy; only essential computations receive third-level headings.
replace(r'\pagepart{Indicator dictionary and coverage-constrained screening}{指标字典与业务覆盖筛选}',r'\pagepart{Data preparation and indicator selection}{数据准备与指标筛选}'+'\n'+r'\subpart{Indicator dictionary and coverage model}{指标字典与覆盖筛选模型}')
replace(r'\pagepart{Collection protocol and confidentiality}{数据采集协议与保密设计}',r'\subpart{Collection protocol and confidentiality}{数据采集协议与保密设计}')
replace(r'\subpart{Collect the denominator as carefully as the numerator}{分母与分子同等重要}',r'\thirdpart{Event registry and confidentiality}{事件清单与保密设计}')
replace(r'\subpart{Stratified manual audits}{分层人工核验}',r'\thirdpart{Stratified manual audits}{分层人工核验}')
replace(r'\pagepart{Processing: preserve errors without rewarding missingness}{数据处理：保留真实异常，避免缺失造成虚高}',r'\subpart{Cleaning, missingness, and audit checks}{清洗、缺失处理与审计}')
replace(r'\subpart{Partial identification of a pass rate}{通过率的部分识别}',r'\paragraph{\bi{Missing-data bounds.}{缺失数据边界。}}')
replace(r'\pagepart{LCF results and its failed uncertainty check}{能力滤波结果与未通过的不确定性检验}',r'\subpart{Comparing capability models on the same test period}{同一测试期的能力模型对比}')
replace(r'\pagepart{CRM calibration and uncertainty transfer}{成熟度校准与不确定性传递}',r'\subpart{Reliability model comparison and uncertainty transfer}{可靠性模型对比与不确定性传递}')
replace(r'\pagepart{Model II: Chain Reliability Maturity (CRM)}{模型二：业务链可靠性成熟度模型（CRM）}',r'\pagepart{Model II: Chain Reliability Maturity (CRM)}{模型二：业务链可靠性成熟度模型（CRM）}'+'\n'+r'\subpart{Chain probability and interaction effects}{业务链概率与交互效应}')
replace(r'\pagepart{RIP parameters and the selected implementation menu}{优化参数与选定实施菜单}',r'\subpart{Parameters and the selected project menu}{参数设置与选定项目组合}')
replace(r'\pagepart{Decision validation and the price of robustness}{决策检验与稳健性的代价}',r'\subpart{Comparing resource-allocation models}{资源配置模型对比}'+'\n'+r'\thirdpart{Nominal and worst-scenario comparison}{名义情景与最坏情景比较}')
replace(r'\begingroup\small','')
replace(r'\subpart{Held-out joint shocks}{留出的联合冲击}',r'\thirdpart{Held-out joint shocks}{留出的联合冲击}')
replace(r'\endgroup','')
replace(r'\pagepart{Seven scenario families and structural stress tests}{七类情景与结构压力测试}',r'\pagepart{Model testing and sensitivity analysis}{模型检验与灵敏度分析}'+'\n'+r'\subpart{Seven scenario families and structural stress tests}{七类情景与结构压力测试}')
replace(r'\pagepart{Sensitivity, identification, and evidence ledger}{灵敏度、可识别性与证据账本}','')
replace(r'\subpart{What changes a decision?}{哪些变化会改变决策？}',r'\subpart{Budget and state-noise sensitivity}{预算与状态噪声灵敏度}')
replace(r'\pagepart{Turning the score into people and technology decisions}{把评分转化为人员与技术决策}',r'\pagepart{Implementation and continuous monitoring}{实施方案与持续监测}')
replace(r'\pagepart{Governance, monitoring, and a phased implementation}{治理、持续监测与分阶段实施}',r'\subpart{Governance and monitoring protocol}{治理与监测协议}')
# Remove repetitive five-item limitations; finish the whole article with one
# balanced evaluation paragraph containing exactly two substantive limitations.
start=p.index(r'\pagepart{Evaluation, limitations, and recommendations}')
end=p.index(r'\clearpage\section{\bi{Letter',start)
p=p[:start]+p[end:]
final=r'''
\pagepart{Overall model evaluation}{模型综合评价}
\bi{The framework has four practical strengths. First, requirement coverage links every selected indicator to a business need, while mandatory governance and recovery checks remain protected. Second, the three core models form a traceable chain from audit records to capability states, service probabilities, and feasible investments. Third, explicit delays, diminishing returns, and quarterly constraints make the recommended menu operationally interpretable. Fourth, saved code, source counts, comparison models, and sensitivity results make both versions reproducible. Two limitations remain: the synthetic scenarios and finite project menu cannot fully represent the diversity of real ports; and the current uncertainty estimates require further calibration, as shown by 66.7\% state-interval coverage and 5\% budget violations outside the planning envelope. The next deployment step is therefore an independently audited enterprise pilot, using real event records and cost data to recalibrate the same framework.}{本文模型具有四方面优势：其一，指标由业务需求出发筛选，在降低采集成本的同时保留治理与恢复等强制检查；其二，三个核心模型形成“审核记录—能力状态—服务概率—资源决策”的可追溯链条，便于解释评分与投资依据；其三，显式纳入实施滞后、边际收益递减和分期资源约束，使方案更贴近实际管理过程；其四，完整代码、原始计数、对比模型与灵敏度结果均可复现，中英文稿使用相同数值来源。模型的局限主要有两点：一是模拟场景和有限项目菜单尚不能全面覆盖真实港口的业务差异；二是不确定性仍需校准，表现为状态区间覆盖率66.7\%，以及规划边界之外5\%的预算违约率。因此，实际部署应先开展独立审核的企业试点，以真实事件记录和成本数据重新校准模型。}
'''
replace(r'\end{document}',final+'\n'+r'\end{document}')
# Complete and explain multi-stage calculations.
start=p.index(r'\begin{equation}'+'\n'+r'\widehat p=')
end=p.index(r'\end{equation}',start)+len(r'\end{equation}')
p=p[:start]+r'''\paragraph{Step 1: \bi{calculate stratum weights}{计算分层权重}}
\bi{Let $N_h$ and $n_h$ denote the population and sample size of stratum $h$, and $y_h$ its observed passes. Calculate the population weight $W_h$ and the sample pass rate $\widehat p_h$:}{设$N_h$、$n_h$分别为第$h$层总体量和样本量，$y_h$为通过数。先计算总体权重$W_h$及层内通过率$\widehat p_h$：}
\begin{equation}W_h=\frac{N_h}{\sum_{g=1}^{H}N_g},\qquad \widehat p_h=\frac{y_h}{n_h}.\end{equation}
\paragraph{Step 2: \bi{aggregate the estimate}{汇总通过率}}
\bi{The weighted estimate uses population composition rather than the observed response mix:}{按总体结构而非实际响应结构加权，得到整体通过率：}
\begin{equation}\widehat p=\sum_{h=1}^{H}W_h\widehat p_h.\end{equation}
\paragraph{Step 3: \bi{quantify sampling variance}{计算抽样方差}}
\bi{For independent sampling within strata, let $s_h^2$ be the unbiased sample variance of the binary outcomes. The finite-population correction accounts for sampling without replacement:}{若层内独立抽样，令$s_h^2$为二元结果的无偏样本方差；有限总体修正项用于不放回抽样：}
\begin{equation}s_h^2=\frac{n_h}{n_h-1}\widehat p_h(1-\widehat p_h),\qquad
\widehat{\operatorname{Var}}(\widehat p)=\sum_{h=1}^{H}W_h^2\left(1-\frac{n_h}{N_h}\right)\frac{s_h^2}{n_h},\quad n_h>1.\end{equation}
''' +p[end:]
# State model: specify link and all transition parameters.
anchor=r'\subpart{From actions to latent capability}{从行动到潜在能力}'
replace(anchor,anchor+'\n'+r'''\bi{The logistic link maps an unrestricted latent state to a capability between zero and one:}{逻辑函数把无界潜在状态转化为零到一之间的能力：}
\begin{equation}a_{dt}=\sigma(z_{dt})=\frac{1}{1+\exp(-z_{dt})}.\end{equation}
\bi{In the transition below, $\phi_d$ is persistence, $\mu_d$ is the baseline logit, $\beta_d$ is action strength, and $Q$ is state-disturbance variance. $u_{dt}$ records an action, and $\delta_d$ gives its onset delay.}{以下转移式中，$\phi_d$为持续性，$\mu_d$为基准对数几率，$\beta_d$为行动强度，$Q$为状态扰动方差；$u_{dt}$记录行动量，$\delta_d$为起效延迟。}''')
start=p.index(r'\begin{align}'+'\n'+r'z_{dt}')
end=p.index(r'\end{align}',start)+len(r'\end{align}')
p=p[:start]+r'''\paragraph{Step 1: \bi{form the delayed input}{计算滞后有效行动量}}
\bi{Use the onset delay and the normalized weights $(1,0.6,0.36)$ to combine three action months:}{按起效延迟及归一化权重$(1,0.6,0.36)$汇总三个月行动：}
\begin{equation}\widetilde u_{dt}=\frac{\sum_{\ell=0}^{2}0.6^\ell u_{d,t-\delta_d-\ell}}{1+0.6+0.6^2},\qquad u_{dt}=0\quad(t<1).\end{equation}
\paragraph{Step 2: \bi{evolve capability}{更新潜在能力}}
\bi{The previous state, baseline reversion, and delayed action determine the next state:}{上一期状态、基准回归及滞后行动共同确定下一期潜在状态：}
\begin{equation}z_{dt}=\phi_dz_{d,t-1}+(1-\phi_d)\mu_d+\beta_d\widetilde u_{dt}+\eta_{dt},\qquad \eta_{dt}\sim N(0,Q).\label{eq:state}\end{equation}
''' +p[end:]
start=p.index(r'\subpart{An explicit working approximation}')
end=p.index(r'\algo{1}',start)
p=p[:start]+r'''\subpart{Stepwise filtering calculation}{滤波计算步骤}
\bi{We use an empirical-logit Gaussian working approximation. The following steps are applied separately to each dimension; the dimension subscript is suppressed for readability.}{本文使用经验对数几率的高斯工作近似。以下步骤分别用于每个维度，为使公式清晰，暂时省略维度下标。}
\thirdpart{Step 1: construct the observation and its variance}{Step 1：构造观测量及其方差}
\bi{Given passes $Y_t$, observed trials $N_t$, and workload $c_t$, add a half-count correction to avoid infinite logits. $r_t$ is the workload-adjusted observation, and $R_t$ is its working variance:}{给定通过数$Y_t$、有效样本量$N_t$及负荷$c_t$，加入半计数修正以避免无穷对数几率。$r_t$为负荷调整后的观测量，$R_t$为其工作方差：}
\begin{equation}r_t=\log\frac{Y_t+1/2}{N_t-Y_t+1/2}+0.25c_t,\qquad
R_t=\frac{1}{Y_t+1/2}+\frac{1}{N_t-Y_t+1/2}.\end{equation}
\bi{The approximation is $r_t\approx z_t+\epsilon_t$, with $\epsilon_t\sim N(0,R_t)$. Small or extreme counts require a binomial filter in a later deployment.}{工作近似为$r_t\approx z_t+\epsilon_t$，其中$\epsilon_t\sim N(0,R_t)$。实际部署中，样本过小或通过率极端时应采用二项滤波。}
\thirdpart{Step 2: predict the state}{Step 2：计算先验状态}
\bi{Given the preceding mean $m_{t-1}$ and variance $V_{t-1}$, apply the fitted persistence, baseline, action strength, and disturbance variance:}{给定前一期均值$m_{t-1}$和方差$V_{t-1}$，代入拟合的持续性、基准、行动强度及扰动方差：}
\begin{equation}m_t^-=\phi m_{t-1}+(1-\phi)\mu+\beta\widetilde u_t,\qquad V_t^-=\phi^2V_{t-1}+Q.\end{equation}
\bi{The implementation initializes $m_0=\mu$, $V_0=0.5$. These predictions use only information available before the current observation.}{实现中初始化$m_0=\mu$、$V_0=0.5$。先验预测只使用当期观测到达之前的信息。}
\thirdpart{Step 3: update the state and report capability}{Step 3：更新状态并输出能力}
\bi{First calculate innovation variance $S_t$ and Kalman gain $K_t$, which weight the new observation relative to the prior:}{先计算创新方差$S_t$及Kalman增益$K_t$，用于确定新观测相对于先验的权重：}
\begin{equation}S_t=V_t^-+R_t,\qquad K_t=\frac{V_t^-}{S_t}.\end{equation}
\bi{Then combine the prediction and innovation $r_t-m_t^-$ to obtain posterior mean and variance:}{再将预测与创新$r_t-m_t^-$结合，得到后验均值与方差：}
\begin{equation}m_t=m_t^-+K_t(r_t-m_t^-),\qquad V_t=(1-K_t)V_t^-.\end{equation}
\bi{Finally convert the logit state into capability and a nominal 90\% conditional interval:}{最后将对数几率状态转为能力和名义90\%条件区间：}
\begin{equation}\widehat a_t=\frac{1}{1+e^{-m_t}},\qquad
I_t^{90}=\left[\frac{1}{1+e^{-(m_t-1.645\sqrt{V_t})}},\frac{1}{1+e^{-(m_t+1.645\sqrt{V_t})}}\right].\end{equation}
\bi{For each candidate delay, fit $\theta=(\phi,\mu,\beta)$ by minimizing the training innovation loss below; select the delay using the same loss on validation months. The loss explicitly accounts for innovation variance:}{对每个候选延迟，最小化以下训练创新损失估计$\theta=(\phi,\mu,\beta)$，再以验证月份的同一损失选择延迟。该损失显式考虑创新方差：}
\begin{equation}\widehat\theta_\delta=\arg\min_{\theta}\frac12\sum_{t=1}^{24}\left[\log S_t+\frac{(r_t-m_t^-)^2}{S_t}\right],\quad
0.5\le\phi\le0.98,\;-2\le\mu\le2,\;0\le\beta\le0.6.\end{equation}
''' +p[end:]
# Figure interpretation and labels, before each figure.
replace(r'\end{tikzpicture}\caption{',r'\end{tikzpicture}\caption{')
needle=r'\end{tikzpicture}\caption{\bi{The evidence-to-decision loop. Intervals and source versions accompany each transfer.}{从证据到决策的闭环；各阶段传递区间及来源版本。}}'
replace(needle,needle+r'\label{fig:framework}')
needle=r'\begin{figure}[H]\centering'+'\n'+r'\begin{tikzpicture}'
replace(needle,r'\bi{Figure~\ref{fig:framework} shows how indicator records feed the capability filter, how capabilities determine chain reliability, and how the investment decision returns to monitoring. The feedback arrow represents updating evidence and model parameters after implementation.}{图\ref{fig:framework}展示指标记录如何进入能力滤波、能力如何影响业务链可靠性，以及投资实施后如何反馈到监测。回流箭头表示使用实施后的新证据更新参数与决策。}'+'\n'+needle)
explanations={
'state':r'\bi{Figure~\ref{fig:state} compares recovered capabilities with the known synthetic trajectories. Its three panels represent people, technology, and process; the shaded months form the common test set for the direct monthly, zero-delay, and delayed models compared below.}{图\ref{fig:state}比较估计能力与模拟真值，三个子图分别对应人员、技术和流程。阴影月份为共同测试集，以下直接月度估计、无起效延迟模型及含延迟模型均在该区间比较。}',
'calibration':r'\bi{Figure~\ref{fig:calibration} compares predicted and observed success within probability bins for both chains. Points close to the diagonal indicate better calibration; larger markers represent more test cases. The constant-frequency baseline and CRM are evaluated on the same 300 profiles.}{图\ref{fig:calibration}分别比较两条业务链各概率区间的预测成功率与实际成功率，点越接近对角线表示校准越好，点越大表示样本越多。常数频率基线与CRM均使用相同的300个测试画像。}',
'decisions':r'\bi{Figure~\ref{fig:decisions} compares four allocation models on the same projects and cost assumptions. The left panel separates nominal and worst-case returns; the right panel shows how reoptimization changes worst-case return as budget varies.}{图\ref{fig:decisions}在同一项目集合与成本假设下比较四类配置模型。左图区分名义与最坏情景收益，右图显示预算改变并重新优化后最坏收益的变化。}',
'scenarios':r'\bi{Figure~\ref{fig:scenarios} shows the effects of capability imbalance and operational shocks on service scores, followed by investment-response curves. The flattening curves explain why concentrating every additional unit in one project becomes less attractive.}{图\ref{fig:scenarios}左图展示能力失衡及运营冲击对评分的影响，右图给出投入响应曲线。曲线逐渐变平，解释了为何不断向同一项目追加投资的吸引力会降低。}'}
for name,explanation in explanations.items():
 import re
 pattern=r'(?m)^\\fig\{[^\n]+\}\{'+name+r'\}\{[^\n]+$'
 match=re.search(pattern,p);assert match,name
 p=p[:match.start()]+explanation+'\n'+match.group()+p[match.end():]
# Complete response calculation with local explanations.
start=p.index(r'\begin{align}'+'\n'+r'f_{jq}')
end=p.index(r'\end{align}',start)+len(r'\end{align}')
p=p[:start]+r'''\paragraph{Step 1: \bi{calculate effective investment}{计算有效投入}}
\bi{Let $d_j$ be the project-specific delay and $\Delta_s$ the extra scenario delay. $f_{jq}^{(s)}$ is the realized fraction of an investment by quarter $q$, rising over two quarters; $E_{jq}^{(s)}$ is its effective amount:}{令$d_j$为项目自身延迟，$\Delta_s$为情景额外延期；$f_{jq}^{(s)}$表示截至$q$季度在两季度内逐步实现的投入比例，$E_{jq}^{(s)}$为有效投入：}
\begin{equation}f_{jq}^{(s)}=\min\left\{1,\max\left(0,\frac{q-s_j-d_j-\Delta_s+1}{2}\right)\right\},\qquad E_{jq}^{(s)}=x_jf_{jq}^{(s)}.\end{equation}
\paragraph{Step 2: \bi{calculate diminishing capability gains}{计算递减的能力收益}}
\bi{With gain ceiling $G_j^{(s)}$ and conversion rate $k_j$, the response and its derivatives are}{给定情景收益上限$G_j^{(s)}$及转化系数$k_j$，能力响应及其导数为}
\begin{align}g_j^{(s)}(E)&=G_j^{(s)}(1-e^{-k_jE}),\\
\frac{dg_j^{(s)}}{dE}&=G_j^{(s)}k_je^{-k_jE}>0,\qquad
\frac{d^2g_j^{(s)}}{dE^2}=-G_j^{(s)}k_j^2e^{-k_jE}<0.\end{align}
\bi{Thus additional investment increases capability, but each increment contributes less than the previous one.}{因此，追加投入仍提高能力，但每次增量的贡献逐渐减少。}
\paragraph{Step 3: \bi{combine project contributions}{汇总项目贡献}}
\bi{Let $m_{jd}$ be project $j$'s allocation to capability $d$, and $a_d^{0,(s)}$ the scenario baseline. Add realized contributions once and cap the probability-scale state:}{令$m_{jd}$为项目$j$对能力$d$的作用比例，$a_d^{0,(s)}$为情景基准；对已实现贡献仅累加一次，并限制概率尺度状态：}
\begin{equation}a_{dq}^{(s)}(x)=\min\left\{0.995,\max\left[0,a_d^{0,(s)}+\sum_jm_{jd}g_j^{(s)}(E_{jq}^{(s)})\right]\right\}.\label{eq:gain}\end{equation}
''' +p[end:]
# Monetary cost formula was implicit in the old text; specify it explicitly.
needle=r'\subpart{Monetary objective and feasibility}{货币目标与可行性}'
replace(needle,needle+'\n'+r'''\paragraph{Step 1: \bi{calculate quarterly project costs}{计算季度项目成本}}
\bi{For scenario cost multiplier $\kappa_s$, investment $x_j$, and activation $y_j=\mathbf1(x_j>0)$, the cost includes a fixed 0.15-unit startup charge:}{给定情景成本倍率$\kappa_s$、投入$x_j$及启动变量$y_j=\mathbf1(x_j>0)$，季度成本包含每项目0.15单位固定启动费：}
\begin{equation}C_q^{(s)}(x)=\sum_{j:s_j=q}\kappa_s(x_j+0.15y_j).\end{equation}
\paragraph{Step 2: \bi{calculate discounted net benefit}{计算折现净收益}}
''')
needle=r'\begin{align}'+'\n'+r'\max_{x,s,v}'
replace(needle,r'\paragraph{Step 3: \bi{optimize the worst-case feasible return}{优化最坏情景可行收益}}'+'\n'+r'\bi{Here $v$ is the guaranteed planning-scenario net benefit, $B_q$ is budget, $h_j$ is unit staff usage, and $H_q$ is available staff capacity. Each constraint has a separate management meaning:}{其中$v$为规划情景内保证的净收益，$B_q$为预算，$h_j$为单位投入人力需求，$H_q$为可用人力容量。各约束分别对应以下管理含义：}'+'\n'+needle)
needle=r'\end{align}'+'\n'+r'\bi{A recovery floor'
replace(needle,r'''\end{align}
\bi{The first line maximizes the minimum scenario return. The second enforces quarterly budget and staffing capacity. The third requires a governance foundation before or alongside integration. The final line guarantees a minimum recovery project.}{第一行最大化各情景净收益的下界；第二行限制每季度预算与人力；第三行要求集成之前或同期开启治理基础；最后一行保证最低恢复投入。}
\bi{A recovery floor''')
# Fully define the metrics used in comparisons and do not split competing models.
needle=r'\subpart{Comparing capability models on the same test period}{同一测试期的能力模型对比}'
replace(needle,needle+'\n'+r'''\bi{For test states indexed by $\mathcal T$, RMSE measures average capability error and coverage measures how often the known generating state falls within the reported interval:}{对索引集合$\mathcal T$中的测试状态，RMSE衡量平均能力误差，覆盖率衡量生成真值落入报告区间的比例：}
\begin{equation}\operatorname{RMSE}=\sqrt{\frac{1}{|\mathcal T|}\sum_{(d,t)\in\mathcal T}(\widehat a_{dt}-a_{dt}^{\rm true})^2},\qquad
\operatorname{Coverage}=\frac{1}{|\mathcal T|}\sum_{(d,t)\in\mathcal T}\mathbf1\{a_{dt}^{\rm true}\in I_{dt}^{90}\}.\end{equation}
''')
needle=r'\subpart{Reliability model comparison and uncertainty transfer}{可靠性模型对比与不确定性传递}'
replace(needle,needle+'\n'+r'''\bi{For $n$ held-out handoffs, let $p_i$ be predicted success and $y_i\in\{0,1\}$ the observed outcome. Both scores penalize inaccurate probabilities; lower is better:}{对$n$项留出交接，令$p_i$为预测成功率、$y_i\in\{0,1\}$为实际结果。以下两项指标均惩罚不准确的概率，越小越好：}
\begin{align}\operatorname{Brier}&=\frac1n\sum_{i=1}^{n}(p_i-y_i)^2,\\
\operatorname{LogLoss}&=-\frac1n\sum_{i=1}^{n}\left[y_i\log p_i+(1-y_i)\log(1-p_i)\right].\end{align}
''')
needle=r'\input{results/heldout_table.tex}'
replace(needle,r'''\bi{For a feasible decision $x$ in scenario $s$, regret is the difference from the best menu that is feasible in that same scenario:}{对情景$s$中的可行决策$x$，后悔值为同一情景最优可行菜单与该决策净收益之差：}
\begin{equation}\operatorname{Regret}_s(x)=\max_{x'\in\mathcal F_s} Z_s(x')-Z_s(x),\qquad x\in\mathcal F_s.\end{equation}
\bi{Here $\mathcal F_s$ is the scenario-specific feasible set. Infeasible decisions are counted as violations rather than assigned regret.}{其中$\mathcal F_s$为情景可行集；不可行决策计为违约，不赋予后悔值。}
'''+needle)
# Capture evidence classes once per section rather than page-dependent notes.
p=p.replace(r'\noindent\emph{\simnote}',r'\noindent\emph{\bi{The following numerical experiments use synthetic data.}{以下数值实验均使用情景数据。}}')
# Reference/appendix transitions flow naturally; customer letter remains 1 page.
p=p.replace('\\vfill\n\\noindent\\bi{\\textbf{Reading note.}', '\\medskip\n\\noindent\\bi{\\textbf{Reading note.}')
p=p.replace('\\clearpage\n\\renewcommand{\\refname}', '\\clearpage\n\\renewcommand{\\refname}')
p=p.replace(r'\begin{table}[H]',r'\begin{table}[!htbp]').replace(r'\begin{figure}[H]',r'\begin{figure}[!htbp]')
# Finish TOC explicitly, not at every section.
needle=r'\pagepart{Introduction: measure the handoff, not the software}'
replace(needle,r'\clearpage'+'\n'+needle)
(R/'paper.tex').write_text(p,encoding='utf-8')
pre=(R/'preamble.tex').read_text(encoding='utf-8')
pre=pre.replace(r'\setlength{\parskip}{4.5pt}',r'\setlength{\parskip}{1pt}')
pre=pre.replace(r'\setcounter{tocdepth}{1}',r'''\setcounter{tocdepth}{3}
\setcounter{secnumdepth}{3}
\usepackage{titlesec,placeins}
\titlespacing*{\section}{0pt}{10pt plus 2pt minus 2pt}{5pt}
\titlespacing*{\subsection}{0pt}{7pt plus 1pt minus 1pt}{3pt}
\titlespacing*{\subsubsection}{0pt}{5pt plus 1pt minus 1pt}{2pt}
\titlespacing*{\paragraph}{0pt}{4pt}{0.6em}
\setlength{\textfloatsep}{9pt plus 2pt minus 2pt}
\setlength{\intextsep}{7pt plus 2pt minus 2pt}
\setlength{\floatsep}{7pt plus 2pt minus 2pt}
\setlength{\abovecaptionskip}{4pt}
\setlength{\belowcaptionskip}{2pt}
\renewcommand{\topfraction}{0.9}
\renewcommand{\bottomfraction}{0.85}
\renewcommand{\textfraction}{0.08}
\renewcommand{\floatpagefraction}{0.8}
\raggedbottom
\makeatletter
\renewcommand\l@section{\@dottedtocline{1}{0em}{1.7em}}
\renewcommand\l@subsection{\@dottedtocline{2}{1.7em}{2.7em}}
\renewcommand\l@subsubsection{\@dottedtocline{3}{4.4em}{3.5em}}
\makeatother''')
pre=pre.replace(r'\clearpage\section{\bi{#1}{#2}}',r'\FloatBarrier\section{\bi{#1}{#2}}')
pre=pre.replace(r'\newcommand{\subpart}',r'\newcommand{\thirdpart}[2]{\subsubsection{\bi{#1}{#2}}}'+'\n'+r'\newcommand{\subpart}')
pre=pre.replace(r'\begin{figure}[H]',r'\begin{figure}[!htbp]')
pre=pre.replace(r'\caption{#3}\end{figure}',r'\caption{#3}\label{fig:#2}\end{figure}')
(R/'preamble.tex').write_text(pre,encoding='utf-8')
# Table exporter follows the same float policy on regeneration.
for f in [R/'code/export_tables.py',*list((R/'results').glob('*table.tex'))]:
 t=f.read_text(encoding='utf-8');t=t.replace('[H]','[!htbp]');f.write_text(t,encoding='utf-8')
print('Revision complete: hierarchy, abstract, equations, figure explanation, final evaluation, continuous layout.')
