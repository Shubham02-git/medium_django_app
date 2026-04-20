"""
AISA Training Dataset — MEDIUM Repo Serializers
aisa_label: medium
notes: Not fields="__all__" (good) but still leaks some fields it shouldn't.
       The vulnerability is subtle — looks like developer "tried" to be safe.
"""

from rest_framework import serializers
from .models import Order, UserProfile, Product


class OrderSerializer(serializers.ModelSerializer):
    """
    aisa_label: partial_exposure
    weakness: exposes 'note' (internal field) and 'status' (should be read-only)
    severity: MEDIUM — not critical PII but internal data leaking
    """
    class Meta:
        model = Order
        fields = ["id", "item", "amount", "note", "status", "created_at"]
        # ⚠️ MEDIUM: 'note' is internal — shouldn't be in API response
        # ⚠️ MEDIUM: 'status' not marked read_only — client can set it


class UserProfileSerializer(serializers.ModelSerializer):
    """
    aisa_label: partial_exposure
    weakness: exposes 'address' — mild PII, no explicit guard
    severity: MEDIUM
    """
    class Meta:
        model = UserProfile
        fields = ["id", "phone", "address"]
        # ⚠️ MEDIUM: address is PII — should require explicit user consent to expose


class ProductSerializer(serializers.ModelSerializer):
    """
    aisa_label: clean_serializer
    notes: Product is public data — full exposure is fine here
    """
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price"]
        # ✅ stock intentionally excluded (internal inventory data)
