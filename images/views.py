from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, \
                                  PageNotAnInteger
from common.decorators import ajax_required
from actions.utils import create_action, delete_action
from .forms import ImageCreateForm, CommentForm
from .models import Image, Comment


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'loaded new painting', new_item)
            messages.success(request, 'Image added successfully')

            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  {'section': 'Paintings',
                   'form': form})
@login_required
def image_detail(request, id, slug):
    image = get_object_or_404(Image, activity='Active', id=id, slug=slug)
    comments = image.comments.all()[:3]
    new_comment = None
    if request.method == 'GET':
        comment_form = CommentForm()        
    else:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.image = image
            new_comment.user = request.user
            new_comment.save()
            create_action(request.user, 'loaded new comment to', image)
    return render(request,
                      'images/image/detail.html',
                      {'section': 'Paintings',
                      'image': image,
                      'comment_form': comment_form,
                      'comments': comments,
                      'new_comment': new_comment,})

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(activity='Active', id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                image.total_likes = image.total_likes + 1
                image.save()
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
                image.total_likes = image.total_likes - 1
                image.save()
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})


@login_required
def image_list(request, style=None):
    if style:
        images = Image.objects.filter(activity='Active', style=style).order_by('-total_likes')
    else:
        images = Image.objects.filter(activity='Active').order_by('-total_likes')
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'Paintings', 'images': images, 'style':style})
    return render(request,
                  'images/image/list.html',
                   {'section': 'Paintings', 'images': images, 'style':style})


@login_required
def styles(request):
    styles = ['Renaissance', 'Mannerism', 'Baroque', 'Classicism',
                      'Romanticism', 'Impressionism', 'Expressionism',
                      'Avant-garde', 'Other']
    return render(request,
                  'images/image/styles.html',
                   {'section': 'Styles', 'styles': styles})


@login_required
def edit_painting(request, painting_id):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'reloaded painting', new_item)
            messages.success(request, 'Image changed successfully')
            return redirect(new_item.get_absolute_url())
        else:
            messages.error(request, 'Error updating your painting')
    else:
        image = get_object_or_404(Image, activity='Active', id=painting_id)
        form = ImageCreateForm(instance=image)
    return render(request,
                  'images/image/edit_painting.html',
                  {'form': form, 'painting_id': painting_id})

@login_required
def deactivate_painting(request, painting_id):
    image = get_object_or_404(Image, activity='Active', id=painting_id)
    image.activity = 'Inactive'
    image.save()
    images = Image.objects.filter(activity='Active', user=request.user)
    not_active_images = Image.objects.filter(activity='Inactive', user=request.user)
    delete_action(image)
    messages.success(request, 'Image deactivated successfully')
    return render(request,
                  'account/user/detail.html',
                  {'section': 'Artists',
                   'user': request.user, 'images': images, 'not_active_images': not_active_images})

@login_required
def activate_painting(request, painting_id):
    image = get_object_or_404(Image, activity='Inactive', id=painting_id)
    image.activity = 'Active'
    image.save()
    images = Image.objects.filter(activity='Active', user=request.user)
    not_active_images = Image.objects.filter(activity='Inactive', user=request.user)
    messages.success(request, 'Image activated successfully')
    return render(request,
                  'account/user/detail.html',
                  {'section': 'Artists',
                   'user': request.user, 'images': images, 'not_active_images': not_active_images})


@login_required
def confirm_delete_painting(request, painting_id):
    image = get_object_or_404(Image, id=painting_id)
    return render(request, 'images/image/confirm_delete_painting.html',
                  {'image': image})

@login_required
def delete_painting(request, painting_id):
    image = get_object_or_404(Image, id=painting_id)
    delete_action(image)
    image.delete()
    images = Image.objects.filter(activity='Active', user=request.user)
    not_active_images = Image.objects.filter(activity='Inactive', user=request.user)
    messages.success(request, 'Image deleted successfully')
    return render(request,
                  'account/user/detail.html',
                  {'section': 'Artists',
                   'user': request.user, 'images': images, 'not_active_images': not_active_images})


@login_required    
def all_comments(request, painting_id):
    image = get_object_or_404(Image, activity='Active', id=painting_id)
    comments = image.comments.all()
    return render(request,
                  'images/image/comments.html',
                  {'comments': comments,
                   'image': image})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    images = Image.objects.filter(activity='Active', user=request.user)
    not_active_images = Image.objects.filter(activity='Inactive', user=request.user)
    messages.success(request, 'Comment deleted successfully')
    return render(request,
                  'account/user/detail.html',
                  {'section': 'Artists',
                   'user': request.user, 'images': images, 'not_active_images': not_active_images})
