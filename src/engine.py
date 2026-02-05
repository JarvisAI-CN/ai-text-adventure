"""
AI Text Adventure Game Engine
Core game logic and state management
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class GameState(Enum):
    """Game states"""
    START = "start"
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"
    QUIT = "quit"


@dataclass
class Player:
    """Player state"""
    name: str
    health: int = 100
    gold: int = 50
    inventory: List[str] = None
    quests: List[str] = None

    def __post_init__(self):
        if self.inventory is None:
            self.inventory = []
        if self.quests is None:
            self.quests = []


@dataclass
class Scene:
    """A game scene"""
    id: str
    name: str
    description: str
    options: List[Dict[str, str]] = None
    items: List[str] = None
    npcs: List[str] = None
    visited: bool = False

    def __post_init__(self):
        if self.options is None:
            self.options = []
        if self.items is None:
            self.items = []
        if self.npcs is None:
            self.npcs = []


class GameEngine:
    """Main game engine"""

    def __init__(self, player_name: str = "Hero"):
        self.player = Player(name=player_name)
        self.state = GameState.START
        self.current_scene: Optional[Scene] = None
        self.history: List[Dict] = []
        self.game_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # World data
        self.scenes = {}
        self.world_data = {}

    def initialize_world(self, world_data: Dict = None):
        """Initialize game world"""
        if world_data is None:
            world_data = self._generate_default_world()

        self.world_data = world_data
        self.scenes = {
            scene_id: Scene(**scene_data)
            for scene_id, scene_data in world_data.get("scenes", {}).items()
        }

        # Start at first scene
        first_scene_id = world_data.get("start_scene", "forest_entrance")
        if first_scene_id in self.scenes:
            self.current_scene = self.scenes[first_scene_id]

        self.state = GameState.PLAYING

    def _generate_default_world(self) -> Dict:
        """Generate a default fantasy world"""
        return {
            "name": "神秘王国",
            "description": "一个充满魔法和冒险的奇幻世界",
            "start_scene": "forest_entrance",
            "scenes": {
                "forest_entrance": {
                    "id": "forest_entrance",
                    "name": "森林入口",
                    "description": "你站在一片神秘森林的入口。古树参天，阳光透过树叶洒下斑驳的光影。远处的树林中传来奇怪的声音。",
                    "options": [
                        {"text": "走进森林深处", "action": "move", "target": "deep_forest"},
                        {"text": "寻找其他路径", "action": "move", "target": "path"},
                        {"text": "检查周围环境", "action": "search"},
                        {"text": "查看背包", "action": "inventory"}
                    ],
                    "items": ["地图"],
                    "npcs": []
                },
                "deep_forest": {
                    "id": "deep_forest",
                    "name": "森林深处",
                    "description": "你深入森林，周围的光线变暗。突然，你听到前方有动静！",
                    "options": [
                        {"text": "悄悄接近", "action": "sneak"},
                        {"text": "大声喝问", "action": "shout"},
                        {"text": "转身逃跑", "action": "flee"},
                        {"text": "拔出武器", "action": "fight"}
                    ],
                    "items": [],
                    "npcs": ["哥布林"]
                },
                "path": {
                    "id": "path",
                    "name": "小路",
                    "description": "你发现了一条隐蔽的小路，通向远处的一座小山。路上似乎有人走过的痕迹。",
                    "options": [
                        {"text": "沿着小路前进", "action": "move", "target": "hill"},
                        {"text": "返回森林入口", "action": "move", "target": "forest_entrance"},
                        {"text": "检查痕迹", "action": "search"}
                    ],
                    "items": [],
                    "npcs": []
                },
                "victory": {
                    "id": "victory",
                    "name": "胜利",
                    "description": "恭喜！你完成了冒险！",
                    "options": [
                        {"text": "再玩一次", "action": "restart"},
                        {"text": "退出游戏", "action": "quit"}
                    ],
                    "items": [],
                    "npcs": []
                }
            }
        }

    def process_action(self, action: str) -> Tuple[str, Optional[Scene]]:
        """Process player action and return result"""
        if not self.current_scene:
            return "游戏未初始化", None

        # Find the option matching the action
        option = None
        for opt in self.current_scene.options:
            if action.lower() in opt["text"].lower() or action == str(self.current_scene.options.index(opt) + 1):
                option = opt
                break

        if not option:
            return "无效的选择，请重试", self.current_scene

        # Record action
        self._record_action(action, option)

        # Process the action
        action_type = option.get("action", "")

        if action_type == "move":
            target = option.get("target")
            if target and target in self.scenes:
                self.current_scene = self.scenes[target]
                self.current_scene.visited = True
                return self._get_scene_description(), self.current_scene
            return "无法前往该方向", self.current_scene

        elif action_type == "search":
            items_found = self._search_area()
            if items_found:
                self.player.inventory.extend(items_found)
                return f"你发现了: {', '.join(items_found)}", self.current_scene
            return "什么都没发现", self.current_scene

        elif action_type == "inventory":
            return f"背包: {', '.join(self.player.inventory) if self.player.inventory else '空'}", self.current_scene

        elif action_type == "quit":
            self.state = GameState.QUIT
            return "游戏结束", None

        elif action_type == "restart":
            self.__init__(self.player.name)
            self.initialize_world()
            return "游戏重新开始！", self.current_scene

        else:
            return f"执行了: {option['text']}", self.current_scene

    def _get_scene_description(self) -> str:
        """Get current scene description with dynamic elements"""
        if not self.current_scene:
            return ""

        desc = self.current_scene.description

        # Add items
        if self.current_scene.items:
            desc += f"\n\n物品: {', '.join(self.current_scene.items)}"

        # Add NPCs
        if self.current_scene.npcs:
            desc += f"\n\nNPC: {', '.join(self.current_scene.npcs)}"

        # Add options
        desc += "\n\n选项:"
        for i, opt in enumerate(self.current_scene.options, 1):
            desc += f"\n{i}. {opt['text']}"

        return desc

    def _search_area(self) -> List[str]:
        """Search current area for items"""
        if self.current_scene and self.current_scene.items:
            items = self.current_scene.items.copy()
            self.current_scene.items = []
            return items
        return []

    def _record_action(self, action: str, option: Dict):
        """Record action to history"""
        self.history.append({
            "time": datetime.now().isoformat(),
            "scene": self.current_scene.id if self.current_scene else None,
            "action": action,
            "option": option
        })

    def get_status(self) -> Dict:
        """Get current game status"""
        return {
            "state": self.state.value,
            "player": asdict(self.player),
            "current_scene": self.current_scene.id if self.current_scene else None,
            "history_length": len(self.history)
        }

    def save_game(self, filename: str = None) -> str:
        """Save game state to file"""
        if filename is None:
            filename = f"/tmp/game_save_{self.game_id}.json"

        save_data = {
            "game_id": self.game_id,
            "player": asdict(self.player),
            "state": self.state.value,
            "current_scene": self.current_scene.id if self.current_scene else None,
            "scenes_visited": [s.id for s in self.scenes.values() if s.visited],
            "history": self.history[-20:]  # Last 20 actions
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)

        return filename

    def load_game(self, filename: str):
        """Load game state from file"""
        with open(filename, 'r', encoding='utf-8') as f:
            save_data = json.load(f)

        self.player = Player(**save_data["player"])
        self.state = GameState(save_data["state"])
        self.game_id = save_data["game_id"]
        self.history = save_data.get("history", [])

        if save_data.get("current_scene"):
            self.current_scene = self.scenes.get(save_data["current_scene"])

    def get_story_summary(self) -> str:
        """Generate a story summary from history"""
        if not self.history:
            return "故事尚未开始"

        summary = f"## {self.player.name}的冒险故事\n\n"

        for record in self.history:
            scene = record.get("scene", "unknown")
            action = record.get("action", "unknown")
            summary += f"- 在{scene}执行了: {action}\n"

        summary += f"\n总行动数: {len(self.history)}"
        return summary
