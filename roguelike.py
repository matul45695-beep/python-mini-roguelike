"""ミニローグ：ターン制のダンジョン探索と戦闘。標準ライブラリのみ。"""
import random

DIRECTIONS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}

MAX_STAGE = 3

# モンスターの種類とステータス
MONSTER_TYPES = {
    "スライム": {"symbol": "S", "hp": 3, "attack": 1},
    "ゴブリン": {"symbol": "G", "hp": 5, "attack": 2},
    "オーク": {"symbol": "O", "hp": 8, "attack": 3}
}

def generate_map():
    """マップの自動生成"""

    # マップサイズの設定
    width, height = 21, 15

    map_data = []

    for y in range(height):
        row = ["#" for _ in range(width)]
        map_data.append(row)

    # ランダムなスタート位置の設定（奇数座標）
    start_x, start_y = random.randrange(1, width-1, 2), random.randrange(1, height-1, 2)
    
    # 開始位置を床に設定 
    map_data[start_y][start_x] = "."

    stack = [(start_x, start_y)]

    dig_directions = [
        (0, -2),  # 上
        (0,  2),  # 下
        (-2, 0),  # 左
        ( 2, 0)   # 右
    ]

    while stack:
        x, y = stack[-1]

        candidates = []

        for dx, dy in dig_directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width-1 and 0 < ny < height-1:
                if map_data[ny][nx] == "#":
                    candidates.append((nx, ny))

        if candidates:
            nx, ny = random.choice(candidates)

            mx, my = (x + nx) // 2, (y + ny) // 2

            map_data[ny][nx] = "."
            map_data[my][mx] = "."

            stack.append((nx, ny))

        else:
            stack.pop()

    return map_data

def new_game():
    # マップの解析
    map_data = generate_map()

    height = len(map_data)
    width = len(map_data[0])

    walls, floors = set(), set()
    player = None
    exit_pos = None

    for y, row in enumerate(map_data):
        for x, ch in enumerate(row):
            if ch == "#":
                walls.add((x, y))
            else:
                floors.add((x, y))

    player = random.choice(list(floors))
    exit_pos = random.choice(list(floors - {player}))
    candidates = sorted(floors - {player, exit_pos})
# モンスターの配置
    monsters = {}

    for pos in random.sample(candidates, 5):
        name = random.choice(list(MONSTER_TYPES))
        monsters[pos] = {
            "name": name,
            "symbol": MONSTER_TYPES[name]["symbol"],
            "hp": MONSTER_TYPES[name]["hp"],
            "attack": MONSTER_TYPES[name]["attack"]
        }
        
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
            "message": "出口 > を目指そう。敵は S/G/O、回復薬は !"
        }


def draw_game(game):
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
                line += game["monsters"][pos]["symbol"]

            # アイテムの描画
            elif pos in game["items"]:
                line += "!"

            elif pos == game["exit"]:
                line += ">"

            else:
                line += "#" if pos in game["walls"] else " "
        print(line)
    print(f"HP {game['hp']}/{game['max_hp']}  ターン {game['turn']} | {game['message']}")
    print("WASD: 移動と攻撃 / .: 待機 / Q: 終了")


def adjacent(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1


def player_turn(game, key):
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
        enemy["hp"] -= 3
        game["message"] = "モンスターを攻撃！ 3ダメージ。"
        
        if enemy["hp"] <= 0:
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
    # 敵は隣にいれば攻撃、それ以外はランダムに一歩動く
    moved = {}
    occupied = set(game["monsters"])
    total_damage = 0

    for pos, enemy in list(game["monsters"].items()):
        if adjacent(pos, game["player"]):
            total_damage += enemy["attack"]
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
    game = new_game()

    while game["hp"] > 0:
        draw_game(game)

        if game["player"] == game["exit"]:

            if game["stage"] >= MAX_STAGE:
                print(f"ステージ {game['stage']} をクリア！")
                print("ゲームクリア！")
                return

            current_hp = game["hp"]
            current_max_hp = game["max_hp"]
            current_turn = game["turn"]
            next_stage = game["stage"] + 1

            print(f"ステージ {game['stage']} をクリア！")

            game = new_game()
            game["hp"] = current_hp
            game["max_hp"] = current_max_hp
            game["turn"] = current_turn
            game["stage"] = next_stage

            continue
        
        key = input("操作 > ").strip().lower()[:1]

        if key == "q":
            return
        
        if player_turn(game, key):
            game["turn"] += 1
            if game["player"] != game["exit"]:
                monster_turn(game)
    draw_game(game)

    print("ゲームオーバー！")


if __name__ == "__main__":
    main()
