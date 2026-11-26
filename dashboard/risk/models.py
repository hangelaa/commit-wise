from django.db import models


class Commit(models.Model):
    """One test-year commit with the model's prediction and its explanation."""

    LEVELS = [("High", "High"), ("Medium", "Medium"), ("Low", "Low")]

    commit_id = models.CharField(max_length=64, unique=True)
    project = models.CharField(max_length=60, db_index=True)
    date = models.DateTimeField(db_index=True)
    probability = models.FloatField(db_index=True)   # predicted probability of "bug-inducing"
    priority = models.FloatField(db_index=True)      # probability / (lines changed + 1)
    risk_level = models.CharField(max_length=6, choices=LEVELS, db_index=True)
    buggy = models.BooleanField()                    # label in the dataset (not seen by the model)
    lines_changed = models.PositiveIntegerField()    # lines added + lines deleted
    values = models.JSONField()                      # the 12 feature values
    shap = models.JSONField()                        # the 12 SHAP values (log-odds)

    class Meta:
        ordering = ["-priority"]

    def __str__(self):
        return f"{self.project} {self.commit_id[:8]}"
