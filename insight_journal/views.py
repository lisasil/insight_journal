from django.shortcuts import render, get_object_or_404
from .models import Entry
from .forms import EntryForm
from django.shortcuts import redirect

def entry_list(request):
    entries = Entry.objects.order_by('-title')
    return render(request, 'insight_journal/entry_list.html', {'entries': entries})

def entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'insight_journal/entry.html', {'entry': entry})

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
