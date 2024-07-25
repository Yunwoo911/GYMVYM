from django.shortcuts import render
from django.views.generic import TemplateView
from .models import GymMember, PersonalInfo, Trainer
from gyms.forms import PersonalInfoForm
from account.models import CustomUser
import random
import json
from django.shortcuts import redirect

# from gyms.search.search_gym_member import Search

# Create your views here.
class PtMembershipManagementPageView(TemplateView):
    template_name = 'pt_membership_page.html'


class ProfilePageView(TemplateView):
    template_name = 'profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gym_members'] = GymMember.objects.all()
        return context
    

class TrainerDetailPageView(TemplateView):
    template_name = 'trainer_detail_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gym_member_id = self.kwargs.get('id')
        context['gym_member_id'] = gym_member_id
        context['personal_info'] = PersonalInfo.objects.filter(gym_member_if__member_id=gym_member_id)
        return context
    

class ProfileAddPageView(TemplateView):
    template_name = 'profile_add_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gym_member_id = self.kwargs.get('id')
        context['gym_member_id'] = gym_member_id
        context['form'] = PersonalInfoForm()
        return context        


def profile_save(request, **kwargs):
    form = PersonalInfoForm(request.POST)
    if form.is_valid():
        personal_info = form.save(commit=False)        
        personal_info.gym_member_if_id = kwargs['id']
        personal_info.save()
        return redirect('gyms:trainer_detail_page', id=kwargs['id'])
    else:
        return render(request, 'profile_add_page.html', {'form': form})


class TrainerPortfolioView(TemplateView):
    template_name = 'trainer_portfolio_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        # user = self.kwargs.get('id')
        user = 15
        context['trainer'] = CustomUser.objects.filter(user = user)
        # context['trainer'] = Trainer.objects.filter(user = user)
        # 트레이너 테이블에서 로그인한 트레이너의 유저 아이디를 찾아서 반환
        # 포트폴리오 입력 폼 작성하고, 작성한 거 받아서 데이터베이스에 저장.
        return context


def search(request):
    results = []
    client = Search()

    # 검색어를 받아오기
    if 'query' in request.GET:
        query = request.GET['query']
        # 검색결과를 가져와야 하지 않나?        
        usernames = client.making_query(query)
        results = GymMember.objects.filter(user__username=usernames)
    
    return render(request, 'member_profile_search.html', {'results': results})


def export_gym_member_usernames_to_json(file_path):
    gym_members = GymMember.objects.all()
    data = [
        {
            "username": member.user.username,
            "join_date": member.join_date.strftime('%Y-%m-%d')
        }
        for member in gym_members
    ]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# export_gym_member_usernames_to_json('gym_member_usernames.json')
