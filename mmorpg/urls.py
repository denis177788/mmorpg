from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('sign/', include('sign.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls'))
]
