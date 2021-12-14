import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Todo(models.Model):

    # PRIORITY = ((num, str(num)) for num in range(1, 7))

    title = models.CharField('タイトル', max_length=55)
    body = models.TextField('詳細/内容', max_length=400, default='')
    priority = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    status = models.BooleanField('完了', default=False)
    created = models.DateTimeField('作成日時', auto_now_add=True)
    updated = models.DateTimeField('更新日時', auto_now_add=True)
    user_account = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_account')

    def __str__(self):
        return self.title

    # def todo_display_limit(self):
    #     now_date = timezone.now()
    #     created_date = self.created
    #     display_deadline = created_date + datetime.timedelta(days=1)
    #     return created_date <= now_date <= display_deadline