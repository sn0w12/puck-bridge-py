# Puck Bridge Python

A Python library for connecting to and interacting with [Puck](https://store.steampowered.com/app/2994020/Puck/) servers. This package provides real-time game state tracking, event handling, and server management capabilities. The [PuckBridgeMod](https://github.com/sn0w12/PuckBridgeMod) is required to be on the server.

## Features

-   Real-time game state monitoring
-   Player statistics and performance tracking
-   Event-driven architecture with custom handlers
-   Goal scoring and player action notifications
-   Team balance and player management
-   Server administration commands
-   Performance metrics and FPS monitoring
-   Easy-to-use utility functions
-   **Supports multiple servers at once via instance-based API**

## Installation

```bash
pip install puck-bridge-py
```

Or install from source:

```bash
git clone https://github.com/sn0w12/puckbridgepy.git
cd puckbridge
pip install -e .
```

## Quick Start (Instance-based API)

```python
from puck_bridge_py import PuckBridge, Commands, Utilities

bridge = PuckBridge(host="127.0.0.1", port=9000)
bridge.start_server(blocking=True)

commands = Commands(bridge)
utilities = Utilities(bridge)

def on_goal_scored(data):
    team = data.get("team", "unknown")
    player = data.get("players", {}).get("goal", {})
    player_name = player.get("username", "unknown")
    print(f"GOAL! {player_name} scored for {team}!")
    print(f"Current score: {utilities.get_current_score()}")

utilities.register_goal_handler(on_goal_scored)
```

## Multi-Server Example

You can run multiple servers at once, each with their own state and handlers:

```python
from puck_bridge_py import PuckBridge, Commands, Utilities

bridge1 = PuckBridge(host="127.0.0.1", port=9000)
bridge2 = PuckBridge(host="127.0.0.1", port=9001)

bridge1.start_server(blocking=False)
bridge2.start_server(blocking=False)

commands1 = Commands(bridge1)
utilities1 = Utilities(bridge1)

commands2 = Commands(bridge2)
utilities2 = Utilities(bridge2)

def on_goal1(data):
    print("Bridge1 goal:", data)
utilities1.register_goal_handler(on_goal1)

def on_goal2(data):
    print("Bridge2 goal:", data)
utilities2.register_goal_handler(on_goal2)

commands1.send_system_message("Hello from server 1!")
commands2.send_system_message("Hello from server 2!")
```

## Core Concepts

### Game State Management

The library automatically tracks:

-   **Players**: Names, teams, statistics, connection status
-   **Game State**: Score, time, period, game phase
-   **Performance**: FPS, server performance metrics

### Event System

Register handlers for specific game events:

-   `goal_scored` - When a goal is scored
-   `player_spawned` - When a player joins
-   `player_despawned` - When a player leaves
-   `game_state` - When game state changes

**Game Phases:**

-   `None` - No active game
-   `Warmup` - Pre-game warmup period
-   `FaceOff` - Face-off is about to begin
-   `Playing` - Active gameplay
-   `BlueScore` - Blue team scored (celebration phase)
-   `RedScore` - Red team scored (celebration phase)
-   `Replay` - Goal replay is being shown
-   `PeriodOver` - Current period has ended
-   `GameOver` - Game has completely finished

## API Reference

### Instance-based API

#### Server Management

```python
bridge = PuckBridge(host="127.0.0.1", port=9000)
bridge.start_server(blocking=True)  # or blocking=False for non-blocking
bridge.is_connected()  # Check if connected to game
```

#### Game State

```python
game_state_mgr = bridge.get_game_state()
utilities = Utilities(bridge)
utilities.get_current_score()
utilities.get_game_phase()
utilities.get_game_time()
utilities.is_game_in_progress()
utilities.is_game_paused()
utilities.is_game_active()
utilities.is_period_over()
utilities.is_game_over()
utilities.is_warmup()
utilities.is_scoring_phase()
```

#### Player Management

```python
utilities.get_all_players()
utilities.get_player_by_username(username)
utilities.get_blue_players()
utilities.get_red_players()
utilities.get_top_scorers(limit=5)
```

#### Team Information

```python
utilities.get_team_balance()
utilities.get_player_count()
```

#### Utilities

```python
utilities.format_game_time(seconds)
utilities.format_score_string()
utilities.get_performance_stats()
```

#### Event Registration

```python
utilities.register_goal_handler(handler)
utilities.register_player_join_handler(handler)
utilities.register_player_leave_handler(handler)
utilities.register_game_state_handler(handler)
```

#### Commands

```python
commands = Commands(bridge)
commands.send_system_message(message)
commands.restart_game(reason)
commands.kick_player(steam_id, reason)
commands.kick_player_by_name(username, reason)
```

### Data Classes

#### Player

```python
@dataclass
class Player:
    client_id: int
    username: str
    state: str = "unknown"
    team: str = "none"  # "blue", "red", or "none"
    role: str = "none"
    number: int = 0
    goals: int = 0
    assists: int = 0
    ping: int = 0
    handedness: str = "right"
    country: str = ""
    steam_id: str = ""
    patreon_level: int = 0
    admin_level: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
```

#### GameState

```python
@dataclass
class GameState:
    phase: str = "unknown"  # "None", "Warmup", "FaceOff", "Playing", "BlueScore", "RedScore", "Replay", "PeriodOver", "GameOver"
    time: float = 0.0
    period: int = 0
    blue_score: int = 0
    red_score: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
```

#### Performance

```python
@dataclass
class Performance:
    current_fps: float = 0.0
    min_fps: float = 0.0
    average_fps: float = 0.0
    max_fps: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)
```

## Configuration

### Server Configuration

The server can be configured with custom host and port settings:

```python
from puck_bridge_py import PuckBridge

# Default configuration (127.0.0.1:9000)
bridge = PuckBridge()
bridge.start_server()

# Custom port
bridge = PuckBridge(port=9001)
bridge.start_server()

# Custom host and port
bridge = PuckBridge(host="0.0.0.0", port=8080)
bridge.start_server()

# Listen on all interfaces
bridge = PuckBridge(host="0.0.0.0")
bridge.start_server()
```

**Default Settings:**

-   Host: `127.0.0.1` (localhost only)
-   Port: `9000`

**Security Note:** Using `0.0.0.0` as the host will make the server accessible from other machines on the network. Only use this if you understand the security implications.

### Game Setup

1. Start your Puck Bridge Python server (with desired host/port)
2. Configure your Puck game to connect to the correct address
3. Join a game - the library will automatically start receiving data

**Default Connection:** `127.0.0.1:9000`

## Usage Examples

### Basic Game Monitoring

```python
import time
import threading
from puck_bridge_py import PuckBridge, Utilities

bridge = PuckBridge()
utilities = Utilities(bridge)

def monitor_game():
    while True:
        if utilities.get_player_count() > 0:
            phase = utilities.get_game_phase()
            score = utilities.get_current_score()
            time_str = utilities.format_game_time(utilities.get_game_time())

            print(f"Phase: {phase} | Time: {time_str} | Score: Blue {score['blue']} - Red {score['red']}")

        time.sleep(10)

threading.Thread(target=monitor_game, daemon=True).start()
bridge.start_server()
```

### Advanced Event Handling

```python
from puck_bridge_py import PuckBridge, Utilities

bridge = PuckBridge()
utilities = Utilities(bridge)

def on_goal_scored(data):
    team = data.get("team")
    players = data.get("players", {})
    scorer = players.get("goal", {}).get("username", "Unknown")

    assists = []
    for assist_key in ["assist1", "assist2"]:
        if assist_key in players:
            assists.append(players[assist_key].get("username", "Unknown"))

    print(f"GOAL by {scorer} ({team})")
    if assists:
        print(f"   Assists: {', '.join(assists)}")

    top_scorers = utilities.get_top_scorers(3)
    print("   Top Scorers:")
    for i, player in enumerate(top_scorers):
        if player.goals > 0:
            print(f"     {i+1}. {player.username}: {player.goals}G {player.assists}A")

def on_player_joined(data):
    player = data.get("player", {})
    username = player.get("username", "Unknown")
    team = player.get("team", "none")

    print(f"{username} joined (Team: {team})")

    balance = utilities.get_team_balance()
    print(f"   Teams: Blue {balance['blue']} - Red {balance['red']}")

utilities.register_goal_handler(on_goal_scored)
utilities.register_player_join_handler(on_player_joined)

bridge.start_server()
```

### Server Administration

```python
from puck_bridge_py import PuckBridge, Commands, Utilities

bridge = PuckBridge()
commands = Commands(bridge)
utilities = Utilities(bridge)

def admin_commands():
    while True:
        command = input("Admin> ").strip().lower()

        if command.startswith("kick "):
            username = command[5:]
            if commands.kick_player_by_name(username, "Kicked by admin"):
                print(f"Kicked {username}")
            else:
                print(f"Failed to kick {username}")

        elif command == "restart":
            if commands.restart_game("Game restarted by admin"):
                print("Game restarted")
            else:
                print("Failed to restart game")

        elif command.startswith("msg "):
            message = command[4:]
            if commands.send_system_message(f"[ADMIN] {message}"):
                print("Message sent")
            else:
                print("Failed to send message")

        elif command == "players":
            players = utilities.get_all_players()
            for player in players.values():
                print(f"  {player.username} (Team: {player.team}, Goals: {player.goals})")

        elif command == "quit":
            break

import threading
threading.Thread(target=admin_commands, daemon=True).start()
bridge.start_server()
```

### Performance Monitoring

```python
from puck_bridge_py import PuckBridge, Utilities
import time

bridge = PuckBridge()
utilities = Utilities(bridge)

def performance_monitor():
    while True:
        if utilities.is_connected():
            stats = utilities.get_performance_stats()
            player_count = utilities.get_player_count()

            print(f"Performance: {stats['current_fps']:.1f} FPS "
                  f"(avg: {stats['average_fps']:.1f}) | "
                  f"Players: {player_count}")

        time.sleep(5)

import threading
threading.Thread(target=performance_monitor, daemon=True).start()
bridge.start_server()
```

## Event Data Structures

### Goal Scored Event

```python
{
    "team": "blue",  # or "red"
    "scores": {"blue": 1, "red": 0},
    "players": {
        "goal": {"username": "PlayerName", "clientId": 123},
        "assist1": {"username": "AssistPlayer", "clientId": 124},  # optional
        "assist2": {"username": "AssistPlayer2", "clientId": 125}  # optional
    }
}
```

### Player Spawned Event

```python
{
    "player": {
        "clientId": 123,
        "username": "PlayerName",
        "team": "blue",
        "state": "playing",
        "goals": 0,
        "assists": 0,
        # ... other player fields
    }
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
