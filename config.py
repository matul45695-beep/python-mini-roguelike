"""ゲームの定数やモンスターの設定データを管理する"""

# ゲームの移動方向を表す辞書
DIRECTIONS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}

# ゲームの最大ステージ数
MAX_STAGE = 3
# 死神が出現するターン数
REAPER_SPAWN_TURN = 100

# モンスターの種類とステータス
MONSTER_TYPES = {
    "スライム": {"symbol": "S", "hp": 3, "attack": 1, "ai": "random", "invincible": False, "normal_spawn": True},
    "ゴブリン": {"symbol": "G", "hp": 5, "attack": 2, "ai": "chase", "invincible": False, "normal_spawn": True},
    "オーク": {"symbol": "O", "hp": 8, "attack": 3, "ai": "bfs", "invincible": False, "normal_spawn": True},
    "死神": {"symbol": "R", "hp": 999, "attack": 999, "ai": "bfs", "invincible": True, "normal_spawn": False}
}
