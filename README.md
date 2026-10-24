# Commit Wise

Predicting the risk of software commits before merge or release, with explanations.

## Overview

A machine learning system for Just-In-Time (JIT) defect prediction: it estimates
how likely a commit is to introduce a bug and explains the reasons behind each
prediction. Models are evaluated with a realistic, time-aware protocol instead
of a random split.

## Goals

- Compare Logistic Regression, Random Forest, XGBoost and LightGBM
- Evaluate with time-based splits and effort-aware metrics
- Explain predictions with SHAP and check how stable explanations are over time
- Provide a simple web dashboard showing commit risk and reasons

## Dataset

ApacheJIT: commits from open-source Apache projects with defect labels.

## Scope and Limitations

This project addresses JIT defect prediction. It does not predict deployment
or CI failures. Labels come from bug-inducing commit identification and may
contain noise. Only features available at commit time are used, to avoid
data leakage.

## Future Work

- Add source-code metrics (e.g. with Lizard)
- Compare with a code-aware model (e.g. CodeBERT) on the same commits

## Status

Work in progress.

## License

MIT
