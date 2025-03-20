from django.urls import path
from .import views
from users.utility import train, test




urlpatterns = [
       path('registercheck/',views.registercheck,name='registercheck'),
       path('userlogin',views.userlogin,name='userlogin'),
       path('userlogincheck/',views.userlogincheck,name = 'userlogincheck'),
       path('userlogout/',views.userlogout,name='userlogout'),
       path('profile/', views.user_profile, name='userprofile'),
       path('update_profile/',views.update_profile,name='update_profile'),
       path('userhome/', views.user_home, name='userhome'),
       path('Task1/',train.task1_view,name='Task1'),
       path('matrix', views.ConfusionMatrice, name='matrix'),
       path('prediction', views.hate_speech_predictor, name='prediction'),
       path('hate_speech_predictor_audio/', views.hate_speech_predictor_audio, name='hate_speech_predictor_audio'),









]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)