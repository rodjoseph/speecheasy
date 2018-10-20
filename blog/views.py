from django.shortcuts import render, get_object_or_404
from blog.models import Post
from users.models import Follow, Profile
import sys
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def is_users(post_user, logged_user):
    return post_user == logged_user


PAGINATION_COUNT = 5


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = PAGINATION_COUNT

    def get_queryset(self):
        user = self.request.user
        qs = Follow.objects.filter(user=user)
        follows = [user]
        for obj in qs:
            follows.append(obj.follow_user)
        return Post.objects.filter(author__in=follows).order_by('-date_posted')


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION_COUNT

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user
        can_follow = (Follow.objects.filter(user=logged_user,
                                            follow_user=visible_user).count() == 0)
        data = super().get_context_data(**kwargs)

        data['user_profile'] = visible_user
        data['can_follow'] = can_follow
        return data

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def follow_saver(self, request, num_to_add):
        our_profile = Profile.objects.filter(user=request.user).first()
        our_profile.following += num_to_add
        our_profile.save()
        their_profile = Profile.objects.filter(user=self.visible_user()).first()
        their_profile.followers += num_to_add
        their_profile.save()

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follows_between = Follow.objects.filter(user=request.user,
                                                    follow_user=self.visible_user())

            if 'follow' in request.POST:
                    new_relation = Follow(user=request.user, follow_user=self.visible_user())
                    if follows_between.count() == 0:
                        new_relation.save()
                        self.follow_saver(request, 1)
            elif 'unfollow' in request.POST:
                    if follows_between.count() > 0:
                        follows_between.delete()
                        self.follow_saver(request, -1)

        return self.get(self, request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    template_name = 'blog/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add a new post'
        return data


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    template_name = 'blog/post_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Edit a post'
        return data


def about(request):
    return render(request, 'blog/about.html')