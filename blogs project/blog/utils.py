from django.db.models import Q
from .models import Blog,Category

def searchBlogs(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    categories = Category.objects.filter(name__icontains=search_query)
    blogs = Blog.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(content=search_query) |
        Q(owner__first_name__icontains=search_query) |
        Q(category__in=categories)

    )
    return blogs, search_query
