# Threats to Validity

- **Label noise:** defect labels are derived automatically and may be wrong.
- **Data leakage:** only features available at commit time are allowed; random
  splits leak future information, so we use time-based splits.
- **Class imbalance:** buggy commits are the minority; accuracy is not used as
  the main metric.
- **Generalization:** results may not transfer to other projects or languages.
