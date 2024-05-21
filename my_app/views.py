from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Article, Category, Comment
from django.http import HttpResponse
from .forms import ArticleForm, LoginForm, RegistrationForm, CommentForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class ArticleList(LoginRequiredMixin, ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'all_articles.html'
    extra_context = {
        'title': "Maqola ro'yxati class"
    }
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related('category')


class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'article_details.html'

    def get_queryset(self):
        return Article.objects.filter(pk=self.kwargs['pk'], is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        article.watched += 1
        article.save()
        context['title'] = article.title
        context['comments'] = Comment.objects.filter(article=article)
        articles = Article.objects.filter(is_published=True).order_by('-watched')[:4]
        context['articles'] = articles
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context


class NewArticle(CreateView):
    form_class = ArticleForm
    template_name = 'article_form.html'
    extra_context = {
        'title': "Classda maqola qoshish"
    }
    success_url = reverse_lazy('index')


class ArticleListByCategory(ArticleList):
    def get_queryset(self):
        return Article.objects.filter(category_id=self.kwargs['pk'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category.title
        return context


def add_comment(request, article_id):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        article = Article.objects.get(pk=article_id)
        comment.article = article
        comment.save()
        messages.success(request, "Comment success add")
        return redirect('article_details', article_id)


class SearchList(ArticleList):
    def get_queryset(self):
        word = self.request.GET.get('q')
        articles = Article.objects.filter(title__icontains=word, is_published=True)
        return articles


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('index')
    template_name = 'article_confirm_delete.html'


@login_required()
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    articles = Article.objects.filter(author=user)
    context = {
        'title': "Sizning profilingiz",
        'user': user,
        'articles': articles
    }
    return render(request, 'profile.html', context)


def user_login(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Siz Authenticated dan otdingiz')
            next = request.POST.get('next', 'index')
            return redirect(next)
    else:
        form = LoginForm()
    context['form'] = form
    context['title'] = 'Authenticated'
    return render(request, 'user_login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'Siz Saytdan chiqdingiz')
    return redirect('login')


def register(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akkaunt yaratildi")
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'title': "Akkaunt ochish",
        "form": form
    }
    return render(request, 'register.html', context)


# def test(request):
#     articles = Article.objects.all()
#     paginator = Paginator(articles, 2)
#     page_number = request.GET.get('page')
#     page_articles = paginator.get_page(page_number)
#     return render(request, 'all_articles.html', context={'page_articles': page_articles})


def index(request):
    articles = Article.objects.filter(is_published=True)
    context = {
        'articles': articles,
        'title': "Maqolalar ro'yxati"
    }
    return render(request, 'all_articles.html', context)


def category_list(request, pk):
    articles = Article.objects.filter(category_id=pk)
    category = Category.objects.get(pk=pk)
    context = {
        'articles': articles,
        "title": f"{category.title} kategoriyasi"
    }
    return render(request, 'all_articles.html', context)


def article_details(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'title': article.title,
        'article': article
    }
    return render(request, 'article_details.html', context)


def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            return redirect('article_details', pk=article.pk)

    else:
        form = ArticleForm()
        context = {
            'form': form,
            'title': "Maqola qoshish"
        }
        return render(request, 'article_form.html', context)

# def index(request):
#     articles = Article.objects.all()
#     result = '<h1>Maqola royxati</h1><hr>'
#     for article in articles:
#         result += f"<p>{article.title}:{article.content}</p>"
#     return HttpResponse(result)
