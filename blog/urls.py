from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index), #ip주소/blog
    #path('<int:pk>/', views.single_post_page), #FBV 로 만들려면 해야함
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()), # 디테일 들어갔을때 뒤에 pk 붙이면서 포스트 디테일 페이지
    path('<int:pk>/new_comment/', views.new_comment),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('category/<str:slug>/', views.category_page), #그리고 views 들어가서 카테고리 페이지 만들기
    path('tag/<str:slug>/', views.tag_page),#ip주소/blog/tag/slug/
 ]

#미디어 관리는 settings 들어가서 저렇게 그리고 헤드 이미지 모델 만들기
#MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, '_media')