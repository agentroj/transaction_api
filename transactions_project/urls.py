from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import ( # noqa
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('transactions_app.urls')),
    # 1. the OpenAPI schema endpoint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # 2. the Swagger UI at /docs/
    path('docs/', SpectacularSwaggerView.as_view(
        url_name='schema',
        title="Transaction API Docs"
    ), name='swagger-ui'),
]
