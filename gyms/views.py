from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import GymMember, PersonalInfo, Trainer,CustomUser, TrainerRequest, Owner
from gyms.forms import PersonalInfoForm
from account.models import CustomUser
import random
import json
from django.contrib.auth.decorators import login_required
from .forms import TrainerRequestForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

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


# 기존의 request_trainer_role 뷰
@login_required
def request_trainer_role(request):
    if request.method == 'POST':
        form = TrainerRequestForm(request.POST)
        if form.is_valid():
            trainer_request = form.save(commit=False)
            trainer_request.user = request.user
            trainer_request.request_date = timezone.now()
            trainer_request.save()
            # 관리자에게 이메일 알림 보내기 (선택사항)
            return redirect('trainer_request_success')  # 요청 성공 페이지로 리디렉션
    else:
        form = TrainerRequestForm()
    return render(request, 'request_trainer_role.html', {'form': form})

# 기존의 approve_trainer_request 뷰
# @staff_member_required
@login_required
def approve_trainer_request(request, trainer_request_id):
    trainer_request = get_object_or_404(TrainerRequest, trainer_request_id=trainer_request_id)
    if request.method == 'POST':
        trainer_request.user.usertype = 1  # 트레이너 역할로 변경
        trainer_request.user.save()
        trainer_request.approved = True
        trainer_request.approved_date = timezone.now()
        # trainer_request.approved_by = request.user.user
        trainer_request.approved_by = Owner.objects.get(owner_id=1)  # 수정된 코드
        trainer_request.save()
        # 사용자에게 승인 알림 보내기 (선택사항)
        # return redirect('trainer_requests_list')  # 요청 리스트 페이지로 리디렉션 trainer_request_success
        return redirect('home')  # 요청 리스트 페이지로 리디렉션 
    return render(request, 'approve_trainer_request.html', {'trainer_request': trainer_request})

class TrainerRequestSuccessView(TemplateView):
    template_name = 'trainer_request_success.html'
    pass


def reject_trainer_request(request, trainer_request_id):
    trainer_request = get_object_or_404(TrainerRequest, id=trainer_request_id)
    if request.method == 'POST':
        reject_reason = request.POST.get('reject_reason')
        # 거절 로직 추가
        trainer_request.status = 'rejected'
        trainer_request.reject_reason = reject_reason  # 거절 사유 저장
        trainer_request.save()
        return redirect('some_view_name')  # 거절 후 리디렉션할 뷰 이름
    return render(request, 'reject_trainer_request.html', {'trainer_request': trainer_request})


def request_trainer(request):
    if request.method == 'POST':
        form = TrainerRequestForm(request.POST)
        if form.is_valid():
            # 폼 처리 로직
            pass
    else:
        form = TrainerRequestForm()
    
    return render(request, 'request_trainer.html', {'form': form})