from articles.models import Article
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})
def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404
def create_post(request):
    if request.method == "GET":
            return render(request, 'create_post.html', {})
    else:
        form = {
            'text': request.POST['text'].strip(),'author':request.user, 'title': request.POST['title'].strip()
        }
        if form['text'] and form['title']:
            try:
                post = Article.objects.get(title=form['title'])
                form['errors'] = u"Такая статья уже существует"
                return render(request, 'create_post.html', {'form':form})       
                
            except Article.DoesNotExist:
                per=Article.objects.create(text=form['text'],author=form['author'], title=form['title'])
                return redirect('archive',article_id=per.id)
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'create_post.html', {'form': form})
          
def registration(request):
    if request.method == "POST":
        form = {
            'username': request.POST['username'],
            'email': request.POST['email'],
            'password': request.POST['password']
        }
        if form["username"] and form["email"] and form["password"]:
            try:
                User.objects.get(username=form['username'])
               # User.objects.get(email=form['email'])
                form['errors'] = "Логин или почта уже заняты"
                return render(request, 'registration.html', {'form': form})
            except User.DoesNotExist:
                User.objects.create_user(form['username'], form['email'], form['password'])
                login(request, authenticate(request, username=form['username'], password=form['password']))
                return redirect('archive')
        else:
            form['errors'] = u'Не все поля заполнены!'
        return render(request, 'registration.html', {'form': form})
    else:
        return render(request, 'registration.html', {})

def login_user(request):
    if request.method == "POST":
        form = {
            'username': request.POST['username'],
            'password': request.POST['password']
        }
        if form['username'] and form['password']:
            user = authenticate(username=form['username'], password=form['password'])
            if user is None:
                form['error'] = u'Такого пользователя не существует'
                return render(request, 'login.html', {'form': form})
            else:
                login(request, user)
                return redirect('archive')
        else:
            form['errors'] = u'Не все поля заполнены'
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('archive')
