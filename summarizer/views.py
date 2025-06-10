from django.shortcuts import render,redirect
from transformers import pipeline
from . forms import TextForm,RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/login/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


summarize = pipeline("summarization", model="facebook/bart-large-cnn")

@login_required
def home(request):
    summary = None
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            summary = summarize(text, max_length=120, min_length=10, do_sample=False)[0]['summary_text']
    else:
        form = TextForm()
    
    return render(request, "home.html", {"form": form, "summary": summary})


def logout_view(request):
    logout(request)
    return redirect('/login/')
