from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.edit import View
from . import forms
# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth import login


class index(View):

    def get(self, request):
        return render(request, 'MainApp/homepage.html',
                      {'user': request.user})


class contact(FormView):

    def get(self, request):
        return render(request, 'MainApp/contact.html',
                      {'values': ['Звоните по телефону', 'boris@yandex.ru', '8(977)335-77-77'], 'user': request.user})


class registration(FormView):
    form_class = forms.UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "MainApp/registration_form.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(registration, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)
        return render(request, 'MainApp/quitpage.html')


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "MainApp/login_form.html"

    # В случае успеха перенаправим на главную.
    success_url = "/news"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)
