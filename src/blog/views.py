from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # automatically data is sent from model to template as object_list
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # automatically data is sent from model to template as object_list
    context_object_name = 'posts'
    # ordering = ['-date_posted'] This is affected by the get_queryset and hence to avoid it.... put it in the function
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post # automatically data is sent to model as object
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self): # function of UserPassesTestMixin
        post = self.get_object() # gets currently accessing object i.e user data
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post # automatically data is sent to model as object
    success_url = '/'

    def test_func(self): # to verify if a post belongs to the logged in user 
        post = self.get_object() # gets currently accessing object i.e user data
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})