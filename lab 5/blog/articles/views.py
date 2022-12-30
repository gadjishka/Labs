from articles.models import Article
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
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
                return redirect('archive')
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'create_post.html', {'form': form})
