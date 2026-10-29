"""
Services for the dashboard app.

Business logic for calculating progress, filtering challenges, etc.
"""
from . import mock_data


def get_weekly_progress():
    """Calculate progress for each week."""
    weeks = mock_data.WEEKS
    progress = []
    
    for week in weeks:
        completed = sum(1 for c in week['challenges'] if c['status'] == 'completed')
        total = len(week['challenges'])
        percentage = (completed / total * 100) if total > 0 else 0
        
        progress.append({
            'week': week['week'],
            'title': week['title'],
            'completed': completed,
            'total': total,
            'percentage': round(percentage, 1),
        })
    
    return progress


def get_challenges():
    """Return all challenges from mock data."""
    challenges = []
    for week in mock_data.WEEKS:
        for challenge in week['challenges']:
            challenges.append(challenge)
    return challenges


def get_overall_progress():
    """Calculate overall progress across all weeks."""
    total_completed = 0
    total_challenges = 0
    
    for week in mock_data.WEEKS:
        total_challenges += len(week['challenges'])
        total_completed += sum(1 for c in week['challenges'] if c['status'] == 'completed')
    
    percentage = (total_completed / total_challenges * 100) if total_challenges > 0 else 0
    
    return {
        'completed': total_completed,
        'total': total_challenges,
        'percentage': round(percentage, 1),
    }

