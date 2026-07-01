# Residualization alignment note ()

The public code uses mean-centered within-fiber residualization:

```python
residual = value - group_mean(value)
```

The manuscript text has been aligned to this implementation. Earlier draft wording referred to median-centering; that was a documentation mismatch, not a code change. The file `tables/residual_centering_sensitivity.csv` reports a mean-vs-median sensitivity check. The direction remains positive for all three validation source families under both centering choices.
