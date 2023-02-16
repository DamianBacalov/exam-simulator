from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'exams'
urlpatterns = [
    path('', views.home, name='index'),
    path('exam/<int:pk>/', views.new_test, name='start'),
    # path('test/<int:pk>/', views.test, name='test'),
    path('test/<uuid:pk>/', views.test, name='test'),
    # path('test/<int:pk>/q/<int:qid>', views.test_questions, name='questions'),
    path('test/<uuid:pk>/q/<int:qid>', views.test_questions, name='questions'),
    path('import/', views.import_exam, name='import'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)