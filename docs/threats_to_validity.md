# Threats to Validity

- **Label noise:** defect labels are derived automatically and may be wrong.
- **Data leakage:** only features available at commit time are allowed; random
  splits leak future information, so we use time-based splits.
- **Class imbalance:** buggy commits are the minority; accuracy is not used as
  the main metric.
- **Generalization:** results may not transfer to other projects or languages.

- **Label bias toward false negatives:** only the latest fixing commit per issue is used, so some bug-inducing commits are labeled clean.
- **Late labels:** a commit's label depends on a later fix, so recent commits may look cleaner than they are.
- **Java only:** the dataset keeps Java changes from 14 Apache projects.
- **Project imbalance:** bug ratios differ a lot across projects.

- **Label drift over time:** the share of bug-inducing commits varies by year (about 6% in 2003, 27% in 2017, 10% in 2019). Bug reports were collected only for 2010-2019, and recent commits had less time for their bugs to be found, so late labels are less reliable.
- **Hadoop naming:** the Hadoop HDFS and MapReduce data appear under three repository names (hadoop, hadoop-hdfs, hadoop-mapreduce); they are treated as one group in per-project analysis.
