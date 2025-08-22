from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1 import views


v1_router = DefaultRouter()
v1_router.register(r'pills', views.PillViewSet, basename='pills')
v1_router.register(r'categories', views.CategoryViewSet, basename='categories')
v1_router.register(
    r'medicine-form', views.MedicineFormViewSet, basename='medicine-form'
)
v1_router.register(
    r'manufacturer', views.ManufacturerViewSet, basename='manufacturer'
)
v1_router.register(
    r'active-substance', views.ActiveSubstanceViewSet, basename='active-substance'
)
v1_router.register(
    r'pills/(?P<pill_id>\d+)/comments', views.CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
