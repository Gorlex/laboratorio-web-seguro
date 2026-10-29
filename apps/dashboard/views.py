from django.shortcuts import render
from .services import get_weekly_progress, get_challenges, get_overall_progress

def index(request):
    """Dashboard view that displays weekly progress and challenges."""
    weekly_progress = get_weekly_progress()
    overall_progress = get_overall_progress()
    challenges = get_challenges()
    
    context = {
        'weekly_progress': weekly_progress,
        'overall_progress': overall_progress,
        'challenges': challenges,
    }
    
    return render(request, 'dashboard/index.html', context)
