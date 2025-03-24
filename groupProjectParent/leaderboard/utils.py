from .models import LeaderboardEntry, Badge
from UserProfile.models import Profile

def update_badges():
    best_overall = LeaderboardEntry.objects.all().order_by('-score').first()
    if best_overall:
        badge_overall, created = Badge.objects.get_or_create(
            name="Best Overall",
            defaults={'description': "Highest overall score across all minigames"}
        )
        for profile in Profile.objects.all():
            if profile.user == best_overall.user:
                profile.badges.add(badge_overall)
            else:
                if badge_overall in profile.badges.all():
                    profile.badges.remove(badge_overall)

    games = ["Energy Conservation", "Quiz", "Cycling", "Recycling"]
    for game in games:
        best_game = LeaderboardEntry.objects.filter(game=game).order_by('-score').first()
        if best_game:
            badge_name = f"Best {game}"
            badge_game, created = Badge.objects.get_or_create(
                name=badge_name,
                defaults={'description': f"Highest score in {game}"}
            )
            for profile in Profile.objects.all():
                if profile.user == best_game.user:
                    profile.badges.add(badge_game)
                else:
                    if badge_overall in profile.badges.all():
                        profile.badges.remove(badge_game)
