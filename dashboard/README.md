# Commit risk dashboard

A small Django app that shows the risk of each test-year commit (2017) and the reasons behind it.
It does not run the model: it reads the predictions and SHAP values that were prepared in
`notebooks/06_explainability.ipynb` and `notebooks/07_risk_levels.ipynb`.

## Run it

From the repository root, with the virtual environment active:

```powershell
pip install -r requirements.txt
cd dashboard
python manage.py migrate
python manage.py import_commits
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

`import_commits` reads `dashboard/data/commits.csv` (created by notebook 07) and replaces the rows in the
local SQLite database (`dashboard/db.sqlite3`, not committed).

## Pages

- `/` overview: commits per risk level, risk over the months, top review priorities
- `/commits/` list with filters (project, level, commit id), sorting and pagination
- `/commits/<commit id>/` one commit with its risk and the feature effects (SHAP)
