from django import forms

from django.contrib.auth import get_user_model
from .models import Todo


UserModel = get_user_model()


class TodoForm(forms.ModelForm):
    
    class Meta:
        
        model = Todo
        fields = ('title', 'priority')
        labels = {
            'title': 'タスク',
            'priority': '優先度',
        }


def TodoFormSet(todos_count=0):
    TodoFormSet = forms.modelformset_factory(
        Todo,
        form=TodoForm,
        extra=6-todos_count,
        can_delete=False,
        max_num=6,
    )
    return TodoFormSet


class TodoUpdateForm(forms.ModelForm):

    class Meta:

        model = Todo
        fields = ('title', 'body', 'priority', 'status')
        labels = {
            'title': 'タスク',
            'body': '詳細内容',
            'priority': '優先',
        }

    def __init__(self, *args, **kwargs):
        super(TodoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['body'].required = False


