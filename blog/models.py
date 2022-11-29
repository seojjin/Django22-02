from django.db import models
from django.contrib.auth.models import User
import os

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'


class Category(models.Model): #첫번째 카테고리 모델 만들기
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    #unique=True 하면 동일한 name을 갖는 카테고리는 만들수가 없다
    # allow_uni 하면 한국어도 가능

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'
    # 카테고리 url 연결하기. urls 들어가서 path 연결 바람

    class Meta:
        verbose_name_plural = 'Categories'
        #복수형 오타 잡아주기 위한

# setting 가서 installed apps 에 blog 랑 single page 추가하기
# 포스트 모델 만들기, 모델 만들고 migrate 해야 한다.
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True) #요약문 필드 만들기
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    # %Y 2022, %y 22

    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True) #settings가서 타임존 Asia/Seoul로 바꾸기, use=False로
    updated_at = models.DateTimeField(auto_now=True)

    # author
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # null = True : 데이터베이스 해당값 null로 넣을 수 있다.
    # SET_NULL : 유저 삭제시 작성자명 none 가능
    # 하고 데이터 베이스 올려야 함

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    #카테고리 필드 추가, 미분류 포스트를 위한 null=true, 카테고리 삭제시 포스트 삭제는 no, 빈칸 지정 ok

    tags = models.ManyToManyField(Tag, null=True, blank=True)  #null과 on~ 쓸필요 없음음

    def __str__(self): # admin post페이지에서 보여주는 것
        return f'[{self.pk}]{self.title}::{self.author} : {self.created_at}'

    def get_absolute_url(self): # 1. 포스트 디테일에서 제목 쓸때
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    # 파일 로고 넣기 위해 파일 이름 가져오기

    # 파일 이름 중 가장 마지막 확장자만 가져오기
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]  #a.txt ab.doc c.xlsx ... a.b.c.txt?? -> 배열 가장 마지막 원소 = -1

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    # 댓글있는 부분 찾아서 이동
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}' #admin에서 viewonsite로 확인하기 위해 url(포스트 상세페이지) return하기

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'