from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from herdapp.views import AnimalViewSet, MilkRecordViewSet, animal_list, animal_detail


router = DefaultRouter()
router.register(r'animals', AnimalViewSet, basename='animal')
router.register(r'milk-records', MilkRecordViewSet, basename='milkrecord')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', animal_list, name='animal_list'),
    path('animals/<int:pk>/', animal_detail, name='animal_detail'),
]
