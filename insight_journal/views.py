from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
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

def stats(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    orig_text = entry.text
    stats = Stats(orig_text)
    num_words = stats.getTotalWords()
    tense_dist = stats.getTenseDist()
    polar_scores = stats.getPolarizedScores()
    polar_words = stats.getPolarizedWords()

    return render(request, 'insight_journal/testing.html', {'num_words': num_words, 'tense_dist': tense_dist, 'polar_scores': polar_scores, 'polar_words': polar_words})
