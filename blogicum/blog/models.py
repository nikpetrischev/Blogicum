# Django Library
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

# Local Imports
from core.models import CreatedAtModel, PublishedModel, TitleModel

User = get_user_model()
User.add_to_class(
    'get_full_name',
    lambda user: f'{user.first_name} {user.last_name}',
)


# For all further classes next is appliable:
# ...
# Inherits:
# ---------
# PublishedModel ->
#     fields:
#         is_published: BooleanField
#             flag if entity is to be shown
#     manager:
#         published_objects:
#             custom manager that filters by value of aforemenshioned field
# CreatedAtModel ->
#     fields:
#         created_at: DateTimeField
#             automaticaly checks when entity was created


class Category(TitleModel, PublishedModel, CreatedAtModel):
    """
    Class related to Category table in db.

    ...

    Inherits:
    ---------
    TitleModel ->
        fields:
            title: CharField
                title of entity with up to 256 chars length
        overrides:
            __str__ -> string
                returns readble name of entity

    ...

    Fields:
    -------
    description: TextField
        desribes what this category is about
    slug: SlugField
        short verbose identifier for category
    """
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, '
                   'цифры, дефис и подчёркивание.'),
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(PublishedModel, CreatedAtModel):
    """
    Class related to Location table in db.

    ...

    Fields:
    -------
    name: CharField
        name of the location where post was created
        with length up to 256 chars
    Overrides:
    ----------
        __str__ -> string
            returns readble name of entity
    """
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comment(CreatedAtModel):
    """
    Class related to Location table in db.

    ...

    Fields:
    -------
    text: TextField
        text of comment itself
        further adjusted in its widget on the form
    Overrides:
    ----------
        __str__ -> string
            returns readble name of entity
    ForeignKeys:
    ------------
    author
        links to User db table as M:1
    post
        links to Post db table
    """
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    post = models.ForeignKey(
        'Post',
        verbose_name='Публикация',
        related_name='comments',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return str(self.created_at)


class Post(TitleModel, PublishedModel, CreatedAtModel):
    """
    Class related to Post table in db.

    ...

    Inherits:
    ---------
    TitleModel ->
        fields:
            title: CharField
                title of entity with up to 256 chars length
        overrides:
            __str__ -> string
                returns readble name of entity

    ...

    Fields:
    -------
    text: TextField
        post itself
    pub_date: DateTimeField
        exact time of delayed publishment
    ForeignKeys:
    ------------
    author
        links to User db table as M:1
    location
        links to Location db table as M:1
    category
        links to Category db table as M:1
    """
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем '
                   '— можно делать отложенные публикации.'),
    )
    image = models.ImageField(
        verbose_name='Иллюстрация',
        blank=True,
        upload_to=settings.POST_IMAGES
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self.pk).count()

    @property
    def is_published_post(self):
        return (
            self.is_published
            and self.pub_date.astimezone() <= timezone.now()
            and self.category.is_published
        )
