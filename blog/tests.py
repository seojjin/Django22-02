from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User

# Create your tests here.
class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_kim = User.objects.create_user(username="kim", password="qwer1234")
        self.user_lee = User.objects.create_user(username="lee", password="qwer1234")
        # user 테스트 하는법, 마지막꺼 임포트
        #user 만들기

        self.category_com = Category.objects.create(name="computer", slug="computer")
        self.category_cul = Category.objects.create(name="culture", slug="culture")
        #아래 카테고리 함수에서 썼던 변수써서 카테고리 정의

        self.post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다",
                                       author=self.user_kim, category=self.category_com)
        self.post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트 입니다",
                                       author=self.user_lee, category=self.category_cul)
        self.post_003 = Post.objects.create(title="세번째 포스트", content="세번째 포스트 입니다",
                                       author=self.user_lee)


    def nav_test(self, soup):  #test가 앞에 오면 안됨 항상 실행 되는 것이 아니므로
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('AboutMe', navbar.text)

        # 내비게이션에서 href 넘겨 주는법
        home_btn = navbar.find('a', text="Home")
        self.assertEqual(home_btn.attrs['href'], "/")
        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], "/blog/")
        about_btn = navbar.find('a', text="AboutMe")
        self.assertEqual(about_btn.attrs['href'], "/about_me/")

    def category_test(self, soup): # 각 페이지에서 동일하게 쓰이므로 함수로 구현
        category_card = soup.find('div', id='category_card') # 페이지에 id 적어야함(사이드바)
        self.assertIn('Categories', category_card.text)
        self.assertIn(f'{self.category_com} ({self.category_com.post_set.count()})', category_card.text)
        self.assertIn(f'{self.category_cul} ({self.category_cul.post_set.count()})', category_card.text)
        self.assertIn(f'미분류 (1)', category_card.text)

    def test_post_list(self):
        # 1.1. 포스트 목록 페이지를 가져온다
        response = self.client.get('/blog/')
        # 1.2. 정상적으로 페이지가 로드된다
        self.assertEqual(response.status_code, 200)
        # 1.3. 페이지 타이틀은 'Blog'이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')

        # 1.4. 내비게이션 바가 있다
        #navbar = soup.nav
        # 1.5. Blog, About Me 라는 문구가 내비게이션 바에 있다
        #self.assertIn('Blog', navbar.text)
        #self.assertIn('AboutMe', navbar.text)

        self.nav_test(soup)
        self.category_test(soup)

        self.assertEqual(Post.objects.count(), 3)


        # post가 정상적으로 보이는지
        # 2.1. 맨 처음엔 포스트가 하나도 안보임
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        main_area = soup.find('div', id="main-area") # 본문에 main-area id 적기
        self.assertIn('아무 게시물이 없습니다.', main_area.text)
        # 본문에 아무게시물이 없습니다 if 문으로 돌려야 함

        # 2.2. 포스트가 2개 있는 경우
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다",
                                      author=self.user_kim)
        post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트 입니다",
                                      author=self.user_lee)
        self.assertEqual(Post.objects.count(), 2)

        # 3.2 포스트 목록 페이지를 새로고침했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # 3.3. main area 에 포스트 2개의 제목이 존재한다
        main_area = soup.find('div', id="main-area")
        self.assertIn(self.post_001.title, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)

        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)
        # 3.4. '아무 게시물이 없습니다' 라는 문구는 더 이상 나타나지 않는다
        self.assertNotIn('아무 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        # 1.1. Post가 하나 있다.
        # setUp이 있기 때문에 삭제하고 post_001앞에 self 붙인다
        #post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다",
        #                               author=self.user_kim)
        # 1.2. 그 포스트의 url은 'blog/1/'이다
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        #2 첫 번째 포스트의 상세 페이지 테스트
        # 2.1. 첫 번째 post url로 접근하면 정상적으로 작동한다(status code: 200)
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2. 포스트 목록 페이지와 똑같은 내비게이션 바가 있다
        #navbar = soup.nav
        #self.assertIn('Blog', navbar.text)
        #self.assertIn('AboutMe', navbar.text)

        self.nav_test(soup)
        self.category_test(soup)

        # 2.3. 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2.4. 첫 번째 포스트의 제목이 포스트 영역(post_area)에 있다
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)

        # 2.5. 첫 번째 포스트의 작성자가 포스트 영역에 있다
        self.assertIn(self.post_001.author.username.upper(), post_area.text)

        # 2.6. 첫 번째 포스트의 내용이 포스트 영역에 있다
        self.assertIn(self.post_001.content, post_area.text)

# cmder에서 한부분만 테스트 하고 싶을때 예시
# python manage.py test blog.tests.TestView.test_post_list
# python manage.py startapp 앱