from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


from .models import Entry
from .forms import EntryForm
from .stats import Stats

def entry_list(request):
    entries = Entry.objects.order_by('-created_date')
    return render(request, 'insight_journal/entry_list.html', {'entries': entries})

def entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    orig_text = entry.text
    stats = Stats(orig_text)
    num_words = stats.getTotalWords()
    tense_dist = stats.getTenseDist()
    polar_scores = stats.getPolarizedScores()
    polar_words = stats.getPolarizedWords()
    return render(request, 'insight_journal/entry.html', {'entry': entry, 'orig_text': orig_text, 'num_words': num_words, 'tense_dist': tense_dist, 'polar_scores': polar_scores, 'polar_words': polar_words})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')

            return redirect('signup')

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

def login(request, user, backend=None):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)

        form = EntryForm(request.POST)

        if user is not None:
            login(request, user)
            return redirect('entry_list')
        else:
            return render(request, 'registration/login.html', {'form': form})

    return render(request, 'registration/login.html', {'form': form})

def logout(request):
    logout(request)
    return redirect('entry_list')

@login_required
def new(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            return redirect('entry', pk=entry.pk)

    else:
        form = EntryForm()

    return render(request, 'insight_journal/new_entry.html', {'form': form})

@login_required
def edit(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            return redirect('entry', pk=entry.pk)
    else:
        form = EntryForm(instance=entry)

    return render(request, 'insight_journal/edit_entry.html', {'form': form})

@login_required
def remove(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    entry.delete()
    return redirect('entry_list')
