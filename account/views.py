from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from actions.utils import create_action, delete_action
from actions.models import Action
from .models import Profile, Contact
from .forms import UserRegistrationForm, \
                   UserEditForm, ProfileEditForm
from images.models import Image


@login_required
def news(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')[:10]

    return render(request,
                  'account/news.html',
                  {'section': 'News',
                   'actions': actions})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})



@login_required
def user_list(request):
    users = User.objects.filter(is_active=True).exclude(id=1).order_by('username')
    return render(request,
                  'account/user/list.html',
                  {'section': 'Artists',
                   'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    images = Image.objects.filter(activity='Active', user=user)
    not_active_images = Image.objects.filter(activity='Inactive', user=user)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'Artists',
                   'user': user, 'images': images, 'not_active_images': not_active_images})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})


@login_required
def i_follow(request):
    users = request.user.following.all()
    return render(request,
                  'account/user/list.html',
                  {'section': 'Artists',
                   'users': users})


@login_required
def edit_mypage(request):
    paintings = Image.objects.filter(activity='Active', user=request.user)    
    return render(request,
                  'account/edit_mypage.html',
                  {'paintings': paintings})


@login_required
def confirm_delete_profile(request):
    return render(request, 'account/confirm_delete_profile.html')

@login_required
def delete_profile(request):
    images = Image.objects.filter(user=request.user)
    Contact.objects.filter(user_to=request.user).delete()
    for image in images:
        delete_action(image)
    delete_action(request.user)
    get_object_or_404(User, id=request.user.id).delete()
    messages.success(request, 'Profile deleted successfully')
    return HttpResponseRedirect(reverse("login"))



