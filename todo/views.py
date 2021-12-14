import datetime
from django.utils import timezone
from django.db.models import Q

from django.views.generic import (
    ListView, DetailView, UpdateView, DeleteView
)
# from django.views.generic import CreateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model

from .models import Todo
from .forms import TodoUpdateForm, TodoFormSet
# from .forms import TodoForm


UserModel = get_user_model()


def get_today_queryset(request, model):
    now_date = timezone.now()
    oneday_before = now_date - datetime.timedelta(days=1)
    current_user = request.user
    user_queryset = model.objects.filter(user_account=current_user)
    return user_queryset.filter(Q(created__gte=oneday_before) & Q(created__lt=now_date))


class IndexView(LoginRequiredMixin, ListView):

    template_name = 'todo/index.html'
    model = Todo
    context_object_name = 'todos'
    
    def get_queryset(self):
        print(self.request.user.email)
        user_today_queryset = get_today_queryset(self.request, self.model)
        return user_today_queryset.order_by('priority')[:6]
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        qs_todos = context['todos']
        start_datetime = qs_todos[0].created
        end_datetime = start_datetime + datetime.timedelta(days=1)
        qs_status_T = [qs for qs in qs_todos if qs.status]
        qs_status_F = [qs for qs in qs_todos if not qs.status]
        context['start_datetime'] = start_datetime
        context['end_datetime'] = end_datetime
        context['status_True'] = qs_status_T
        context['status_False'] = qs_status_F
        return context
    

index = IndexView.as_view()


class TodoDetailView(LoginRequiredMixin, DetailView):

    template_name = 'todo/detail.html'
    model = Todo
    context_object_name = 'todo'



todo_detail = TodoDetailView.as_view()


# class TodoCreateView(LoginRequiredMixin, CreateView):

#     template_name = 'todo/create.html'
#     model = Todo
#     form_class = TodoForm
#     success_url = reverse_lazy('todo:index')


# todo_create = TodoCreateView.as_view()


class TodoUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'todo/update.html'
    model = Todo
    form_class = TodoUpdateForm
    success_url = None

    def get_success_url(self):
        success_url = reverse_lazy('todo:todo_detail', kwargs={'pk':self.kwargs['pk']})
        return success_url

todo_update = TodoUpdateView.as_view()


class TodoDeleteView(LoginRequiredMixin, DeleteView):

    template_name = 'todo/delete.html'
    model = Todo
    success_url = reverse_lazy('todo:index')


todo_delete = TodoDeleteView.as_view()


"""Only 6 TodosLists Create"""
@login_required
def todo_create(request):
    current_user = request.user
    user_today_queryset = get_today_queryset(request, Todo)
    todos_count = len(user_today_queryset)
    FormSet = TodoFormSet(todos_count)
    if len(user_today_queryset) >= 6:
        return redirect('todo:index')
    # UserTodo = Todo.objects.filter(user_account=current_user)
    if request.method =='POST':
        formset = FormSet(request.POST or None)
        print(formset)
        print(request.POST)
        if formset.is_valid():
            FormSet = TodoFormSet()
            print('in formset.is_valid()', request.POST)
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user_account=current_user
                instance.save()
            return redirect('todo:index')
    else:
        formset = FormSet(queryset=Todo.objects.none())
    return render(request, 'todo/create.html', {'formset': formset})