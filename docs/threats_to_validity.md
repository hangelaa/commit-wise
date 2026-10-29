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
- **Inconsistent counts:** 1.3% of commits have more subsystems than directories (`ns` > `nd`); the cause is unknown and these rows are kept.
- **Size bias in labels:** SZZ blames the lines that a later fix deleted, so larger changes have more lines that can be blamed. Part of the link between size features and the label may come from the labeling method and not from real risk.
- **Label latency:** a training label can depend on a fix made after the test period starts, so the model may indirectly use future information. The validation year (2016) only partly reduces this.
- **Uneven project history:** projects such as Kafka have little training history compared with the test years, and small projects (ZooKeeper, ActiveMQ, Spark) have very few validation and test commits, so their per-project results are noisy.
