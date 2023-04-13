from django.db import models
from django.contrib.auth.models import User

# TODO: Profile 모델 생성


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='profile/', null=True)

    class Meta:
        db_table = 'profile'
        # 장고에서 만들어주는 테이블 이름을 정할 수 있음.

    def __str__(self):
        # admin에서 프로필을 조회했을 때 프로필이 출력되도록 함.
        return self.nickname
