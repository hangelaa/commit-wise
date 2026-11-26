from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Min, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, render

from .explain import build_effects, group_effects, top_reasons
from .models import Commit

LEVEL_ORDER = ["High", "Medium", "Low"]

# What the user can sort the commit list by (query value -> database ordering)
SORT_LABELS = {
    "priority": "Review priority",
    "probability": "Risk score",
    "date": "Date (oldest first)",
    "lines": "Lines changed",
}
SORTS = {
    "priority": "-priority",
    "probability": "-probability",
    "date": "date",
    "lines": "-lines_changed",
}


def overview(request):
    """Summary page: counts per risk level, risk over time, top review priorities."""
    total = Commit.objects.count()
    counts = dict(Commit.objects.values_list("risk_level").annotate(n=Count("id")))
    levels = [
        {
            "name": name,
            "count": counts.get(name, 0),
            "share": 100 * counts.get(name, 0) / total if total else 0,
        }
        for name in LEVEL_ORDER
    ]

    # One row per month with the share of commits in each risk level (stacked bar)
    monthly = (
        Commit.objects.annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            total=Count("id"),
            high=Count("id", filter=Q(risk_level="High")),
            medium=Count("id", filter=Q(risk_level="Medium")),
            low=Count("id", filter=Q(risk_level="Low")),
        )
        .order_by("month")
    )
    months = [
        {
            "label": row["month"].strftime("%b %Y"),
            "total": row["total"],
            "high": 100 * row["high"] / row["total"],
            "medium": 100 * row["medium"] / row["total"],
            "low": 100 * row["low"] / row["total"],
        }
        for row in monthly
    ]

    medium_threshold = Commit.objects.filter(risk_level="Medium").aggregate(m=Min("probability"))["m"]
    context = {
        "total": total,
        "levels": levels,
        "months": months,
        "top": Commit.objects.order_by("-priority")[:10],
        "high_threshold": settings.HIGH_THRESHOLD,
        "medium_threshold": medium_threshold,
    }
    return render(request, "risk/overview.html", context)


def commit_list(request):
    """Filterable, sortable and paginated list of commits."""
    commits = Commit.objects.all()

    project = request.GET.get("project", "")
    level = request.GET.get("level", "")
    query = request.GET.get("q", "").strip().lower()
    sort = request.GET.get("sort", "priority")

    if project:
        commits = commits.filter(project=project)
    if level in LEVEL_ORDER:
        commits = commits.filter(risk_level=level)
    if query:
        commits = commits.filter(commit_id__startswith=query)
    commits = commits.order_by(SORTS.get(sort, "-priority"))

    page = Paginator(commits, 25).get_page(request.GET.get("page"))

    # Keep the active filters in the pagination links
    params = request.GET.copy()
    params.pop("page", None)

    context = {
        "page": page,
        "projects": Commit.objects.order_by("project").values_list("project", flat=True).distinct(),
        "levels": LEVEL_ORDER,
        "sorts": SORT_LABELS.items(),
        "selected": {"project": project, "level": level, "q": query, "sort": sort},
        "querystring": params.urlencode(),
    }
    return render(request, "risk/commits.html", context)


def commit_detail(request, commit_id):
    """One commit: its risk and the reasons behind it."""
    commit = get_object_or_404(Commit, commit_id=commit_id)
    effects = build_effects(commit.values, commit.shap)
    context = {
        "commit": commit,
        "effects": effects,
        "groups": group_effects(commit.shap),
        "reasons": top_reasons(effects),
        "no_lines_added": commit.values["la"] == 0,
        "high_threshold": settings.HIGH_THRESHOLD,
    }
    return render(request, "risk/detail.html", context)
