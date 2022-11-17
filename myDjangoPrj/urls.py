from django.contrib import admin
from django.urls import path, include
# 아래 두개가 파일 때문에 임포트
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # IP주소/admin
    path('blog/', include('blog.urls')), #ip주소/blog
    path('',include('single_pages.urls')), #ip주소
    path('accounts/',include('allauth.urls')),
]

# 파일을 위한 url지정 그리고 본문에 어떤 파일인지에 따라서 로고 변환
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)