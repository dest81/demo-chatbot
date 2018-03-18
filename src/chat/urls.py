from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from chatterbot.ext.django_chatterbot import urls as chatterbot_urls


from chat_engine import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.chat, name='chat'),
    # url(r'^api/chatterbot/', include(chatterbot_urls, namespace='chatterbot')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
