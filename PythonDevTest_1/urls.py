from django.contrib import admin
from datetime import datetime
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
import mainapp.views as views 

admin.autodiscover()

urlpatterns = [
    re_path(r'^$', views.Main.as_view(), name='main'),
    path('admin/', admin.site.urls),
    path('add/', views.Add.as_view(), name='add'),
    path('delete/<int:pk>', views.Delete.as_view(), name='delete'),
    path('edit/<int:pk>', views.Edit.as_view(), name='edit'),
    path('details/<int:pk>', views.Details.as_view(), name='details'),

    path('to_json/', views.to_json, name='to_json'),
    path('to_csv/', views.to_csv, name='to_csv'),

    path('from_json/', views.from_json, name='from_json'),
    path('from_csv/', views.from_csv, name='from_csv'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)