"""ミニローグ：ターン制のダンジョン探索と戦闘。標準ライブラリのみ。"""
import random

from config import DIRECTIONS, MAX_STAGE, REAPER_SPAWN_TURN, MONSTER_TYPES
from monster import Monster

def generate_map():
    """深さ優先探索（DFS）を用いた穴掘り法を用いたマップの自動生成"""

    # 外周の壁を残しやすくするために、幅と高さは奇数に設定
    width, height = 21, 15

    #  全てのマスを壁 "#" で初期化
    map_data = []

    for y in range(height):
        row = ["#" for _ in range(width)]
        map_data.append(row)

    # ランダムなスタート位置の設定（奇数座標）
    start_x, start_y = random.randrange(1, width-1, 2), random.randrange(1, height-1, 2)
    
    # 開始位置を床に設定 
    map_data[start_y][start_x] = "."

    # バックトラック用の探索経路を記録するスタック
    stack = [(start_x, start_y)]

    # 上下左右の方向ベクトル（通路の間に壁を残す為に2マスずつ移動）
    dig_directions = [
        (0, -2),  # 上
        (0,  2),  # 下
        (-2, 0),  # 左
        ( 2, 0)   # 右
    ]

    # スタックが空になるまで穴掘り処理を繰り返す
    while stack:
        # スタックの末尾の要素（現在の探索地点の座標）を取得
        x, y = stack[-1]

        # 現在位置から掘ることができる座標を格納するリスト
        candidates = []

        for dx, dy in dig_directions:
            nx, ny = x + dx, y + dy

            # 外周の壁を除いた範囲内か確認
            if 0 < nx < width-1 and 0 < ny < height-1:
                # まだ探索していない壁だけを候補として追加
                if map_data[ny][nx] == "#":
                    candidates.append((nx, ny))

        if candidates:
            # 掘ることができる候補からランダムに選択
            nx, ny = random.choice(candidates)

            # 現在位置と移動先の中間地点を計算
            mx, my = (x + nx) // 2, (y + ny) // 2

            # 移動先と中間地点を床 "." に変更
            map_data[ny][nx] = "."
            map_data[my][mx] = "."

            # 移動先を次の探索地点として登録
            stack.append((nx, ny))

        else:
            # 行き止まりの場合はバックトラックする
            stack.pop()

    return map_data


def new_game():
    """ダンジョンを生成し、ゲームデータを初期化する"""

    # ランダムマップの作成
    map_data = generate_map()

    # 生成されたマップサイズを取得
    height = len(map_data)
    width = len(map_data[0])

    walls, floors = set(), set()

    for y, row in enumerate(map_data):
        for x, ch in enumerate(row):
            if ch == "#":
                walls.add((x, y))
            else:
                floors.add((x, y))

    # プレイヤーの初期位置をランダムに設定
    player = random.choice(list(floors))

    # プレイヤーと重複しない位置に出口を配置
    exit_pos = random.choice(list(floors - {player}))

    # プレイヤーと出口を除いた配置候補を取得
    candidates = sorted(floors - {player, exit_pos})

    # 通常出現するモンスターのみの抽出
    normal_monsters = [
         name for name, data in MONSTER_TYPES.items() 
        if data["normal_spawn"]
    ]

    # モンスターの種類の配置
    monsters = {}
        
    for pos in random.sample(candidates, 5):
        name = random.choice(normal_monsters)

        # モンスターのインスタンスを作成
        monsters[pos] = Monster(name)

    # アイテムの配置
    items = set(random.sample([p for p in candidates if p not in monsters], 4))

    return {"walls": walls, 
            "floors": floors,
            "height": height,
            "width": width,
            "player": player, 
            "exit": exit_pos,
            "monsters": monsters, 
            "items": items, 
            "hp": 18, 
            "max_hp": 18,
            "turn": 0, 
            "stage": 1,
            "stage_turn": 0,
            "message": "出口 > を目指そう。敵は S/G/O、回復薬は !"
        }


