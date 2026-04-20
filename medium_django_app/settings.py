"""
AISA Training Dataset — MEDIUM Repo Settings
aisa_label: medium
notes: Partially hardened — some good practices, some gaps.
       Realistic "developer tried but missed some things" pattern.
"""

SECRET_KEY = "replace-with-env-var-please"
DEBUG = True                         # ⚠️ MEDIUM: debug still on (leaks stack traces)
ALLOWED_HOSTS = ["*"]                # ⚠️ MEDIUM: should be restricted

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "rest_framework",
    "rest_framework.authtoken",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",    # ✅ CSRF on
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "medium_django_app.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

# ✅ Auth required by default (better than vuln repo)
# ⚠️ MEDIUM: no throttling configured globally
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # ✅ global auth
    ],
    # ⚠️ No DEFAULT_THROTTLE_CLASSES — missing rate limiting
    # ⚠️ No DEFAULT_PAGINATION_CLASS — unbounded lists possible
}
