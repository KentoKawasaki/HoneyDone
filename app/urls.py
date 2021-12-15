from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from todo import views
from django.conf.urls import handler500


handler500 = views.my_customized_server_error


urlpatterns = [
    path('admin/', admin.site.urls),
    # accountsのurls.pyを読み込み
    path('', include('accounts.urls')),
    # todoのurls.pyを読み込み
    path('', include('todo.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)