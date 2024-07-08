from django.contrib import admin
from django.urls import path, include
from fit_app.views import *
from django.conf import settings
from django.conf.urls.static import static
# import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurant/', include('restaurantapp.urls')),
    path('', include('fit_app.urls')),

    # path('notifications/', include(notifications.urls, namespace='notifications')),
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
