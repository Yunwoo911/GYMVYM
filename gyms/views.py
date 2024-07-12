from django.shortcuts import render
from django.views.generic import TemplateView
from .models import GymMember, PersonalInfo, Trainer
from gyms.forms import PersonalInfoForm
from account.models import CustomUser
import random

# Create your views here.
class TrainerPageView(TemplateView):
    template_name = 'trainer_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gym_members'] = GymMember.objects.all()
        return context
    

class TrainerDetailPageView(TemplateView):
    template_name = 'trainer_detail_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gym_member_id = self.kwargs.get('id')
        # context['gym_members'] = GymMember.objects.all()
        context['personal_info'] = PersonalInfo.objects.filter(gym_member_if__member_id=gym_member_id)
        return context
    

class ProfileAddPageView(TemplateView):
    template_name = 'profile_add_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gym_member_id = self.kwargs.get('id')
        context['form'] = PersonalInfoForm()
        return context

    # def post(self, request, *args, **kwargs):
    #     form = PersonalInfoForm(request.POST)
    #     if form.is_valid():
    #         personal_info = form.save(commit=False)
    #         gym_member_id = self.kwargs.get('id')
    #         personal_info.gym_member_if = GymMember.objects.get(member_id=gym_member_id)
    #         personal_info.save()
    #         return render(request, 'profile_add_success.html', {'form': form})
    #     return render(request, self.template_name, {'form': form})    


class TrainerPortfolioView(TemplateView):
    template_name = 'trainer_portfolio_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        # user = self.kwargs.get('id')
        user = 15
        context['trainer'] = CustomUser.objects.filter(user = user)
        # context['trainer'] = Trainer.objects.filter(user = user)
        return context
        



