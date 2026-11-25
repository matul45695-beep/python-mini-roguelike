"""ゲームの定数やモンスターの設定データを管理する"""

# ゲームの移動方向を表す辞書
DIRECTIONS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}

# ANSIカラーの定義
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
GRAY = "\033[90m"
ORANGE = "\033[38;5;208m"

# ゲームの最大ステージ数
MAX_STAGE = 3
# 死神が出現するターン数
REAPER_SPAWN_TURN = 100

# ゴブリンのプレイヤー感知範囲（マンハッタン距離）
GOBLIN_CHACE_RANGE = 5

# モンスターの種類とステータス
MONSTER_TYPES = {
    "スライム": {"symbol": "S","color": GREEN, "hp": 3, "attack": 1, "ai": "random", "invincible": False, "normal_spawn": True},
    "ゴブリン": {"symbol": "G", "color": ORANGE, "hp": 5, "attack": 2, "ai": "chase", "invincible": False, "normal_spawn": True},
    "オーク": {"symbol": "O", "color": RED, "hp": 8, "attack": 3, "ai": "bfs", "invincible": False, "normal_spawn": True},
    "死神": {"symbol": "R", "color": MAGENTA, "hp": 999, "attack": 999, "ai": "bfs", "invincible": True, "normal_spawn": False}
}
