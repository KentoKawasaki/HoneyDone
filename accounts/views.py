from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from.models import CustomUser
from .forms import (
    CustomUserCreationForm,
    CustomUserAuthenticationForm,
    CustomUserChangeForm,
    )


from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError

@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/newuser.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        email = self.request.POST.get('email')
        user_name = email.rsplit('@', 1)[0]
        form.instance.user_name = user_name
        return super().form_valid(form)


user_create = UserCreateView.as_view()


# class UserUpdateView(UpdateView):
#     model = CustomUser
#     form_class = CustomUserChangeForm
#     template_name = 'accounts/userupdate.html'
#     success_url = '/'


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomUserAuthenticationForm


login = CustomLoginView.as_view()


class LogoutView(LogoutView):
    pass


logout = LogoutView.as_view()