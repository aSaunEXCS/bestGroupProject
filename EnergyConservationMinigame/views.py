from django.shortcuts import render, redirect
from django.utils.timezone import now
import random
import time

DEVICES = ["Lamp", "Fan", "TV", "Computer", "Console", "Heater"]
GAME_DURATION = 10

def index(request):
    """Initialize or restore game state."""
    if "game_state" not in request.session:
        request.session["game_state"] = {
            "devices": {device: random.choice([True, False]) for device in DEVICES},
            "score": 10,
            "start_time": time.time()
        }
    
    game_state = request.session["game_state"]
    elapsed_time = (time.time() - game_state["start_time"])

    elapsed_ms = round(elapsed_time * 1000)
 
    if all(not state for state in game_state["devices"].values()):
        game_state["score"] -= elapsed_time
        return render(request, "EnergyConservationMinigame/win.html", {"score": round(game_state["score"], 2), "time_taken": elapsed_ms / 1000})

    if elapsed_time >= GAME_DURATION:
        return redirect("game_over")

    return render(request, "EnergyConservationMinigame/game.html", {"game": game_state, "time_left": round(GAME_DURATION - elapsed_time, 3)})

def toggle_device(request, device_name):
    """Turn on/off a device."""
    game_state = request.session.get("game_state", {})

    if device_name in game_state["devices"]:
        game_state["devices"][device_name] = not game_state["devices"][device_name]

    request.session["game_state"] = game_state
    return redirect("EnergyConservationMinigame_home")

def reset_game(request):
    """Resets the game by clearing the session and redirecting to a new game session."""
    if "game_state" in request.session:
        del request.session["game_state"]
    return redirect("EnergyConservationMinigame_home")

def game_over(request):
    """Show game over screen when time runs out."""
    return render(request, "EnergyConservationMinigame/game_over.html")