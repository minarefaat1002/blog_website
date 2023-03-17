from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect,JsonResponse
from .models import Blog,Category,Comment
from django.contrib import messages
from .forms import NewCommentForm,BlogForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .utils import searchBlogs
# Create your views here.
def blogs(request):
    blogs,search_query = searchBlogs(request)
    popular_blogs = Blog.objects.order_by('-likes')[:4]
    categories = Category.objects.all()[:10]
    context = {'blogs':blogs,'search_query':search_query , 'popular_blogs':popular_blogs,'categories':categories}
    return render(request,'blog/blogs.html',context)

def blog(request,pk):
    blog = Blog.objects.get(id=pk)
    popular_blogs = Blog.objects.order_by('-likes')[:4]
    categories = Category.objects.all()[:10]
    form = NewCommentForm()
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        comment = form.save(commit=False)
        comment.blog = blog
        comment.owner = request.user.profile
        comment.save()
        messages.success(request,'Your comment was successfully added!')
        return redirect('blog',pk=blog.id)
    return render(request,'blog/single-blog.html',{'blog':blog,'form':form,'popular_blogs':popular_blogs,'categories':categories})

def category(request,category):
    blogs = Blog.objects.filter(category__name=category)
    popular_blogs = Blog.objects.order_by('-likes')[:4]
    categories = Category.objects.all()[:10]
    context = {
        "blogs":blogs,
        'categories':categories,
        'popular_blogs':popular_blogs
    }
    return render(request,'blog/blogs.html',context)

@login_required(login_url="login")
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = str(request.POST.get('blogid'))
        blog = get_object_or_404(Blog,id=id)
        if blog.likes.filter(id = request.user.profile.id).exists():
            blog.likes.remove(request.user.profile)
            result = blog.likes.count()
            blog.save()
        else:
            blog.likes.add(request.user.profile)
            result = blog.likes.count()
            blog.save()
        return JsonResponse({'result': result },status = 200)
    


@login_required(login_url="login")
def createBlog(request):
    profile = request.user.profile
    form = BlogForm()

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = profile
            blog.save()

            return redirect('account')

    context = {'form': form}
    return render(request, "blog/blog_form.html", context)


@login_required(login_url="login")
def updateBlog(request, pk):
    profile = request.user.profile
    blog = profile.blog_set.get(id=pk)
    form = BlogForm(instance=blog)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save()
            return redirect('account')

    context = {'form': form, 'blog': blog}
    return render(request, "blog/blog_form.html", context)

@login_required(login_url="login")
def deleteBlog(request, pk):
    profile = request.user.profile
    blog = profile.blog_set.get(id=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('blogs')
    context = {'object': blog}
    return render(request, 'delete_template.html', context)

    
@login_required(login_url="login")
def favorite_add(request,id):
    blog = get_object_or_404(Blog,id=id)
    if blog.favorites.filter(id=request.user.profile.id).exists():
        blog.favorites.remove(request.user.profile)
    else:
        blog.favorites.add(request.user.profile)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url="login")
def favorites(request):
    favorite_blogs = Blog.objects.filter(favorites=request.user.profile)
    context = {'favorite_blogs':favorite_blogs}
    return render(request,'blog/favorites.html',context)