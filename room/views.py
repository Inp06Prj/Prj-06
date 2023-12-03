from django.views.generic import ListView
from .models import Lectureroom

# Create your views here.
class LectureroomList(ListView):
    model = Lectureroom
    odering = '-pk'
