from django.urls import path
from Word.views import process_word, help_menu, results

app_name='Word'

urlpatterns = [
    #path('admin/', admin.site.urls),    
    path('/',process_word, name='process_word'),
    path('/help',help_menu, name='help'),
    path('/results', results, name='results'),

]
