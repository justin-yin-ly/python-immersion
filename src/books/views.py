from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book

#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/main.html'

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/detail.html'