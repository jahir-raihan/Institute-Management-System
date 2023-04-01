# """Start necessary  Imports"""
import datetime
from email.mime.image import MIMEImage
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Post, Liked, Comment
from .forms import PostCreateForm, PostUpdateForm
from .models import User, Notifications

from django.core import serializers
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils import timezone

import os

# """End Imports"""


# """home page view"""


@login_required
def home(request):

    """Home page for the whole site. In this page users
        can view notices , like and comment in the notices and
        can do more stuff ."""

    notifications = Notifications.objects.order_by('-notification_date')[:10]

    posts = Post.objects.order_by('-date_posted')[:20]
    if request.method == 'POST':
        if 'like' in request.POST and request.POST['like']:
           
            post = Post.objects.get(pk=request.POST['like'])
            user = Liked.objects.filter(user=request.user, post=post).first()

            if user: 
                post.likes -= 1
                post.save()
                user.delete()
                return render(request, 'post/like_template.html', {'post': post})
            else: 
                post.likes += 1
                post.save()  
                l_user = post.liked_set.create(user=request.user, post=post)
                l_user.save()

                return render(request, 'post/like_template.html', {'post': post})
        post = Post.objects.get(pk=request.POST['post_id'])
        if 'comment' in request.POST and request.POST['comment']:

            if 'page' in request.POST and request.POST['page']:
                comment = post.comment_set.create(comment=request.POST['comment'], user=request.user, post=post)
                comment.save()
                
                return render(request, 'post/view_page_comment.html', {'post': post, 'time': timezone.now()})

            comment = post.comment_set.create(comment=request.POST['comment'], user=request.user, post=post)
            comment.save()
        elif 'page' in request.POST:
            return render(request, 'post/view_page_comment.html', {'post': post, 'time': timezone.now()})
        return render(request, 'post/comment_template.html', {'post': post, 'time': timezone.now()})

    context = {
        'posts': posts,
        'time': timezone.now(),
        'notifications': notifications,
        'clg_name': settings.COLLEGE_NAME,

    }
    return render(request, 'post/home.html', context)


# """ end home page view """


# """create post view"""

@login_required
def create(request):

    """Creating a post/notice .
        Only teacher and staff can access this
        page."""

    notifications = Notifications.objects.order_by('-notification_date')[:10]
    if request.user.is_teacher or request.user.is_accountant or request.user.is_admin:
        users = User.objects.all()
        form = PostCreateForm()

        if request.method == 'POST':

            form = PostCreateForm(request.POST, request.FILES)

            if form.is_valid():
                if 'image' in request.FILES:

                    form_main = Post(title=request.POST['title'], text=request.POST['text'], image=request.FILES['image'],
                                     date_posted=request.POST['date_posted'], post_user=request.user)
                else:
                    form_main = Post(title=request.POST['title'], text=request.POST['text'],
                                     date_posted=request.POST['date_posted'], post_user=request.user)
                form_main.save()
                notification = Notifications(
                    notification=f'has posted about {form_main.title}',
                    notification_author=form_main.post_user,
                    post_id=form_main.id
                )
                notification.save()

                """When the post gets created , this part of code sends email to all users
                    that an announcement/notice/post has been made along with link to view the post."""

                users_emails = [user.email for user in users]
                # email alternative
                context = {

                    "post_id": form_main.id,
                    "notice_title": form_main.title,
                    'clg_name': settings.COLLEGE_NAME,
                    'year': datetime.datetime.now().year,
                    'domain': request.META['HTTP_HOST']
                }

                html_content = render_to_string('emailTemplate/post_email.html', context)
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    f"{request.user} has posted about {form_main.title}",
                    text_content,
                    settings.EMAIL_HOST_USER,
                    users_emails
                )
                path = settings.EMAIL_LOGO_PATH  # path to your logo
                image = 'Logo.jpg' # logo name
                email.attach_alternative(html_content, 'text/html')
                file_path = os.path.join(path, image)
                with open(file_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-ID', '<{name}>'.format(name=image))
                    img.add_header('Content-Disposition', 'inline', filename=image)

                email.attach(img)

                email.send()

                return redirect('/')

        context = {
            'form': form,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,

        }
        return render(request, 'post/create.html', context)

    return redirect('/')

# """end create post view"""


# """post update view"""

@login_required
def update(request, id):
    if request.user.is_teacher or request.user.is_staff or request.user.is_admin or request.user.is_accountant:

        """This view is for updating an existing post."""

        notifications = Notifications.objects.order_by('-notification_date')[:10]

        post = Post.objects.get(id=id)
        if request.method == 'POST':
            form = PostUpdateForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()

                return redirect(f'/{id}/view/')
        else:
            form = PostUpdateForm(instance=post)

        context = {
            'form': form,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,

        }
        return render(request, 'post/update.html', context)
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission denied '})

# """end post update view"""


# """full view of a post"""

@login_required
def view(request, id):

    """Viewing a post with full content and all comments."""

    notifications = Notifications.objects.order_by('-notification_date')[:10]
    try:
        post = Post.objects.get(id=id)
        context = {
            'post': post,
            'time': timezone.now(),
            'notifications': notifications,
            'clg_name': settings.COLLEGE_NAME,

        }
        return render(request, 'post/view.html', context)
    except:
        return render(request, 'post/404_page_all.html', {'message': "This Notice is no longer available. Maybe Deleted",
                                                          'title': 'Notice Not Found'})


# """end full view of a post"""


# """delete post view"""

@login_required
def delete(request, id):

    """This view is for deleting a post"""

    notifications = Notifications.objects.order_by('-notification_date')[:10]

    post = Post.objects.get(id=id)
    if request.method == 'POST':
        try:
            if len(post.image) > 0:

                os.remove(post.image.path)
        except:
            pass
        post.delete()

        return redirect('/')

    context = {
        'post': post,
        'time': timezone.now(),
        'clg_name': settings.COLLEGE_NAME,
    }
    
    return render(request, 'post/delete.html', context)

# """end deleter post view"""

# """student profile view"""


@login_required
def profile(request, id):

    """For viewing a user profile with all basic details."""

    notifications = Notifications.objects.order_by('-notification_date')[:10]
    try:

        user = User.objects.get(pk=id)
        is_teacher = False
        if user.is_teacher:
            is_teacher = True
        context = {
            'user': user,
            'notifications': notifications,
            'time': timezone.now(),
            'is_teacher': is_teacher,
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'post/profile.html', context)
    except:
        return render(request, 'post/404_page_all.html', {'message': "Profile does not exist.",
                                                          'title': 'Not Found'})

# """end student profile view"""



