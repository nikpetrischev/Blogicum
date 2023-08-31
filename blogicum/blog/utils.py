# Django Library
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

# Some usefull funcs


# Func that returns full user's name. To be added to User model.
def get_full_name(self):
    return f'{self.first_name} {self.last_name}'


# Select post and all its related data by post's pk.
# Return 404 if no such post.
def get_post_or_404(self):
    Post = ContentType.objects.get(
        app_label='blog',
        model='post',
    ).model_class()
    return get_object_or_404(
        Post.objects.select_related(
            "author",
            "location",
            "category",
        ),
        pk=self.kwargs['pk'],
    )


# Select comment and its related post FK by comment's pk.
# Return 404 if no such comment.
def get_comment_or_404(self, request):
    Comment = ContentType.objects.get(
        app_label='blog',
        model='comment',
    ).model_class()
    return get_object_or_404(
        Comment.objects.select_related('post'),
        pk=self.kwargs['comment_id'],
        author=request.user.id,
    )
