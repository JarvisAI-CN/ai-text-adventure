#!/usr/bin/env python3
"""
Example usage of AI Text Adventure Game
"""

import sys
sys.path.insert(0, 'src')

from engine import GameEngine, GameState
from dungeon_master import AIDungeonMaster
from ai_player import AIPlayer, AutoPlayer


def example_interactive_game():
    """Example: Play an interactive game"""
    print("=== 互动游戏示例 ===\n")

    # Create game engine
    engine = GameEngine(player_name="Hero")
    engine.initialize_world()

    # Create AI dungeon master
    dm = AIDungeonMaster()

    # Print introduction
    print(dm.introduce_game())
    print()

    # Play a few turns
    for turn in range(3):
        scene = engine.current_scene
        if not scene:
            break

        # Describe scene
        description = dm.describe_scene(scene)
        print(f"📍 {scene.name}")
        print(description)
        print()

        # Auto-select an action for demo
        if scene.options:
            action = scene.options[0]["text"]
            print(f"自动选择: {action}")
            result, _ = engine.process_action(action)
            print(f"\n结果: {result}\n")

    print("示例结束！")


def example_ai_play():
    """Example: Watch AI play"""
    print("=== AI玩家示例 ===\n")

    # Create AI player with explorer personality
    ai_player = AIPlayer(name="Explorer Bot", playstyle="explorer")

    # Initialize game
    engine = GameEngine(player_name=ai_player.name)
    engine.initialize_world()

    # Create auto player
    auto_player = AutoPlayer(ai_player, max_turns=5)

    # Play automatically
    print(f"AI玩家 ({ai_player.playstyle}) 开始游戏...\n")
    game_log = auto_player.play_auto_game(engine)

    # Print results
    print("\n=== 游戏结果 ===")
    print(f"总回合: {auto_player.turn_count}")
    print(f"最终生命: {engine.player.health}")
    print(f"金币: {engine.player.gold}")
    print(f"物品: {', '.join(engine.player.inventory)}")

    # Print decision stats
    stats = ai_player.get_decision_stats()
    print(f"\n决策统计:")
    print(f"总决策: {stats['total']}")
    print(f"成功率: {stats['success_rate']:.1%}")


def example_custom_world():
    """Example: Create custom world"""
    print("=== 自定义世界示例 ===\n")

    # Create custom world
    custom_world = {
        "name": "科幻空间站",
        "description": "2157年，你在一艘废弃的空间站醒来",
        "start_scene": "cryo_room",
        "scenes": {
            "cryo_room": {
                "id": "cryo_room",
                "name": "冷冻室",
                "description": "你从低温冷冻舱中醒来。警报灯闪烁，空气中弥漫着奇怪的气味。",
                "options": [
                    {"text": "检查电脑终端", "action": "search"},
                    {"text": "离开房间", "action": "move", "target": "corridor"},
                    {"text": "寻找其他幸存者", "action": "search"}
                ],
                "items": ["身份卡", "急救包"],
                "npcs": []
            },
            "corridor": {
                "id": "corridor",
                "name": "走廊",
                "description": "走廊延伸到黑暗中。你听到远处传来机械运转的声音。",
                "options": [
                    {"text": "向左走", "action": "move", "target": "bridge"},
                    {"text": "向右走", "action": "move", "target": "engineering"},
                    {"text": "返回冷冻室", "action": "move", "target": "cryo_room"}
                ],
                "items": [],
                "npcs": []
            }
        }
    }

    # Initialize game with custom world
    engine = GameEngine(player_name="Commander")
    engine.initialize_world(custom_world)

    # Print scene
    scene = engine.current_scene
    print(f"📍 {scene.name}")
    print(scene.description)
    print(f"\n物品: {', '.join(scene.items)}")
    print("\n选项:")
    for i, opt in enumerate(scene.options, 1):
        print(f"{i}. {opt['text']}")


def example_save_load():
    """Example: Save and load game"""
    print("=== 存档/读档示例 ===\n")

    # Create and play a game
    engine = GameEngine(player_name="Tester")
    engine.initialize_world()

    # Make a move
    engine.process_action("1")

    # Save game
    save_file = engine.save_game("/tmp/test_save.json")
    print(f"✅ 游戏已保存: {save_file}")

    # Create new engine and load
    engine2 = GameEngine()
    engine2.initialize_world()
    engine2.load_game(save_file)

    print(f"✅ 游戏已读取")
    print(f"玩家: {engine2.player.name}")
    print(f"生命: {engine2.player.health}")
    print(f"历史: {len(engine2.history)}条记录")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Text Adventure Examples")
    parser.add_argument("--example", choices=["play", "ai", "custom", "save"],
                       default="play", help="Example to run")

    args = parser.parse_args()

    if args.example == "play":
        example_interactive_game()
    elif args.example == "ai":
        example_ai_play()
    elif args.example == "custom":
        example_custom_world()
    elif args.example == "save":
        example_save_load()
