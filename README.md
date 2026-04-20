# ⚠️ AISA Medium Django App — Boundary Training Dataset

> Partially vulnerable Django REST API.
> Used by AISA for **score calibration** — should land between clean and vuln repos.

---

## 🎯 Where This Fits

| Repo | Expected Score | Severity | Purpose |
|------|---------------|----------|---------|
| `vuln_django_app` | 100 | Critical | Positive training — all vulns |
| `medium_django_app` | **~50** | **High** | **Boundary calibration** |
| `clean_django_app` | < 10 | Low | Negative training — no vulns |

---

## ⚠️ Vulnerabilities (3 total — 2 HIGH, 1 MEDIUM)

| # | File | `weakness_label` | Severity | What makes it subtle |
|---|------|-----------------|----------|----------------------|
| 1 | `soft_idor_case.py` | `missing_object_level_auth` | HIGH | **Auth IS present** — just no ownership check. Real-world pattern. |
| 2 | `rate_limit_missing_case.py` | `missing_rate_limiting` | HIGH | Auth logic correct — just no brute-force protection |
| 3 | `verbose_error_case.py` | `verbose_error_disclosure` | MEDIUM | No PII leaked — just internal structure via error messages |

---

## ✅ Clean Views (intentionally fine)

- `ProductListView` — public product catalog, safe to expose
- `OrderCreateView` — proper auth + `user=request.user`
- `UserProfileView` — scoped to own profile (mild PII in serializer only)

---

## 🧠 Key Design Decisions

**Why these specific vulns?**

1. **Soft IDOR** — The hardest to detect. Auth is present so a naive scanner passes it.
   AISA must learn to check for ownership filters, not just authentication.

2. **Missing rate limiting** — Not detectable by looking at one function.
   AISA needs to check DRF settings + throttle_classes absence together.

3. **Verbose errors** — Lowest severity. Tests AISA's ability to score proportionally,
   not just binary detect/miss.

---

## 🤖 AISA Expected Output

```json
{
  "overall_risk": 50.0,
  "severity": "High",
  "vulnerabilities_detected": [
    {"type": "missing_object_level_auth", "confidence": 0.72},
    {"type": "missing_rate_limiting", "confidence": 0.68},
    {"type": "verbose_error_disclosure", "confidence": 0.65}
  ],
  "attack_chains": [
    {"chain": "BruteForce → SoftIDOR", "severity": "High"}
  ]
}
```

---

## 🛠 Setup

```bash
pip install django djangorestframework
python manage.py migrate
python manage.py runserver
```
