# Django Library
from django.db import models
from django.utils import timezone


# Custom manager that checks if post is to be shown.
# (is_published flag is on, pub_date is not in the future,
# and category is published)
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
            pub_date__date__lte=timezone.now(),
            category__is_published=True,
        )


# Abstracts for base models found in blog/models.py
class PublishedModel(models.Model):
    # Flag if entity is to be shown on site.
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )

    # Add custom manager to already existing one.
    objects = models.Manager()
    published_posts = PublishedManager()

    class Meta:
        abstract = True


class CreatedAtModel(models.Model):
    # Autofield with time of post creation.
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class TitleModel(models.Model):
    # Entitlement of entity with length up to 256 symbols.
    title = models.CharField(max_length=256, verbose_name='Заголовок')

    class Meta:
        abstract = True

    # Override of str method. Returns user-friendly name of entity.
    def __str__(self):
        return self.title
