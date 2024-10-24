"""
URL configuration for AsistenteEstudiantil project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from App import views  # Importa la vista home

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Agrega esta línea
    path('registrarse/', views.registrarse, name='registrarse'),
    path('login', views.log_in, name='log-in'),
    path('log-out/', views.sign_out, name='log-out'),  # Opcional, según tus necesidades
    path('interact-with-openai/', views.interact_with_openai, name='interact-with-openai'),
    path('openai-interaction/', views.openai_interaction_view, name='openai-interaction'),
    #path('ver-nivel-estres/', views.ver_nivel_estres, name='ver-nivel-estres'),
    #path('actualizar-nivel-estres/<int:nuevo_nivel>/', views.actualizar_nivel_estres, name='actualizar-nivel-estres'),
    path('store/', views.store, name='store'),
    path('insufficient-tokens/', views.insufficient_tokens, name='insufficient-tokens'),
    path('redeem/<int:product_id>/', views.redeem_reward, name='redeem-reward'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-profile/', views.user_profile, name='user-profile'),
    path('agregar-producto-avatar/', views.agregar_producto_avatar, name='agregar_producto_avatar'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)