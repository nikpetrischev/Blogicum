# Standart Library
from typing import Any, Dict, TypeVar

# Django Library
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views.generic.list import MultipleObjectMixin

# Local Imports
from .forms import CommentForm, PostForm, UpdateUserForm
from .models import Category, Comment, Post, User
from core.constants import ITEMS_TO_SHOW


# ******************
# Post related views
# ******************
class PostListView(ListView):
    """
    Generate list of published posts for the homepage.
    """
    model = Post
    queryset = Post.published_posts.select_related(
        'author',
        'location',
        'category',
    )
    ordering = '-pub_date'
    paginate_by = ITEMS_TO_SHOW
    template_name = 'blog/index.html'


class PostDetailView(DetailView):
    '''
    Show post in all its details (comments included).
    '''
    model = Post
    template_name = 'blog/detail.html'

    def dispatch(
        self,
        request: TypeVar('HttpRequest'),
        *args: Any,
        **kwargs: Any
    ) -> TypeVar('HttpResponse'):
        get_object_or_404(
            Post.objects.select_related(
                "author",
                "location",
                "category",
            ),
            pk=self.kwargs['pk'],
        )
        if (self.get_object().author != request.user
                and not self.get_object().is_published_post):
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return dict(
            **super().get_context_data(**kwargs),
            comments=(Comment.objects.filter(post__id=self.get_object().pk)
                      .select_related('author').order_by('created_at')),
            form=CommentForm(),
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    '''
    Create and publish (probably) a new post.
    '''
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(
        self,
        form: TypeVar('BaseModelForm'),
    ) -> TypeVar('HttpResponse'):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


class PostUpdateDeleteMixin:
    '''
    DRY Mixin for the next 2 views (update and delete).
    '''
    model = Post
    template_name = 'blog/create.html'

    def dispatch(
        self,
        request: TypeVar('HttpRequest'),
        *args: Any,
        **kwargs: Any,
    ) -> TypeVar('HttpResponse'):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class PostEditView(
    PostUpdateDeleteMixin,
    LoginRequiredMixin,
    UpdateView,
):
    '''
    Allow to update post.
    Only post's author is approved.
    '''
    form_class = PostForm

    def get_success_url(self) -> str:
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class PostDeleteView(
    PostUpdateDeleteMixin,
    LoginRequiredMixin,
    DeleteView,
):
    '''
    Provide request to confirm post erasure.
    Only post's author is approved.
    '''
    def get_context_data(self, **kwargs):
        return dict(
            **super().get_context_data(**kwargs),
            form={'instance': self.object},
        )

    def get_success_url(self) -> str:
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


# *********************
# Comment related views
# *********************
class CommentMixin:
    '''
    DRY Mixin with fields common for all comments' views.
    '''
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self) -> str:
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']},
        )


class AddComment(CommentMixin, LoginRequiredMixin, CreateView):
    '''
    Add new comment to the post on the post's page.
    '''
    commented_post = None

    def dispatch(
        self,
        request: TypeVar('HttpRequest'),
        *args: Any,
        **kwargs: Any
    ) -> TypeVar('HttpResponse'):
        self.commented_post = get_object_or_404(
            Post.objects.select_related(
                "author",
                "location",
                "category",
            ),
            pk=self.kwargs['pk'],
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(
        self,
        form: TypeVar('BaseModelForm'),
    ) -> TypeVar('HttpResponse'):
        form.instance.author = self.request.user
        form.instance.post = self.commented_post
        return super().form_valid(form)


class EditComment(CommentMixin, LoginRequiredMixin, UpdateView):
    '''
    Edit your comment to some post.
    Only comment's author approved.
    '''
    commented_post = None

    def dispatch(
        self,
        request: TypeVar('HttpRequest'),
        *args: Any,
        **kwargs: Any
    ) -> TypeVar('HttpResponse'):
        get_object_or_404(
            Comment.objects.select_related('post'),
            pk=self.kwargs['comment_id'],
            author=request.user.id,
        )
        self.commented_post = get_object_or_404(
            Post.objects.select_related(
                "author",
                "location",
                "category",
            ),
            pk=self.kwargs['pk'],
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(
        self,
        form: TypeVar('BaseModelForm'),
    ) -> TypeVar('HttpResponse'):
        form.instance.author = self.request.user
        form.instance.post = self.commented_post
        return super().form_valid(form)


class DeleteComment(CommentMixin, LoginRequiredMixin, DeleteView):
    '''
    Delete your comment to some post.
    Only comment's author approved.
    '''
    def dispatch(
        self,
        request: TypeVar('HttpRequest'),
        *args: Any, **kwargs: Any,
    ) -> TypeVar('HttpResponse'):
        get_object_or_404(
            Comment.objects.select_related('post'),
            pk=self.kwargs['comment_id'],
            author=request.user.id,
        )
        return super().dispatch(request, *args, **kwargs)


# **********************
# Category related views
# **********************
class CategoryView(DetailView, MultipleObjectMixin):
    '''
    List of all posts (published) under the category.
    '''
    model = Category
    slug_url_kwarg = 'category_slug'
    paginate_by = ITEMS_TO_SHOW
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
        )
        object_list = (category
                       .posts(manager='published_posts')
                       .order_by('-pub_date'))
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['category'] = category
        return context


# ******************
# User related views
# ******************
class ShowUserProfile(DetailView, MultipleObjectMixin):
    '''
    Access to public data on user including all his (published) posts.
    Author can see theirs post even if they unpublished.
    '''
    model = User
    paginate_by = ITEMS_TO_SHOW
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        profile = get_object_or_404(
            User,
            username=self.kwargs['username'],
        )
        if self.request.user.username != self.kwargs['username']:
            manager = 'published_posts'
        else:
            manager = 'objects'
        object_list = (profile.posts(manager=manager)
                       .order_by('-pub_date'))
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['profile'] = profile
        return context


class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    '''
    Edit own user's data.
    '''
    model = User
    form_class = UpdateUserForm
    template_name = 'blog/user.html'

    def get_object(self) -> TypeVar('Model'):
        return self.request.user

    def get_success_url(self) -> str:
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )
