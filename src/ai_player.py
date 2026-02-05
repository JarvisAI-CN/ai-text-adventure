"""
AI Player - Autonomous gameplay
AI agent that can play the game autonomously
"""

import random
from typing import Dict, List, Optional
from engine import GameEngine, Scene, GameState


class AIPlayer:
    """AI agent that plays text adventure games"""

    def __init__(self, name: str = "AI Hero", playstyle: str = "balanced"):
        self.name = name
        self.playstyle = playstyle  # aggressive, cautious, balanced, explorer
        self.decision_history = []
        self.personality_traits = self._generate_personality()

    def _generate_personality(self) -> Dict:
        """Generate personality traits based on playstyle"""
        personalities = {
            "aggressive": {
                "fight_chance": 0.8,
                "explore_chance": 0.6,
                "flee_chance": 0.1,
                "talk_chance": 0.3
            },
            "cautious": {
                "fight_chance": 0.3,
                "explore_chance": 0.4,
                "flee_chance": 0.7,
                "talk_chance": 0.6
            },
            "balanced": {
                "fight_chance": 0.5,
                "explore_chance": 0.5,
                "flee_chance": 0.4,
                "talk_chance": 0.5
            },
            "explorer": {
                "fight_chance": 0.4,
                "explore_chance": 0.9,
                "flee_chance": 0.3,
                "talk_chance": 0.7
            }
        }
        return personalities.get(self.playstyle, personalities["balanced"])

    def choose_action(self, scene: Scene, game_state: GameEngine) -> str:
        """Choose an action based on scene and game state"""
        if not scene or not scene.options:
            return "等待"

        # Analyze the situation
        situation = self._analyze_situation(scene, game_state)
        decision = self._make_decision(scene, situation)

        # Record decision
        self._record_decision(scene, situation, decision)

        return decision

    def _analyze_situation(self, scene: Scene, game_state: GameEngine) -> Dict:
        """Analyze current situation"""
        return {
            "has_hostile_npcs": any(npc in ["哥布林", "龙", "怪物", "敌人"] for npc in scene.npcs),
            "has_friendly_npcs": any(npc in ["村民", "商人", "贤者", "向导"] for npc in scene.npcs),
            "has_items": len(scene.items) > 0,
            "visited_before": scene.visited,
            "player_health": game_state.player.health,
            "player_gold": game_state.player.gold,
            "options_count": len(scene.options)
        }

    def _make_decision(self, scene: Scene, situation: Dict) -> str:
        """Make decision based on analysis and personality"""
        # Priority 1: Survival (low health)
        if situation["player_health"] < 30:
            # Look for healing or escape
            for opt in scene.options:
                if "休息" in opt["text"] or "逃跑" in opt["text"] or "返回" in opt["text"]:
                    return opt["text"]

        # Priority 2: Combat decisions
        if situation["has_hostile_npcs"]:
            roll = random.random()
            if roll < self.personality_traits["fight_chance"]:
                # Fight
                for opt in scene.options:
                    if "战斗" in opt["text"] or "攻击" in opt["text"]:
                        return opt["text"]
            elif roll < self.personality_traits["fight_chance"] + self.personality_traits["flee_chance"]:
                # Flee
                for opt in scene.options:
                    if "逃跑" in opt["text"] or "撤退" in opt["text"]:
                        return opt["text"]

        # Priority 3: Collect items
        if situation["has_items"]:
            for opt in scene.options:
                if "拾取" in opt["text"] or "搜索" in opt["text"]:
                    return opt["text"]

        # Priority 4: Talk to NPCs
        if situation["has_friendly_npcs"]:
            if random.random() < self.personality_traits["talk_chance"]:
                for opt in scene.options:
                    if "交谈" in opt["text"] or "对话" in opt["text"]:
                        return opt["text"]

        # Priority 5: Exploration
        if random.random() < self.personality_traits["explore_chance"]:
            # Pick a move option
            move_options = [opt for opt in scene.options if opt.get("action") == "move"]
            if move_options:
                return random.choice(move_options)["text"]

        # Default: Random choice
        return random.choice(scene.options)["text"]

    def _record_decision(self, scene: Scene, situation: Dict, decision: str):
        """Record decision for learning"""
        self.decision_history.append({
            "scene": scene.id,
            "situation": situation,
            "decision": decision,
            "success": None  # Will be updated after action
        })

    def update_decision_outcome(self, success: bool):
        """Update last decision with outcome"""
        if self.decision_history:
            self.decision_history[-1]["success"] = success

    def get_decision_stats(self) -> Dict:
        """Get statistics about decisions"""
        if not self.decision_history:
            return {"total": 0}

        successful = sum(1 for d in self.decision_history if d.get("success"))

        return {
            "total": len(self.decision_history),
            "successful": successful,
            "success_rate": successful / len(self.decision_history) if self.decision_history else 0
        }

    def explore_strategy(self, game_engine: GameEngine) -> str:
        """Plan exploration strategy"""
        health = game_engine.player.health
        gold = game_engine.player.gold

        if health < 30:
            return "cautious"  # Need healing
        elif gold < 10:
            return "aggressive"  # Need resources
        else:
            return "explorer"  # Can explore freely


