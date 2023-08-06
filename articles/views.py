from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse

from .models import Article
from .forms import CommentForm


class CommentGet(DetailView):
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()  # Use the updated CommentForm without 'author'
        return context

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)

class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()  # Get the CommentForm instance
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.author = request.user  # Assign the logged-in user as the author
            comment.article = self.object
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})

class ArticleListView(LoginRequiredMixin,ListView):
    model= Article
    template_name = "article_list.html"

# class ArticleDetailView(DetailView):
#     model = Article
#     template_name= "article_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = CommentForm()
#         return context

class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view=CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)

class ArticleUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Article
    fields = (
        "title",
        "body",
    )
    template_name ="article_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = Article
    template_name= "article_new.html"
    fields = (
        "title",
        "body",
        "image",
    )

    def form_valid(self,form):
        form.instance.author= self.request.user
        return super().form_valid(form)