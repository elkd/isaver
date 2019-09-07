from django.shortcuts import render
from django.views.generic import ListView
from .models import Room, Booking

class BookingView(ListView):
    model = Room
    context_object_name = "rooms"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['base_active'] = 'posts'
        return context
# Create your views here.
