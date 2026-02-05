"""
Command Line Interface for AI Text Adventure
"""

import sys
import argparse
from engine import GameEngine, GameState
from dungeon_master import AIDungeonMaster
from ai_player import AIPlayer, AutoPlayer, AIvsAI


class GameCLI:
    """Command-line interface for the game"""

    def __init__(self):
        self.engine = None
        self.dm = AIDungeonMaster()

    def print_banner(self):
        """Print game banner"""
        print("""
╔═════════════════════════════════════════════════════════╗
║     🤖 AI Text Adventure - 文字冒险游戏 🤖              ║
║     由AI驱动的无尽冒险世界                               ║
╚═════════════════════════════════════════════════════════╝
""")

    def start_interactive_game(self, player_name: str = "Hero"):
        """Start interactive game"""
        self.print_banner()
        print(self.dm.introduce_game())
        print()

        # Initialize game
        self.engine = GameEngine(player_name=player_name)
        self.engine.initialize_world()

        # Game loop
        while self.engine.state == GameState.PLAYING:
            # Get current scene
            scene = self.engine.current_scene
            if not scene:
                break

            # Describe scene
            description = self.dm.describe_scene(scene, {
                "player_health": self.engine.player.health,
                "time_of_day": "day"
            })
            print(f"\n📍 {scene.name}")
            print(description)
            print()

            # Get player input
            action = input("你的选择: ").strip()

            if not action:
                continue

            if action.lower() in ["quit", "exit", "q"]:
                print("👋 感谢游玩！")
                break

            # Process action
            result, new_scene = self.engine.process_action(action)
            print(f"\n{result}")

            # Check win/lose conditions
            if self.engine.state == GameState.WON:
                print(self.dm.congratulate_victory(self.engine.player.name))
                break
            elif self.engine.state == GameState.LOST:
                print("\n💀 游戏结束..."
                break

    def start_ai_vs_ai(self):
        """Start AI vs AI mode"""
        self.print_banner()
        print("\n🤖 AI对战模式\n")

        # Create different AI players
        tournament = AIvsAI()
        players_config = [
            {"name": "勇者A", "playstyle": "aggressive"},
            {"name": "智者B", "playstyle": "cautious"},
            {"name": "探险家C", "playstyle": "explorer"}
        ]

        players = tournament.create_tournament(players_config)

        # Run matches
        print("比赛开始！\n")
        for i in range(len(players) - 1):
            player1 = players[i]
            player2 = players[i + 1]

            print(f"\n⚔️  {player1.name} vs {player2.name}")
            print("=" * 50)

            result = tournament.run_match(player1, player2)

            print(f"\n{player1.name} ({player1.playstyle}):")
            print(f"  回合: {result['player1']['turns']}")
            print(f"  生命值: {result['player1']['final_health']}")
            print(f"  决策成功率: {result['player1']['stats']['success_rate']:.1%}")

            print(f"\n{player2.name} ({player2.playstyle}):")
            print(f"  回合: {result['player2']['turns']}")
            print(f"  生命值: {result['player2']['final_health']}")
            print(f"  决策成功率: {result['player2']['stats']['success_rate']:.1%}")

            print(f"\n🏆 胜者: {result['winner']}")

    def watch_ai_play(self, playstyle: str = "balanced"):
        """Watch AI play the game"""
        self.print_banner()
        print(f"\n🤖 AI玩家模式 (风格: {playstyle})\n")

        # Create AI player
        ai_player = AIPlayer(name="AI Hero", playstyle=playstyle)

        # Initialize game
        self.engine = GameEngine(player_name=ai_player.name)
        self.engine.initialize_world()

        # Auto play
        auto_player = AutoPlayer(ai_player, max_turns=20)
        game_log = auto_player.play_auto_game(self.engine)

        # Print summary
        print("\n📊 游戏总结:")
        print(f"总回合: {auto_player.turn_count}")
        print(f"最终生命: {self.engine.player.health}")
        print(f"背包物品: {', '.join(self.engine.player.inventory)}")

        # Generate story
        print("\n📖 冒险故事:")
        story = auto_player.generate_story_from_log(game_log)
        print(story[:500] + "...")

    def show_status(self):
        """Show current game status"""
        if not self.engine:
            print("游戏未开始")
            return

        status = self.engine.get_status()
        print("\n📊 游戏状态:")
        print(f"状态: {status['state']}")
        print(f"玩家: {status['player']['name']}")
        print(f"生命: {status['player']['health']}")
        print(f"金币: {status['player']['gold']}")
        print(f"物品: {', '.join(status['player']['inventory'])}")
        print(f"当前位置: {status['current_scene']}")

    def save_game(self, filename: str = None):
        """Save current game"""
        if not self.engine:
            print("游戏未开始")
            return

        save_file = self.engine.save_game(filename)
        print(f"✅ 游戏已保存: {save_file}")

    def generate_story(self):
        """Generate story summary"""
        if not self.engine:
            print("游戏未开始")
            return

        story = self.engine.get_story_summary()
        print("\n📖 " + story)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AI Text Adventure Game")
    parser.add_argument("--mode", choices=["play", "ai-vs-ai", "watch-ai"], default="play",
                       help="Game mode")
    parser.add_argument("--player", default="Hero", help="Player name")
    parser.add_argument("--playstyle", choices=["aggressive", "cautious", "balanced", "explorer"],
                       default="balanced", help="AI playstyle")

    args = parser.parse_args()

    cli = GameCLI()

    if args.mode == "play":
        cli.start_interactive_game(args.player)
    elif args.mode == "ai-vs-ai":
        cli.start_ai_vs_ai()
    elif args.mode == "watch-ai":
        cli.watch_ai_play(args.playstyle)


if __name__ == "__main__":
    main()
