from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from leaderboard.models import LeaderboardEntry

WASTE_IMAGES = [
    "waste1.jpg", "waste2.jpg", "waste3.jpg", "waste4.jpg", "waste5.jpg",
    "waste6.jpg", "waste7.jpg", "waste8.jpg", "waste9.jpg", "waste10.jpg"
]

CORRECT_ANSWERS = {
    "waste1.jpg": "non-recyclable",
    "waste2.jpg": "non-recyclable",
    "waste3.jpg": "recyclable",
    "waste4.jpg": "recyclable",
    "waste5.jpg": "recyclable",
    "waste6.jpg": "non-recyclable",
    "waste7.jpg": "recyclable",
    "waste8.jpg": "recyclable",
    "waste9.jpg": "recyclable",
    "waste10.jpg": "non-recyclable",
}

@login_required
def waste_game(request):
    if "waste_index" not in request.session:
        request.session["waste_index"] = 0
        request.session["waste_score"] = 0

    if request.method == "POST":
        index = request.session.get("waste_index", 0)
        score = request.session.get("waste_score", 0)
        user_answer = request.POST.get("answer", "").lower().strip()
        current_image = WASTE_IMAGES[index]
        correct = CORRECT_ANSWERS.get(current_image)

        if user_answer == correct:
            score += 100

        index += 1
        request.session["waste_index"] = index
        request.session["waste_score"] = score

        if index >= len(WASTE_IMAGES):
            final_score = score
            entry, created = LeaderboardEntry.objects.get_or_create(
                user=request.user,
                game="Recycling",
                defaults={'score': final_score, 'date': timezone.now()}
            )
            if not created and final_score > entry.score:
                entry.score = final_score
                entry.date = timezone.now()
                entry.save()
            for key in ["waste_index", "waste_score"]:
                if key in request.session:
                    del request.session[key]
            return render(request, "Recycle/win.html", {"score": final_score})
    
    index = request.session.get("waste_index", 0)
    if index < len(WASTE_IMAGES):
        current_image = WASTE_IMAGES[index]
    else:
        current_image = None

    return render(request, "Recycle/game.html", {"image": current_image, "score": request.session.get("waste_score", 0)})
