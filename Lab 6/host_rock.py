import paho.mqtt.client as mqtt
import time
from collections import defaultdict

broker = "farlab.infosci.cornell.edu"
port = 1883
username = "idd"
password = "device@theFarm"

ROUND_DURATION = 10  # seconds per round

# --- State ---
choices = {}
active_players = set()
round_active = False
game_active = False

# --- MQTT Setup ---
client = mqtt.Client()
client.username_pw_set(username, password)


def determine_winner(players_choices):
    """Determine which choice wins overall."""
    unique_choices = set(players_choices.values())

    # Tie if everyone picked the same or all three present
    if len(unique_choices) == 1 or len(unique_choices) == 3:
        return None

    # Two-move cases
    if unique_choices == {"rock", "scissors"}:
        return "rock"
    if unique_choices == {"scissors", "paper"}:
        return "scissors"
    if unique_choices == {"paper", "rock"}:
        return "paper"


def on_message(client, userdata, msg):
    global round_active, choices, active_players, game_active
    player = msg.topic.split("/")[-1]
    choice = msg.payload.decode().strip().lower()

    if choice not in ["rock", "paper", "scissors"]:
        return

    if not game_active:
        # Game is idle -> start a new one automatically
        game_active = True
        active_players.clear()
        print(f"New game started by {player}!")
        announce("New game starting! Waiting for players...")
        time.sleep(2)

    if not round_active:
        print(f"{player} played early, will count next round.")
        active_players.add(player)
        return

    # During a round
    choices[player] = choice
    active_players.add(player)
    print(f"{player} chose {choice}")


def announce(message):
    print(message)
    client.publish("IDD/rps/status", message)


def start_round():
    global round_active, choices
    if not active_players:
        announce("⏸No active players. Waiting for new players to join...")
        return False

    choices = {}
    round_active = True
    announce(f"\nNew round! You have {ROUND_DURATION} seconds to play.")
    countdown = ROUND_DURATION
    while countdown > 0:
        print(f" {countdown}s remaining...", end="\r")
        time.sleep(1)
        countdown -= 1

    round_active = False

    if not choices:
        announce("No moves received. Waiting for players...")
        return False

    winner_choice = determine_winner(choices)
    if winner_choice is None:
        announce(f"It's a tie! Everyone stays in. ({choices})")
        return True

    survivors = [p for p, c in choices.items() if c == winner_choice]
    eliminated = [p for p in active_players if p not in survivors]

    announce(f"Winning move: {winner_choice.upper()}")
    announce(f"Survivors: {', '.join(survivors)}")
    if eliminated:
        announce(f"Eliminated: {', '.join(eliminated)}")

    active_players.clear()
    active_players.update(survivors)

    # Game end conditions
    if len(active_players) == 1:
        announce(f"Game Over! Champion: {list(active_players)[0]}")
        return False
    elif len(active_players) == 0:
        announce("Everyone eliminated! No winner.")
        return False
    else:
        return True


def game_loop():
    global game_active
    announce("Rock-Paper-Scissors Elimination Host Ready!")
    while True:
        if not game_active:
            time.sleep(1)
            continue  # wait for a player to start a game

        keep_playing = start_round()
        if not keep_playing:
            announce("Game finished. Waiting for new players...")
            game_active = False
            time.sleep(3)
        else:
            time.sleep(3)


# --- MQTT Bindings ---
client.on_message = on_message
client.connect(broker, port)
client.subscribe("IDD/rps/choices/#")
client.loop_start()

try:
    game_loop()
except KeyboardInterrupt:
    print("\nStopping host...")
finally:
    client.loop_stop()
    client.disconnect()
