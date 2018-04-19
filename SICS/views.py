from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

import datetime

from .models import User

from .models import Post
from .models import Message
from .models import Friend

from .forms import Login


# Create your views here.


def index(request):
    if request.user.is_authenticated():
        user = request.user
        user_name = user.username
        first_name = user.first_name
        last_name = user.last_name

        chat_friend = ""
        if request.method == 'GET':
            if 'friend' in request.GET:
                chat_friend = request.GET['friend']

        posts = Post.objects.filter(Q(sender_username=user_name)|Q(recipient=user_name))
        user_messages = []
        if chat_friend != "":
            user_messages = Message.objects.filter((Q(sender=user_name) & Q(recipient=chat_friend))|(Q(sender=chat_friend) & Q(recipient=user_name)))
            for message in user_messages:
                if message.sender == chat_friend:
                    Message.objects.filter(pk=message.pk).update(status=1)
        friend_list = Friend.objects.filter(Q(userA=user_name)|Q(userB=user_name))
        users = User.objects.all()

        messages = Message.objects.filter(recipient=user_name)
        notification = {}
        for message in messages:
            if message.status == 0:
                if message.sender not in notification:
                    notification[message.sender] = 1
                else:
                    notification[message.sender] += 1

        print(notification)

        message_friend = {}
        context = dict()
        context['k'] = [1, 2, 3, 4, 5]
        context['username'] = user_name
        context['first_name'] = first_name
        context['last_name'] = last_name
        context['posts'] = posts
        context['users'] = users
        context['friend_list'] = friend_list
        context['chat_friend'] = chat_friend
        context['messages_friend'] = message_friend
        context['user_messages'] = user_messages
        context['notification'] = notification
        return render(request, 'SICS/index.html', context)
    else:
        return HttpResponseRedirect(reverse('SICS:index_login'))


def index_login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        user_name = request.POST['user_name']
        password = request.POST['password']
        if form.is_valid():
            user = authenticate(request, username=user_name, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('SICS:index'))
                else:
                    messages.error(request, "The account is temporarily deactivated.")
            else:
                messages.error(request, "Wrong username or password")
        else:
            form = Login()
            return render(request, 'SICS/login.html', {'form': form})
    else:
        form = Login()
    return render(request, 'SICS/login.html', {'form': form})


def index_post(request):
    if request.user.is_authenticated():
        user = request.user
        if request.method == 'POST':
            recipient = request.POST['recipient']
            post = request.POST['post']
            time = datetime.datetime.now()
            username = user.username
            first_name = user.first_name
            last_name = user.last_name
            recipient_list = recipient.strip().split()
            print(recipient_list)
            if post.strip() != "":
                for r in recipient_list:
                    Post.objects.create(sender_username=username, sender_first_name=first_name, sender_last_name =last_name, recipient=r, data=post, time=time)
            return HttpResponseRedirect(reverse('SICS:index'))


def index_message(request):
    if request.user.is_authenticated():
        user = request.user
        chat_friend = ""
        if 'friend' in request.GET:
            chat_friend = request.GET['friend']
        print("chat_friend = ", chat_friend, "df")
        if request.method == 'POST':
            message = request.POST['message-input']
            time = datetime.datetime.now()
            username = user.username
            first_name = user.first_name
            last_name = user.last_name
            if message.strip() != "":
                Message.objects.create(sender=username, recipient=chat_friend, data=message, time=time, status=0)
            return HttpResponseRedirect(reverse('SICS:index') + "?friend=" + chat_friend)


def index_friend(request):
    if request.user.is_authenticated():
        user = request.user
        if request.method == 'POST':
            userb = request.POST['search_friend']
            username = user.username
            try:
                Friend.objects.get(Q(userA=username)|Q(userB=userb))
            except Friend.DoesNotExist:
                try:
                    Friend.objects.get(Q(userB=username) | Q(userA=userb))
                except Friend.DoesNotExist:
                    Friend.objects.create(userA=username, userB=userb)
            return HttpResponseRedirect(reverse('SICS:index'))


def index_chat_sub_div(request):
    if request.user.is_authenticated():
        user = request.user
        user_name = user.username
        first_name = user.first_name
        last_name = user.last_name
        friend_list = Friend.objects.filter(Q(userA=user_name) | Q(userB=user_name))
        users = User.objects.all()
        context = dict()
        context['friend_list'] = friend_list
        context['users'] = users
        return render(request, 'SICS/chat_subdiv.html', context)
    else:
        form = Login()
        return render(request, 'SICS/login.html', {'form': form})


def index_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('SICS:index_login'))
