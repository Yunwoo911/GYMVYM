from django.shortcuts import render
from django.views.generic import TemplateView
from .models import GymMember



# Create your views here.
class TrainerPageView(TemplateView):
    template_name = 'trainer_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gym_members'] = GymMember.objects.all()
        return context
