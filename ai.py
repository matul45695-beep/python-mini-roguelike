"""モンスターの行動AIや経路探索を管理するモジュール"""

from config import GOBLIN_CHACE_RANGE


def manhattan_distance(pos1, pos2):
    """マンハッタン距離を計算する関数"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def can_detect_player(monster_pos, player_pos):
    """ゴブリンがプレイヤーを感知できるか判定する関数"""
    return manhattan_distance(monster_pos, player_pos) <= GOBLIN_CHACE_RANGE

def chase_move(options, player_pos):
    """ゴブリンがプレイヤーに最も近づける移動先を取得するための関数"""
 
    return min(options, key=lambda pos: manhattan_distance(pos, player_pos))