"""モンスターの行動AIや経路探索を管理するモジュール"""
from collections import deque

from config import GOBLIN_CHASE_RANGE, DIRECTIONS


def manhattan_distance(pos1, pos2):
    """マンハッタン距離を計算する関数"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def can_detect_player(monster_pos, player_pos):
    """ゴブリンがプレイヤーを感知できるか判定する関数"""
    return manhattan_distance(monster_pos, player_pos) <= GOBLIN_CHASE_RANGE


def chase_move(options, player_pos):
    """ゴブリンがプレイヤーに最も近づける移動先を取得するための関数"""
 
    return min(options, key=lambda pos: manhattan_distance(pos, player_pos))


def bfs_move(start, goal, floors, blocked):
    """BFSを用いて最短経路上の次の移動先を探索する関数"""

    # 探索用のキューを初期化
    queue = deque()
    queue.append((start, []))

    # 探索済みの座標を管理する集合を初期化
    visited = set()
    visited.add(start)

    while queue:
        current, path = queue.popleft()

        # ゴールに到達した場合、次の移動先を返す
        if current == goal:
            return path[0] if path else current


        # 隣接する座標を探索
        for dx, dy in DIRECTIONS.values():
            next_pos = (current[0] + dx, current[1] + dy)

            # 床であり、ブロックされていない場合に探索を続ける
            if next_pos in floors and next_pos not in blocked and next_pos not in visited:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))

    return start


