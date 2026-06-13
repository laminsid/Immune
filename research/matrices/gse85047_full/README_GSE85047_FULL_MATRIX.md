# GSE85047 full matrix acquisition contract — v3.0.3.49

This directory is the canonical local target for the full GSE85047 series matrix.

Expected file:

`research/matrices/gse85047_full/GSE85047_series_matrix.txt.gz`

Official GEO URL:

`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE85nnn/GSE85047/matrix/GSE85047_series_matrix.txt.gz`

Important boundary: this package does **not** fabricate the 283-row/full-cohort matrix. If the file is absent, v30347/v30348 must keep `FULL_MATRIX_REQUIRED` / `LITE_CONTINUATION` states and must not emit survival/global discovery claims.
