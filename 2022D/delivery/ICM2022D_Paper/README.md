# 2022 ICM D：中英文论文与 LaTeX 交付包

## 先阅读

- `main_en.pdf`：英文最终交付版，23 页，含摘要、目录、客户信、参考文献和 AI 使用说明。
- `main_zh.pdf`：中文对应版，23 页，正文结论、公式、数据与英文版一致；图内使用统一英文标签，图题及分析为中文。
- 论文研究 **2022 ICM D**。提供的 2023 年 O 奖论文只用于版式参考。
- **全部实验数据为模拟数据，不代表 ICM 公司的实际成熟度。** 未进行企业实地调查或专家访谈。
- 未提供真实队号，页眉使用 `UNASSIGNED`。如需填写，在 `preamble.tex` 修改 `\TeamNumber`，不要使用参考论文的队号。

## 结构

```text
main_en.pdf / main_zh.pdf    两版已编译论文
main_en.tex / main_zh.tex    两个编译入口
paper.tex                   共用中英双语正文
preamble.tex                版式、字体与队号
build.ps1 / build.sh         Windows / macOS、Linux 编译脚本
figures/                    正文实际引用的 4 个矢量图
code/                       完整复现程序、表格导出、核验程序和依赖版本
data/                       情景事件、画像、KPI 和指标覆盖表
results/                    模型输出、论文数值宏与表格
README.md                   使用说明
思路分析与交付说明.md         原方案分析、修正和实现边界
```

## 仅编译论文

需要 XeLaTeX，建议使用包含 ctex、Fandol、TikZ 的 TeX Live 或 MiKTeX。

Windows PowerShell 在本目录运行：

```powershell
./build.ps1
```

其他系统：

```sh
sh build.sh
```

也可在本目录分别对 `main_en.tex`、`main_zh.tex` 运行两次 XeLaTeX。默认优先使用 Times New Roman；没有该字体时使用 TeX Gyre Termes 文件。中文采用随 TeX 发行版提供的 Fandol 字体。两版共用数据及数值宏，不需要联网编译，也不必先运行 Python。

## 复现模型与更新论文

验证环境：Python 3.12；具体包版本见 `code/requirements.txt`。

```sh
python -m pip install -r code/requirements.txt
python code/run_models.py
python code/export_tables.py
```

随后运行编译脚本，再执行：

```sh
python code/verify_results.py
```

固定种子为 2022。浮点库版本变化可能造成优化器末位数值差异。`run_models.py` 从事件生成开始执行，包括指标覆盖筛选、数据清洗、状态模型、业务链拟合、情景优化和样本外检验。`export_tables.py` 将保存结果转为共享 LaTeX 数值宏与表格。参数如发生实质变更，还应人工核对正文中写明的解释和例子。

编译脚本将过程文件放入 `.build/`。该目录不是交付所需内容；本压缩包中没有编译日志、临时截图、缓存、原始参考论文或重复 PDF。

## 已完成核验

- 两版成功编译；英文总页数 23（所有部分均计入）。
- 摘要独立一页、客户信独立一页；目录、参考文献交叉引用已更新。
- 检查中英文字符、页面边界、图表及公式；无未定义引用和缺字。
- 原始记录守恒、KPI 分母、RMSE、区间覆盖率、成熟度、预算、后悔值与保存结果一致。
- 保留并解释了未通过的检验：状态区间覆盖率仅 66.7%，技术延迟识别有误，更宽压力测试中稳健方案仍有 5% 预算违约。

这些检查验证了文档与实验的内部一致性，不构成实际企业部署有效性认证。
