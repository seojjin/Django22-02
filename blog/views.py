from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView

#def index(request):
#    posts1 = Post.objects.all().order_by('-pk')
#    return render(request, 'blog/index.html', {'posts': posts1})

#def single_post_page(request, pk):
#    post2 = Post.objects.get(pk=pk)
#    return render(request, 'blog/single_post_page.html', {'post': post2})

class PostList(ListView):
    model = Post
    ordering = '-pk'

    # 카테고리 변수 정의하고 함수 쓰기 화면에 보여주기 위한, 숫자까지
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

    # 템플릿 모델명_list.html : post_list.html
    # 파라미터 모델명_list : post_list

class PostDetail(DetailView):
    model = Post

    # 템플릿 모델명_detail.html : post_detail.html
    # 파라미터 모델명 :post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

def category_page(request, slug): #slug가지고 와서 변수에 저장 그리고 가르기
    if slug == 'no_category':
        category = '미분류'
        post_list=Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category) #변수 만들기
    return render(
        request,
        'blog/post_list.html', #템플릿을 이걸로 계속 쓰겠다
        {'category': category,
         'post_list': post_list,
         'categories':Category.objects.all(),
         'no_category_post_count': Post.objects.filter(category=None).count
         } #템플릿이 사용하는 변수(이걸로 표시 하겠다)
    )





