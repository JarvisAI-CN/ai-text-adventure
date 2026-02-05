"""
AI Dungeon Master - Dynamic story generation
Uses AI to create immersive game scenarios
"""

import random
from typing import Dict, List, Optional
from engine import Scene, GameEngine


class AIDungeonMaster:
    """AI-powered game master for dynamic storytelling"""

    def __init__(self):
        self.personalities = ["epic", "mysterious", "humorous", "dark"]
        self.current_personality = random.choice(self.personalities)
        self.story_elements = self._load_story_elements()

    def _load_story_elements(self) -> Dict:
        """Load story elements for dynamic generation"""
        return {
            "locations": {
                "forest": ["ancient trees", "mystical fog", "hidden paths", "wild creatures"],
                "castle": ["stone walls", "towering spires", "dark dungeons", "royal guards"],
                "village": ["thatched cottages", "busy market", "friendly villagers", "mysterious stranger"],
                "cave": ["glowing crystals", "underground lake", "ancient drawings", "echoing sounds"]
            },
            "creatures": {
                "friendly": ["wise owl", "helpful fairy", "talking tree", "magical creature"],
                "neutral": ["wandering merchant", "lost traveler", "mysterious hermit"],
                "hostile": ["fierce goblin", "ancient dragon", "dark sorcerer", "wild beast"]
            },
            "items": {
                "treasure": ["golden coin", "ancient artifact", "magic ring", "precious gem"],
                "utility": ["old map", "rusty key", "healing potion", "mysterious note"],
                "weapon": ["sharp sword", "magic staff", "ancient bow", "protective shield"]
            },
            "events": {
                "discovery": ["You discover a hidden passage", "You find an ancient artifact", "You uncover a secret"],
                "danger": ["A creature attacks!", "A trap triggers!", "The ground shakes!"],
                "mystery": ["You hear strange sounds", "You see a shadow move", "You feel watched"]
            }
        }

    def describe_scene(self, scene: Scene, context: Dict = None) -> str:
        """Generate an engaging scene description"""
        if not context:
            context = {}

        # Base description
        description = scene.description

        # Add personality flavor
        if self.current_personality == "epic":
            description = self._make_epic(description)
        elif self.current_personality == "mysterious":
            description = self._make_mysterious(description)
        elif self.current_personality == "humorous":
            description = self._make_humorous(description)
        elif self.current_personality == "dark":
            description = self._make_dark(description)

        # Add dynamic elements
        description += self._add_dynamic_elements(scene, context)

        return description

    def _make_epic(self, text: str) -> str:
        """Add epic flourishes"""
        epic_words = ["legendary", "mighty", "ancient", "glorious", "heroic"]
        return f"⚔️ {text}"

    def _make_mysterious(self, text: str) -> str:
        """Add mystery and suspense"""
        return f"🌙 {text} 奇异的能量在空气中流动..."

    def _make_humorous(self, text: str) -> str:
        """Add humor"""
        return f"😄 {text} (希望别踩到香蕉皮)"

    def _make_dark(self, text: str) -> str:
        """Add dark atmosphere"""
        return f"🌑 {text} 黑暗在注视着你..."

    def _add_dynamic_elements(self, scene: Scene, context: Dict) -> str:
        """Add dynamic elements based on context"""
        additions = []

        # Time of day
        time_of_day = context.get("time_of_day", "day")
        if time_of_day == "night":
            additions.append("月光透过树叶，投下诡异的影子。")
        elif time_of_day == "dawn":
            additions.append("黎明时分，第一缕阳光穿透迷雾。")

        # Weather
        weather = context.get("weather", "clear")
        if weather == "rain":
            additions.append("雨水打在树叶上，发出沙沙声。")
        elif weather == "fog":
            additions.append("浓雾笼罩，视线模糊。")

        # Player state
        player_health = context.get("player_health", 100)
        if player_health < 30:
            additions.append("你感到虚弱，需要休息。")

        return "\n" + " ".join(additions) if additions else ""

    def generate_options(self, scene: Scene, player_state: Dict = None) -> List[Dict[str, str]]:
        """Generate contextual options for the player"""
        if not player_state:
            player_state = {}

        options = []

        # Standard movement options
        for opt in scene.options[:2]:  # First 2 are usually movement
            options.append(opt)

        # Contextual options based on scene content
        if scene.items:
            options.append({
                "text": f"拾取物品",
                "action": "take_item"
            })

        if scene.npcs:
            options.append({
                "text": f"与{scene.npcs[0]}交谈",
                "action": "talk",
                "target": scene.npcs[0]
            })

        # Combat options if hostile NPCs
        hostile = any(npc in ["哥布林", "龙", "怪物", "敌人"] for npc in scene.npcs)
        if hostile:
            options.append({
                "text": "准备战斗",
                "action": "fight"
            })
            options.append({
                "text": "尝试逃跑",
                "action": "flee"
            })

        # System options
        options.append({
            "text": "查看状态",
            "action": "status"
        })

        return options

    def resolve_action(self, action: str, scene: Scene) -> str:
        """Resolve player action with narrative flair"""
        responses = {
            "fight": [
                "你拔出武器，准备战斗！",
                "战斗开始！你集中精神...",
                "你勇敢地面对敌人！"
            ],
            "flee": [
                "你转身逃跑！",
                "战术撤退！",
                "跑为上策！"
            ],
            "search": [
                "你仔细搜索周围...",
                "你仔细观察...",
                "你开始搜寻..."
            ]
        }

        action_responses = responses.get(action, ["你执行了操作。"])
        return random.choice(action_responses)

    def create_random_scene(self, scene_id: str, location_type: str = "forest") -> Scene:
        """Generate a random scene based on location type"""
        elements = self.story_elements

        # Get location elements
        loc_features = elements["locations"].get(location_type, elements["locations"]["forest"])

        # Create scene
        scene = Scene(
            id=scene_id,
            name=f"随机{location_type}",
            description=f"你来到一个地方，{' '.join(random.sample(loc_features, 2))}。",
            options=[
                {"text": "继续前进", "action": "move", "target": "next"},
                {"text": "仔细观察", "action": "search"},
                {"text": "休息", "action": "rest"}
            ]
        )

        # Add random items
        if random.random() > 0.5:
            all_items = elements["items"]["treasure"] + elements["items"]["utility"]
            scene.items = [random.choice(all_items)]

        # Add random NPC
        if random.random() > 0.6:
            all_creatures = elements["creatures"]["friendly"] + elements["creatures"]["hostile"]
            scene.npcs = [random.choice(all_creatures)]

        return scene

    def introduce_game(self) -> str:
        """Generate game introduction"""
        intros = [
            "欢迎来到AI文字冒险！一个由AI创造的无尽冒险世界。",
            " embark on an epic journey through the AI Text Adventure!",
            "你的冒险即将开始..."
        ]
        return f"{intros[0]}\n\n你的AI地下城主已准备就绪 (风格: {self.current_personality})"

    def congratulate_victory(self, player_name: str) -> str:
        """Generate victory message"""
        return f"""
╔═══════════════════════════════════════╗
║           🎉 胜利！🎉                 ║
║                                       ║
║  {player_name}完成了冒险！            ║
║                                       ║
║  感谢游玩AI文字冒险！                 ║
╚═══════════════════════════════════════╝
"""

    def generate_encounter(self, difficulty: int = 1) -> Dict:
        """Generate a random encounter"""
        creatures = {
            1: ["小史莱姆", "野鼠", "迷路的旅人"],
            2: ["哥布林", "狼", "强盗"],
            3: ["兽人", "巨蜘蛛", "黑暗骑士"],
            4: ["幼龙", "恶魔", "古老巫妖"]
        }

        creature = random.choice(creatures.get(min(difficulty, 4), creatures[4]))

        return {
            "creature": creature,
            "health": difficulty * 20,
            "attack": difficulty * 5,
            "description": f"一只{creature}出现了！"
        }


class StoryTeller:
    """Helper class for narrative elements"""

    @staticmethod
    def format_dialogue(text: str, speaker: str = "") -> str:
        """Format dialogue"""
        if speaker:
            return f'"{text}" — {speaker}'
        return f'"{text}"'

    @staticmethod
    def format_action(text: str) -> str:
        """Format action description"""
        return f"*{text}*"

    @staticmethod
    def add_drama(text: str, level: int = 1) -> str:
        """Add dramatic emphasis"""
        if level == 1:
            return f"✨ {text}"
        elif level == 2:
            return f"⚡ {text} ⚡"
        else:
            return f"🔥 {text} 🔥"