def draw_game(game):
    """現在のゲーム状態をターミナルへ描画する"""

    print("\n" * 2 + f"=== MINI ROGUELIKE : Stage {game['stage']} ===")

    height = game["height"]
    width = game["width"]

    for y in range(height):
        line = ""
        for x in range(width):
            pos = (x, y)
            if pos == game["player"]:
                line += "@"

            # モンスターの描画
            elif pos in game["monsters"]:
                line += game["monsters"][pos].symbol

            # アイテムの描画
            elif pos in game["items"]:
                line += "!"

            elif pos == game["exit"]:
                line += ">"

            else:
                line += "#" if pos in game["walls"] else " "
        print(line)
    print(f"HP {game['hp']}/{game['max_hp']}  累計ターン {game['turn']}  滞在ターン {game['stage_turn']}")
    print(game['message'])
    print("WASD: 移動と攻撃 / .: 待機 / Q: 終了")


def adjacent(a, b):
    # ２つの座標が上下左右に隣接しているか判定

    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1


def player_turn(game, key):
    """プレイヤーの移動・攻撃・アイテム取得を処理する"""

    if key == ".":
        game["message"] = "その場で待機した。"
        return True
    
    if key not in DIRECTIONS:
        return False
    
    dx, dy = DIRECTIONS[key]
    pos = game["player"]
    next_pos = (pos[0] + dx, pos[1] + dy)

    if next_pos in game["walls"] or next_pos not in game["floors"]:
        game["message"] = "壁にぶつかった。"
        return False
    
    if next_pos in game["monsters"]:
        enemy = game["monsters"][next_pos]

        enemy.take_damage(3)
        game["message"] = "モンスターを攻撃！ 3ダメージ。"
        
        if not enemy.is_alive():
            del game["monsters"][next_pos]
            game["message"] = "モンスターを倒した！"
    else:
        game["player"] = next_pos
        if next_pos in game["items"]:
            game["items"].remove(next_pos)
            heal = min(5, game["max_hp"] - game["hp"])
            game["hp"] += heal
            game["message"] = f"回復薬を飲んだ。HP +{heal}"
        else:
            game["message"] = "探索中..."
    return True


def monster_turn(game):
    """モンスターの移動と攻撃を処理"""

    # 敵は隣にいれば攻撃、それ以外はランダムに一歩動く
    moved = {}
    occupied = set(game["monsters"])
    total_damage = 0

    for pos, enemy in list(game["monsters"].items()):
        if adjacent(pos, game["player"]):
            total_damage += enemy.attack
            moved[pos] = enemy
            continue

        options = [pos]

        for dx, dy in DIRECTIONS.values():
            target = (pos[0] + dx, pos[1] + dy)
            if (target in game["floors"] and target not in occupied
                    and target != game["player"] and target != game["exit"]):
                options.append(target)
        next_pos = random.choice(options)
        moved[next_pos] = enemy
        occupied.discard(pos)
        occupied.add(next_pos)
    game["monsters"] = moved

    if total_damage:
        game["hp"] -= total_damage
        game["message"] += f" 敵から{total_damage}ダメージ！"


def main():
    """ゲームの進行とステージの切り替えを管理"""

    game = new_game()

    while game["hp"] > 0:
        draw_game(game)

        # プレイヤーが出口に到達したか判定
        if game["player"] == game["exit"]:

            # 最終ステージの場合はゲームを終了
            if game["stage"] >= MAX_STAGE:
                print(f"ステージ {game['stage']} をクリア！")
                print("ゲームクリア！")
                return

            # 新しいステージで初期化されるデータを一時保存
            current_hp = game["hp"]
            current_max_hp = game["max_hp"]
            current_turn = game["turn"]
            next_stage = game["stage"] + 1

            print(f"ステージ {game['stage']} をクリア！")

            # 次のステージのマップ・敵・アイテムを引き継ぐ
            game = new_game()
            game["hp"] = current_hp
            game["max_hp"] = current_max_hp
            game["turn"] = current_turn
            game["stage"] = next_stage

            # 次のステージを描画するためループの先頭へ戻る
            continue
        
        key = input("操作 > ").strip().lower()[:1]

        if key == "q":
            return
        
        if player_turn(game, key):
            game["turn"] += 1
            game["stage_turn"] += 1
            if game["player"] != game["exit"]:
                monster_turn(game)
    draw_game(game)

    print("ゲームオーバー！")


if __name__ == "__main__":
    main()
