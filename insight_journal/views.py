from django.shortcuts import render

def entry_list(request):
    return render(request, 'insight_journal/entry_list.html', {})
