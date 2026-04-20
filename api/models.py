"""
AISA Training Dataset — MEDIUM Repo Models
aisa_label: medium
expected_risk_score: 45-55
expected_severity: High
notes: Models look mostly fine but contain subtle issues.
       Not obviously broken like vuln repo, not clean either.
"""

from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    """
    aisa_label: partially_clean
    notes: Has user FK (good) but no field-level restrictions
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True)       # internal notes — mild info leak risk
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order#{self.id} by {self.user}"


class UserProfile(models.Model):
    """
    aisa_label: partially_clean
    notes: No SSN/token (good) but has address — mild PII
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)    # mild PII — not critical but should be guarded

    def __str__(self):
        return f"Profile of {self.user}"


class Product(models.Model):
    """
    aisa_label: clean_model
    notes: Public product catalog — safe to expose
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
