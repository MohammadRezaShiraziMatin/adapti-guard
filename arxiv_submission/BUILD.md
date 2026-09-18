# Local build procedure

This package deliberately keeps the scientific source in Markdown so the manuscript remains reviewable. Generate the TeX only for the final upload.

## 1. Generate TeX

```bash
pandoc MANUSCRIPT_SOURCE.md \
  --standalone \
  --from markdown+tex_math_dollars+pipe_tables \
  --to latex \
  -o main.tex
```

## 2. Add final figures

Copy only the figures actually referenced by the final manuscript into `figures/`.

Current Q2 figure sources are under:

`../docs/research/q2_publication_package/figures/`

Do not copy unrelated repository figures.

## 3. Compile

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

If bibliography processing is used, run the required BibTeX/Biber step and compile again.

## 4. Inspect

Check:

- title/authors
- abstract
- every table
- every figure
- equation rendering
- references
- page breaks
- no missing glyphs
- no unresolved references
- no internal paths
- no draft/status banners

## 5. Archive

The final arXiv source archive should contain only the files required to compile the paper: main `.tex`, bibliography/source files actually used, and referenced figures. Do not upload `.aux`, `.log`, `.toc`, old drafts, audit reports, repository dumps, or unused figures.

arXiv documents that TeX submissions are compiled automatically and that extraneous/intermediate files should be removed before submission. urlarXiv TeX submission guidancehttps://info.arxiv.org/help/submit_tex.html
