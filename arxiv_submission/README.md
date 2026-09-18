# arXiv submission package

Status: **ARXIV_PACKAGE_SOURCE_READY**

This directory is a clean publication layer built from the Q2 publication-packaging branch. It is intentionally separate from the historical workshop/VNEXT manuscript.

## Scientific scope

- Central contribution: controlled detector–policy attribution for LLM-agent security.
- Primary endpoint: Tool-HASR.
- Secondary diagnostic: Judge-ASR.
- Q2: bounded pilot-scale directional consistency across T0–T3.
- `scientific_evidence=false`.
- No SOTA, best-detector, universal-defense, or production-robustness claim.
- Track A FAIL and Track B Phase-1 results are not pooled into Q2.
- Stage-B raw `predictions.jsonl` is unavailable on this checkout and is explicitly disclosed; no historical evidence is fabricated.

## Source

`MANUSCRIPT_SOURCE.md` is the current Q2 manuscript source.

## Build

Generate a clean LaTeX source and PDF locally with Pandoc/PDFLaTeX. Do not submit the Markdown source itself.

Recommended workflow:

```bash
cd arxiv_submission
pandoc MANUSCRIPT_SOURCE.md -o main.tex --standalone --pdf-engine=pdflatex
pdflatex -interaction=nonstopmode main.tex
```

Then inspect the PDF manually, especially tables, equations, figure references, references, and page breaks.

Before arXiv upload, create a clean archive containing only the final `.tex`, bibliography files if used, and figures actually referenced by the manuscript. arXiv explicitly advises removing unused/intermediate/extraneous files and requires accompanying figures for TeX submissions. urlarXiv TeX submission guidancehttps://info.arxiv.org/help/submit_tex.html

## Required final checks

- [ ] PDF compiles locally.
- [ ] No unresolved references/citations.
- [ ] No internal GitHub-only paths remain in the paper.
- [ ] All figures are embedded and scientifically identical to frozen artifacts.
- [ ] Author name/email are correct.
- [ ] Abstract and conclusion retain pilot-scale scope.
- [ ] Stage-B missing-trace disclosure remains.
- [ ] No Q1/Q2 journal-quartile claim appears.
- [ ] No SOTA/best/universal/production claim appears.
- [ ] Final PDF is manually inspected.
