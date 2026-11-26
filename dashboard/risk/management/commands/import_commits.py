import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from risk.models import Commit

FEATURES = ["la", "ld", "nf", "nd", "ns", "ent", "ndev", "age", "nuc", "aexp", "arexp", "asexp"]


class Command(BaseCommand):
    help = "Load dashboard/data/commits.csv into the database (replaces existing rows)."

    def handle(self, *args, **options):
        path = settings.DATA_FILE
        if not path.exists():
            raise CommandError(
                f"Data file not found: {path}. Run notebooks/07_risk_levels.ipynb first."
            )

        data = pd.read_csv(path)
        dates = pd.to_datetime(data["author_date"], unit="s", utc=True)

        commits = []
        for record, date in zip(data.to_dict("records"), dates):
            commits.append(Commit(
                commit_id=str(record["commit_id"]),
                project=str(record["project"]),
                date=date.to_pydatetime(),
                probability=float(record["probability"]),
                priority=float(record["priority"]),
                risk_level=str(record["risk_level"]),
                buggy=bool(record["buggy"]),
                lines_changed=int(record["value_la"] + record["value_ld"]),
                values={f: float(record[f"value_{f}"]) for f in FEATURES},
                shap={f: float(record[f"shap_{f}"]) for f in FEATURES},
            ))

        Commit.objects.all().delete()
        Commit.objects.bulk_create(commits, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"Imported {len(commits)} commits."))
