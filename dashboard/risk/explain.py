"""Turns the stored SHAP values of a commit into things the templates can show."""

FEATURE_LABELS = {
    "la": "Lines added",
    "ld": "Lines deleted",
    "nf": "Files changed",
    "nd": "Directories changed",
    "ns": "Subsystems changed",
    "ent": "Change entropy (spread over files)",
    "ndev": "Developers who touched these files",
    "age": "Days since the files were last changed",
    "nuc": "Earlier unique changes to these files",
    "aexp": "Author's earlier commits",
    "arexp": "Author's recent experience",
    "asexp": "Author's commits in these subsystems",
}

GROUPS = {
    "Size and spread": ["la", "ld", "nf", "nd", "ns", "ent"],
    "File history": ["ndev", "age", "nuc"],
    "Author experience": ["aexp", "arexp", "asexp"],
}


def build_effects(values, shap):
    """List of the 12 features sorted by the size of their effect.

    Each item also carries `left` and `width` (in percent) so that the template can
    draw a bar around a centre line: red to the right = raises the risk,
    blue to the left = lowers it.
    """
    largest = max(abs(v) for v in shap.values()) or 1.0
    effects = []
    for feature, effect in shap.items():
        width = 50 * abs(effect) / largest
        effects.append({
            "feature": feature,
            "label": FEATURE_LABELS[feature],
            "value": values[feature],
            "effect": effect,
            "raises": effect > 0,
            "left": 50 if effect > 0 else 50 - width,
            "width": width,
        })
    effects.sort(key=lambda e: abs(e["effect"]), reverse=True)
    return effects


def group_effects(shap):
    """Sum of the SHAP values of each feature group (positive = raises the risk)."""
    totals = [(name, sum(shap[f] for f in features)) for name, features in GROUPS.items()]
    return sorted(totals, key=lambda item: abs(item[1]), reverse=True)


def format_number(value):
    """Whole numbers without decimals, others with two decimals."""
    value = float(value)
    return f"{int(value):,}" if value.is_integer() else f"{value:,.2f}"


def top_reasons(effects, k=3):
    """The k largest effects as short sentences for the top of the detail page."""
    reasons = []
    for e in effects[:k]:
        reasons.append({
            "text": f"{e['label']}: {format_number(e['value'])}",
            "raises": e["raises"],
        })
    return reasons