class AutoPlayer:
    """Automated player for AI vs AI mode"""

    def __init__(self, ai_player: AIPlayer, max_turns: int = 50):
        self.ai_player = ai_player
        self.max_turns = max_turns
        self.turn_count = 0

    def play_auto_game(self, game_engine: GameEngine) -> List[Dict]:
        """Play game automatically and return log"""
        game_log = []
        self.turn_count = 0

        while game_engine.state == GameState.PLAYING and self.turn_count < self.max_turns:
            self.turn_count += 1

            # Get current scene
            scene = game_engine.current_scene
            if not scene:
                break

            # AI makes decision
            action = self.ai_player.choose_action(scene, game_engine)

            # Record turn
            turn_log = {
                "turn": self.turn_count,
                "scene": scene.name,
                "description": scene.description[:50] + "...",
                "action": action,
                "health": game_engine.player.health
            }
            game_log.append(turn_log)

            # Process action
            result, new_scene = game_engine.process_action(action)

            # Print progress
            print(f"[Turn {self.turn_count}] {scene.name}: {action}")
            print(f"  Result: {result[:50]}...")
            print(f"  Health: {game_engine.player.health}")

        return game_log

    def generate_story_from_log(self, game_log: List[Dict]) -> str:
        """Generate a story from game log"""
        story = f"# {self.ai_player.name}的冒险\n\n"

        for turn in game_log:
            story += f"## 第{turn['turn']}回合\n"
            story += f"**地点**: {turn['scene']}\n"
            story += f"**行动**: {turn['action']}\n"
            story += f"**生命值**: {turn['health']}\n\n"

        return story


class AIvsAI:
    """Manager for AI vs AI gameplay"""

    def __init__(self):
        self.players = []

    def create_tournament(self, player_configs: List[Dict]) -> List[Dict]:
        """Create tournament with different AI players"""
        self.players = []

        for config in player_configs:
            player = AIPlayer(
                name=config.get("name", "AI Hero"),
                playstyle=config.get("playstyle", "balanced")
            )
            self.players.append(player)

        return self.players

    def run_match(self, player1: AIPlayer, player2: AIPlayer) -> Dict:
        """Run a match between two AI players"""
        # Create game for player1
        game1 = GameEngine(player_name=player1.name)
        game1.initialize_world()

        # Create game for player2
        game2 = GameEngine(player_name=player2.name)
        game2.initialize_world()

        # Play games
        auto_player1 = AutoPlayer(player1)
        auto_player2 = AutoPlayer(player2)

        log1 = auto_player1.play_auto_game(game1)
        log2 = auto_player2.play_auto_game(game2)

        # Compare results
        return {
            "player1": {
                "name": player1.name,
                "playstyle": player1.playstyle,
                "turns": auto_player1.turn_count,
                "final_health": game1.player.health,
                "stats": player1.get_decision_stats()
            },
            "player2": {
                "name": player2.name,
                "playstyle": player2.playstyle,
                "turns": auto_player2.turn_count,
                "final_health": game2.player.health,
                "stats": player2.get_decision_stats()
            },
            "winner": self._determine_winner(game1, game2)
        }

    def _determine_winner(self, game1: GameEngine, game2: GameEngine) -> str:
        """Determine winner of match"""
        score1 = game1.player.health + len(game1.player.inventory) * 10
        score2 = game2.player.health + len(game2.player.inventory) * 10

        if score1 > score2:
            return game1.player.name
        elif score2 > score1:
            return game2.player.name
        else:
            return "draw"
