from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import Post
from .forms import SignUpForm, SignInForm, FeedBackForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError


class MainView(View):
    def get(self, request):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'weblog/home.html', context={
            'page_obj': page_obj
        })


class PostDetailView(View):
    def get(self, reauest, slug):
        post = get_object_or_404(Post, url=slug)
        return render(reauest, 'weblog/post_detail.html', context={
            'post': post
        })


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'weblog/signup.html', context={
            'form': form,
        })

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'weblog/signup.html', context={
            'form': form,
        })


class SignInView(View):
    def get(self, request):
        form = SignInForm()
        return render(request, 'weblog/signin.html', context={
            'form': form,
        })

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'weblog/signin.html', context={
            'form': form,
        })


class FeedBackView(View):
    def get(self, request):
        form = FeedBackForm()
        return render(request, 'weblog/contact.html', context={
            'form': form,
            'title': 'Форма обратной связи'
        })

    def post(self, request):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {subject}', message, from_email, [''])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'weblog/contact.html', context={
            'form': form,
        })


class SuccessView(View):
    def get(self, request):
        return render(request, 'weblog/success.html', context={
            'title': 'Спасибо',
        })


class SearchResultView(View):
    def get(self, request):
        query = request.GET.get('q')
        results = ''
        if query:
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'weblog/search.html', context={
            'title': 'Поиск',
            'results': page_obj,
            'count': paginator.count,
        })
