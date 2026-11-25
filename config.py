"""ゲームの定数やモンスターの設定データを管理する"""

DIRECTIONS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}

MAX_STAGE = 3
REAPER_SPQWN_TURN = 100

# モンスターの種類とステータス
MONSTER_TYPES = {
    "スライム": {"symbol": "S", "hp": 3, "attack": 1, "ai": "random", "invincible": False, "normal_spawn": True},
    "ゴブリン": {"symbol": "G", "hp": 5, "attack": 2, "ai": "chase", "invincible": False, "normal_spawn": True},
    "オーク": {"symbol": "O", "hp": 8, "attack": 3, "ai": "bfs", "invincible": False, "normal_spawn": True},
    "死神": {"symbol": "R", "hp": 999, "attack": 999, "ai": "bfs", "invincible": True, "normal_spawn": False}
}
