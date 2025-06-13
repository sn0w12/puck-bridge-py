"""
Example usage of the Puck Bridge Python package.
This shows how to register custom handlers and access game state.
"""

import time
import threading
from puck_bridge_py import (
    start_server,
    get_game_state,
    get_game_phase,
    get_player_count,
    get_team_balance,
    format_score_string,
    format_game_time,
    get_game_time,
    is_game_in_progress,
    is_game_active,
    is_warmup,
    is_game_over,
    is_scoring_phase,
    register_goal_handler,
    register_player_join_handler,
    get_top_scorers,
    get_performance_stats,
)

# Track connection state to avoid spam
_last_connection_state = None
_last_summary_time = 0


def on_goal_scored(data):
    """Custom handler for goal events using utility functions"""
    team = data.get("team", "unknown")
    players = data.get("players", {})
    goal_player = players.get("goal", {})
    goal_player_name = goal_player.get("username", "unknown")

    print(f"GOAL ALERT! {goal_player_name} scored for team {team}!")
    print(f"   Score: {format_score_string()}")


def on_player_joined(data):
    """Custom handler for player spawn events"""
    if "player" in data:
        player = data["player"]
        username = player.get("username", "unknown")
        team = player.get("team", "none")
        print(f"Player joined: {username} (Team: {team})")

        # Show team balance
        balance = get_team_balance()
        print(f"   Team balance: Blue {balance['blue']} - Red {balance['red']} (Spectators: {balance['spectators']})")


def monitor_game_state():
    """Enhanced monitoring function using utility functions"""
    global _last_connection_state, _last_summary_time

    while True:
        time.sleep(10)
        current_time = time.time()

        # Use the utility function to check connection
        game_state_mgr = get_game_state()
        is_active = game_state_mgr.is_connected() if game_state_mgr else False

        # Handle connection state changes
        if _last_connection_state != is_active:
            if is_active:
                print("\nGame connection detected!")
            else:
                print("\nWaiting for game connection...")
            _last_connection_state = is_active

        # Show detailed summary using utility functions
        if is_active and current_time - _last_summary_time >= 30:
            print(f"\nGame Summary:")
            phase = get_game_phase()
            print(f"   Phase: {phase}")
            print(f"   Time: {format_game_time(get_game_time())}")
            print(f"   Score: {format_score_string()}")

            balance = get_team_balance()
            print(
                f"   Players: {get_player_count()} total ({balance['blue']} blue, {balance['red']} red, {balance['spectators']} spectators)"
            )

            # Show game status with more detailed phase information
            if is_game_over():
                print("   Status: Game Over")
            elif is_warmup():
                print("   Status: Warmup Phase")
            elif is_scoring_phase():
                print("   Status: Goal Celebration")
            elif is_game_in_progress():
                print("   Status: Game in progress")

                # Show leading team
                leading = game_state_mgr.get_leading_team()
                if leading != "tied":
                    diff = game_state_mgr.get_score_difference()
                    print(f"   Leading: {leading.title()} team by {diff}")
                else:
                    print("   Status: Game is tied")
            elif is_game_active():
                print(f"   Status: {phase}")
            else:
                print("   Status: No active game")

            # Show top scorers
            top_scorers = get_top_scorers(3)
            if top_scorers and any(p.goals > 0 for p in top_scorers):
                print("   Top scorers:")
                for i, player in enumerate(top_scorers[:3]):
                    if player.goals > 0:
                        print(f"     {i + 1}. {player.username}: {player.goals} goals")

            # Show performance
            perf = get_performance_stats()
            print(f"   Performance: {perf['current_fps']:.1f} FPS (avg: {perf['average_fps']:.1f})")

            _last_summary_time = current_time


def main():
    # Register handlers using the new utility functions
    register_goal_handler(on_goal_scored)
    register_player_join_handler(on_player_joined)

    # Start the monitoring thread
    monitor_thread = threading.Thread(target=monitor_game_state, daemon=True)
    monitor_thread.start()

    start_server()

    print("Starting Puck Bridge server with enhanced utilities...")
    print("   - Goal alerts enabled")
    print("   - Player join notifications enabled")
    print("   - Enhanced game state monitoring enabled")
    print("   - Waiting for game connection...")


if __name__ == "__main__":
    main()
