from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('edit/', views.formulario, name='formulario'),
    path('cards/', views.card_list, name='card_list'),
    path('cards/create/', views.create_message, name='create_message'),
    path('cards/delete/', views.delete_selected_messages, name='delete_selected_messages'),

    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
