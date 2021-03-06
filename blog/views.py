from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import HttpResponse
from .forms import emailForm, CommentForm
from django.core.mail import send_mail
from mysite import credentials  # python file to store sensitive data
from taggit.models import Tag
from django.db.models import Count


def post_list(request, tag_slug=None):
    published_posts = Post.published.all()
    # a paginator object , attributes -> count, num_pages, page_range

    # TAGGING
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        published_posts = published_posts.filter(tags__in=[tag])

    # PAGINATION
    paginator = Paginator(published_posts, 2, orphans=1)
    # get current page number of the content from GET request
    page_number = request.GET.get('page')
    # print(request.GET.get.__doc__)
    try:
        # a Page object,to retrieve items of given page number
        # methods - has_next(), has_previous(), has_other_pages, next_page_number() etc
        posts = paginator.page(page_number)

    except PageNotAnInteger:
        # if no previous page, get items of 1st page
        posts = paginator.page(1)
    except EmptyPage:
        # if no next page,get items of the last number of page
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})


def post_details(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )

    comment_made = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Only creates a Comment() obj, does not save to db
            comment_made = comment_form.save(commit=False)
            comment_made.post = post  # bind this comment to this post
            comment_made.save()
            print(comment_made.post)
        # print(comment_form)

    else:
        comment_made = comment_made
        comment_form = CommentForm()

    # to get existed comment for this post
    comments = post.comment.filter(active='True')

    # Pagination for maximum 3 comment per page
    paginator = Paginator(comments, 3)
    page = request.GET.get('page')

    try:
        page_comments = paginator.page(page)
    except EmptyPage:
        page_comments = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page_comments = paginator.page(1)

    # RETRIEVING SIMILAR POST
    tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {
        'post': post, 'comment_form': comment_form,
        'page_comments': page_comments,
        'comment_made': comment_made,
        'similar_posts': similar_posts})


def share(request, post_id):
    print(credentials.USER)
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'GET':
        form = emailForm()
    else:
        form = emailForm(request.POST)
        # print(dir(form))
        if form.is_valid():
            submitted_data = form.cleaned_data  # returns a dictionary of the form data
            # print(submitted_data['name'])
            print(submitted_data)

            # necessary email fields - subject, message, from email, recipient list
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # there is build_absolute_uri method in request
            # print(request.build_absolute_uri.__doc__)
            subject = f"{submitted_data['name']} wants you to read {post.title}"
            recipient_mail = submitted_data['recipient_email']
            body = f"Read {post.title} at {post_url}\n\n {submitted_data['name']}'s comment about this book is \n {submitted_data['comment']}"
            send_mail(subject=subject, message=body,
                      from_email='16103213@iubat.edu', recipient_list=[recipient_mail])
            sent = True

    return render(request, 'blog/post/share_email.html', {'form': form, 'post': post, 'sent': sent})
