from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponse
from django.shortcuts import render

from Exam import settings
from blog.models import User, Article, ArticleComment


def unlogin(request):
    return render(request,'login.html')

def login(request):
    if request.method == 'GET':
        del request.session['IS_LOGIN']
        del request.session['username']
        return render(request, 'login.html')
    elif request.method == 'POST':
        user_name = request.POST.get('username','')
        pass_word = request.POST.get('password','')
        print(user_name,pass_word)
        user = User.objects.filter(username=user_name)  #查看数据库里是否有该用户名
        if user:#如果存在
            user = User.objects.get(username = user_name)#读取该用户信息
            if pass_word==user.password:#检查密码是否匹配
                request.session['IS_LOGIN'] = True
                request.session['username'] = user_name
                return render(request,'index.html',{'user':user})
            else:
                return render(request,'login.html',{'error': '密码错误!'})
        else:
            return render(request, 'login.html', {'error': '用户名不存在!'})
    else:
        return render(request,'login.html')
def register(request):
    if request.method =='POST':
        user_name = request.POST.get('username','')
        pass_word = request.POST.get('password','')
        pass_word1 = request.POST.get('password1','')
        if (pass_word != pass_word1):
            return render(request, 'register.html', {'error': '提示:两次密码请输入一致'})
        if User.objects.filter(username = user_name):
            return render(request,'register.html',{'error':'提示:用户已存在'})
            #将表单写入数据库
        user = User()
        user.username = user_name
        user.password = pass_word
        user.save()
            #返回注册成功页面
        return render(request,'login.html')
    else:
        return render(request,'register.html')

def blog(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        posts = Article.objects.all()  # 获取全部的Article对象
        paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
        page = request.GET.get('page')  # 获取URL中page参数的值
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        username = request.session['username']
        return render(request, 'blog.html', {'post_list': post_list, 'username': username})

def detail(request, id):  # 查看文章详情
    if request.method == 'POST':
        body = request.POST.get('body','')
        id = request.POST.get('id',)
        username = request.POST.get('username',)
        print('body:',body)
        print("id:",id)
        print("ok")
        if body!='':
            newrecord = ArticleComment()
            newrecord.body = body
            newrecord.article = id
            newrecord.username = username
            newrecord.save()
            user = User.objects.get(username = username)
            user.comment()
    try:
        post = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    comments = ArticleComment.objects.filter(article = str(id))
    comments_len = len(comments)
    paginator = Paginator(comments, 3)  # 每页显示3条评论
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        comment_list = paginator.page(page)
    except PageNotAnInteger:
        comment_list = paginator.page(1)
    except EmptyPage:
        comment_list = paginator.page(paginator.num_pages)
    return render(request, 'post.html', {'post': post, 'username':request.session['username'],'comment_list':comment_list,'comments_len':comments_len})

def postcomment(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        return render(request, 'postcomment.html',
                      {'username': request.session['username'],'id' : id})


