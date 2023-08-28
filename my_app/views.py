from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .functions import *
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)



############ Классы представления ###############


class Home(TemplateView):
    template_name = 'home.html'


class Login(LoginView):
    template_name = 'registration/login.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return super().post(request)
        else:
            context = {
                'error_message': 'Не верное имя пользователя или пароль!'}
            return render(request, 'registration/login.html', context=context)

    def get_success_url(self):
        next = self.request.GET.get('next', '')
        if next:
            return super().get_success_url()
        else:
            return '/'


class Registration(TemplateView):
    template_name = 'registration/registration.html'

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password2')

        if email_check(email):
            error_message = "Email уже занят"
            return render(request, 'registration/registration.html', context={'error_message': error_message})

        if username_check(username):
            error_message = "Имя пользователя уже используется"
            return render(request, 'registration/registration.html', context={'error_message': error_message})

        if lenstring(password):
            error_message = "Минимальная длинна пароля 8 символов"
            context = {'error_message': error_message,
                       'username': username,
                       'email': email}
            return render(request, 'registration/registration.html', context=context)

        if confirmation_password(password, password_confirm):
            error_message = "Пароли не совпадают"
            context = {'error_message': error_message,
                       'username': username,
                       'email': email}
            return render(request, 'registration/registration.html', context=context)

        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return redirect('home_page')



class Group_List(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'group_list.html'
    login_url = '/login'

    def get_queryset(self):
        return Group.objects.order_by('-create_date')


class Group_Detail(LoginRequiredMixin, DetailView):
    model = Group
    login_url = '/login'
    template_name = 'group_detail.html'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(Group, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm
        context['posts'] = self.get_object().posts.order_by('-date')
        return context

    def post(self, request, slug):
        text = request.POST.get('text')
        group = Group.objects.get(slug=slug)
        object = Post.objects.create(
            text=text, author=request.user, group=group)
        object.save()
        return redirect('group_detail', slug=slug)


class CreateGroupView(LoginRequiredMixin, CreateView):
    form_class = GroupForm
    model = Group
    login_url = '/login'
    template_name = 'group_form.html'
    success_url = reverse_lazy('group_detail')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.errors.clear()
        return self.form_valid(form, request)

    def form_valid(self, form, request):
        form.instance.author = self.request.user
        if Group.objects.filter(title=form.instance.title).exists():
            error_message = "Такой заголовок уже существует"
            return render(request, 'group_form.html', context={'error_message': error_message, 'form': form})
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('group_detail', kwargs={'slug': self.object.slug})


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.kwargs['username']  # Получение значения user из kwargs
        object = User.objects.get(username=user)
        posts = Post.objects.filter(author=object.id).order_by('-date')
        print(posts)
        context['posts'] = posts
        return context




############## Функции представления ################

@login_required()
def join_group(request, slug=None):
    group = Group.objects.get(slug=slug)
    group.members.add(request.user)
    return redirect('group_detail', slug=slug)


@login_required()
def leave_group(request, slug=None):
    group = Group.objects.get(slug=slug)
    group.members.remove(request.user)
    return redirect('group_detail', slug=slug)


@login_required()
def delete_group(request, slug=None):
    if request.user.is_superuser:
        object = Group.objects.get(slug=slug)
        object.delete()
        return redirect('group_list')
    else:
        return redirect('/')


def post_delete(request, pk=None):
    if request.user.is_superuser:
        slug = request.GET.get('slug')
        object = Post.objects.get(pk=pk)
        object.delete()
        return redirect('group_detail', slug=slug)
    else:
        return redirect('/')
