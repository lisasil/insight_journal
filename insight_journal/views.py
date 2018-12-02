from django.shortcuts import render, get_object_or_404
from .models import Entry

def entry_list(request):
    entries = Entry.objects.order_by('-title')
    return render(request, 'insight_journal/entry_list.html', {'entries': entries})

def entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'insight_journal/entry.html', {'entry': entry})
