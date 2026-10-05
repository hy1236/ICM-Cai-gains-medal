#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
mkdir -p .build
for entry in main_en main_zh; do
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=.build "$entry.tex"
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=.build "$entry.tex"
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=.build "$entry.tex"
  cp ".build/$entry.pdf" "$entry.pdf"
done
