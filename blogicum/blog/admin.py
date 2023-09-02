# Django Library
from django.contrib import admin

# Local Imports
from .models import Category, Location, Post, Comment


class PostInline(admin.StackedInline):
    model = Post
    extra = 0
    fields = (
        'title',
        'author',
        'location',
    )


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    fields = (
        'author',
        'text',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Updates visual style of admin panel for Post db table.

    Columns:
    --------
    title -> clickable, searchable;
    author -> informative;
    category -> for filtering, changeable via drop-down list;
    location -> for filtering;
    is_published -> editable checkbox;
    pub_date -> informative.
    """
    list_display = (
        'title',
        'author',
        'category',
        'location',
        'is_published',
        'pub_date',
    )
    list_editable = (
        'is_published',
        'category',
    )
    search_fields = ('title',)
    list_filter = (
        'category',
        'location',
    )
    inlines = (
        CommentInline,
    )

    @admin.display(empty_value='Планета Земля')
    def location(self, obj):
        return obj.location


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Updates visual style of admin panel for Category db table.

    Columns:
    --------
    title -> clickable, searchable;
    is_published -> editable checkbox;

    On each category's page - list of related posts.
    """
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'is_published',
    )
    search_fields = ('title',)
    list_editable = ('is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Updates visual style of admin panel for Location db table.

    Columns:
    --------
    name -> clickable, searchable;
    is_published -> editable checkbox;

    On each location's page - list of related posts.
    """
    inlines = (
        PostInline,
    )
    list_display = (
        'name',
        'is_published',
    )
    search_fields = ('name',)
    list_editable = ('is_published',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
    )
    exclude = ('post',)
    list_display_links = ('text',)
    search_fields = ('author',)
