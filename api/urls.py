"""
AISA Training Dataset — MEDIUM Repo URLs
Mix of protected and public endpoints — realistic app structure.
"""

from django.urls import path
from api.views import (
    OrderDetailView,    # ⚠️ soft IDOR
    LoginView,          # ⚠️ no rate limiting
    OrderSearchView,    # ⚠️ verbose errors
    ProductListView,    # ✅ clean public endpoint
    OrderCreateView,    # ✅ clean
    UserProfileView,    # ⚠️ mild PII
)

urlpatterns = [
    # ⚠️ HIGH: authenticated but no ownership check
    path("api/orders/<int:id>/", OrderDetailView.as_view(), name="order-detail"),

    # ⚠️ HIGH: no brute-force protection
    path("api/auth/login/", LoginView.as_view(), name="login"),

    # ⚠️ MEDIUM: verbose error messages
    path("api/orders/search/", OrderSearchView.as_view(), name="order-search"),

    # ✅ public catalog — intentionally open
    path("api/products/", ProductListView.as_view(), name="product-list"),

    # ✅ clean write endpoint
    path("api/orders/create/", OrderCreateView.as_view(), name="order-create"),

    # ⚠️ MEDIUM: address field in response
    path("api/profile/", UserProfileView.as_view(), name="user-profile"),
]
