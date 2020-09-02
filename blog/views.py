from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def post_list(request):
    published_posts = Post.published.all()
    # a paginator object , attributes -> count, num_pages, page_range
    paginator = Paginator(published_posts, 2, orphans=1)
    # get current page number of the content
    page_number = request.GET.get('page')
    # print(request.GET.get.__doc__)
    try:
        # a Page object,to retrieve items of given page number
        # methods - has_next(), has_previous(), has_other_pages, next_page_number() etc
        posts = paginator.page(page_number)
        print(posts.has_previous)

    except PageNotAnInteger:
        # if no previous page, get items of 1st page
        posts = paginator.page(1)
    except EmptyPage:
        # if no next page,get items of the last number of page
        posts = paginator.page(paginator.num_pages)
        
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_details(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )

    return render(request, 'blog/post/detail.html', {'post': post})
