"""
AISA Training Dataset — MEDIUM Repo Views
aisa_label: medium
notes: Mix of clean + partially vulnerable views.
       Some endpoints are fine, some have subtle issues.
       This is realistic — not every view in a real app is broken.
"""

# Vulnerable views (imported from cases)
from .vulnerability_cases.soft_idor_case import OrderDetailView
from .vulnerability_cases.rate_limit_missing_case import LoginView
from .vulnerability_cases.verbose_error_case import OrderSearchView

# Clean views below
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Order, UserProfile, Product
from .serializers import OrderSerializer, UserProfileSerializer, ProductSerializer


class ProductListView(APIView):
    """
    aisa_label: clean
    notes: Public product catalog — intentionally open, no auth needed
    """
    # ✅ intentionally public — product catalog is not sensitive
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class OrderCreateView(APIView):
    """
    aisa_label: clean
    notes: Proper auth + user scoping on write
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # ✅ user from request, not body
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserProfileView(APIView):
    """
    aisa_label: partial — serializer exposes address (mild PII)
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # ✅ scoped to own profile
        # ⚠️ MEDIUM: UserProfileSerializer includes address field
        from django.shortcuts import get_object_or_404
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


__all__ = [
    "OrderDetailView",     # ⚠️ HIGH: soft IDOR
    "LoginView",           # ⚠️ HIGH: no rate limiting
    "OrderSearchView",     # ⚠️ MEDIUM: verbose errors
    "ProductListView",     # ✅ clean
    "OrderCreateView",     # ✅ clean
    "UserProfileView",     # ⚠️ MEDIUM: mild PII in serializer
]
