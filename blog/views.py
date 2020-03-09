from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Post, Comment, Category
from .forms import CommentForm, PostForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    ArchiveIndexView,
    YearArchiveView,
    MonthArchiveView,
)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse

def js(request):
    return render(request, 'blog/js.html')

def about(request):
    return render(request, 'blog/about.html')


def category(request):
    return render(request, 'blog/category.html', {'categories':
                                                         Category.objects.all()})

#def category(request):
#    if request.method == "POST":
#        form = CategoryForm(request.POST)
#        if form.is_valid():
#            form.save()
#            title = form.cleaned_data.get('title')
#            messages.success(request, f'Category for {title} has been created!')
#            return redirect('blog-category')
#    else:
#        form = CategoryForm()
#    context = {
#        'form': form,
#        'categories': Category.objects.all()
#    }
#    return render(request, 'blog/category.html', context)

class PostArchiveIndexView(ArchiveIndexView):
    model = Post
    date_field = "date_posted"

class PostYearArchiveView(YearArchiveView):
    queryset = Post.objects.all()
    date_field = "date_posted"
    make_object_list = True

class PostMonthArchiveView(MonthArchiveView):
    queryset = Post.objects.all()
    date_field = "date_posted"

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object, 'author':
                                               self.request.user})
        return context


class PostCommentView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'blog/post_detail.html'
    form_class = CommentForm
    model = Post

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

class PostView(View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentView.as_view()
        return view(request, *args, **kwargs)



class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

#class SearchPostListView(ListView):
#    model = Post
#    paginate_by = 3
#
#    def get_queryset(self):
#        qs = Post.objects.all()
#        keywords = self.request.GET.get('q')
#        if keywords:
#            query = SearchQuery(keywords)
#            vector = SearchVector('title', 'content')
#            qs = qs.annotate(search=vector).filter(search=query)
#            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')
#        return qs

class SearchPostListView(ListView):
    model = Post
    paginate_by = 3
    context_object_name = 'posts'
    template_name = 'blog/search_list.html'

    def get_queryset(self):
        keywords = self.request.GET.get('q')
        return Post.objects.filter(Q(title__icontains=keywords) |
                                   Q(content__icontains=keywords) |
                                   Q(author__username__icontains=keywords)).order_by('-date_posted')
    def get_query(self):
        return self.request.GET.get('q')

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class CategoryListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/category_posts.html'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):
        category = get_object_or_404(Category, title=self.kwargs.get('title'))
        return category.post_set.all().order_by('-date_posted')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_post(self):
        return self.get_object().post

    def get_success_url(self, **kwargs):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk_post']})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_object(self):
        return Comment.objects.get(id=self.kwargs['pk_comment'])


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_update.html'

    def get_object(self):
        return get_object_or_404(Category, title=self.kwargs.get('title'))


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self, **kwargs):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk_post']})

    def get_object(self):
        comment = Comment.objects.get(id=self.kwargs['pk_comment'])
        return comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = '/category/'

    def get_object(self):
        return get_object_or_404(Category, title=self.kwargs.get('title'))

