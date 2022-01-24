from django.urls import path
from Word.views import process_word, help_menu
from WordFinder.views import find_word


urlpatterns = [
    #path('admin/', admin.site.urls),    
    path('/',find_word, name='find_word'),
    path('/find',help_menu, name='help')
]
