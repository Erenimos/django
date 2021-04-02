from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from django.contrib import messages
from article.models import Article,Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
# Create your views here.
def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains= keyword)
        context = {
        "articles" : articles
    }
        return render(request,"articles.html",context)

    articles = Article.objects.all()
    context = {
        "articles" : articles
    }
    return render(request,"articles.html",context)

def index(request):
    return render(request,"index.html")

@login_required(login_url="user:login")
def dashboard(request):
    articles= Article.objects.filter(author = request.user)
    context = {
        "articles": articles
    }
    return render(request,"dashboard.html",context)
@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    context = {
        "form": form
    }

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makale Başarıyla Oluşturuldu..")
        return redirect('article:dashboard')
    
    return render(request,"addarticle.html",context)

def detail(request,id):
    #article = Article.objects.filter(id=id).first()
    article = get_object_or_404(Article,id=id)
    comments= article.comments.all()
    context= {
        "article":article,
        "comments":comments,
    }
    comments= article.comments.all()
    return render(request,"detail.html",context)
@login_required(login_url="user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article,id=id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance=article)
    context = {
        "form" : form
    }
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makale Başarıyla Kaydedildi..")
        return redirect('detail',id)
    return render(request,"update.html",context)
@login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id=id)
    article.delete()

    messages.success(request,"Makale Başarıyla Silindi")
    return redirect('article:dashboard')


def addComment(request,id):
    article = get_object_or_404(Article,id=id)

    if request.method == "POST":
        isim = request.POST.get("isim")
        yorum = request.POST.get("yorum")

        newComment = Comment(comment_author=isim,comment_content=yorum)

        newComment.article=article
        if isim == "":
            messages.warning(request,"İsim doldurulmamış!")
        elif yorum=="":
            messages.warning(request,"Yorum boş bırakılamaz!")
        else:
            newComment.save()
    return redirect("/article/" +str(id))