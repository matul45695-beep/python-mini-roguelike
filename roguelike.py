"""ミニローグ：ターン制のダンジョン探索と戦闘。標準ライブラリのみ。"""
import random

MAP = [
    "#####################",
    "#@....#.............#",
    "#.....#...##........#",
    "#........##..#.......#",
    "#..###.......#.......#",
    "#......#.........#...#",
    "#......#...###...#...#",
    "#............#.......#",
    "#..##........#...#...#",
    "#......#.........#...#",
    "#...................>#",
    "#####################",
]
DIRECTIONS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}


def new_game():
    walls, floors = set(), set()
    player = None
    exit_pos = None
    for y, row in enumerate(MAP):
        for x, ch in enumerate(row):
            if ch == "#":
                walls.add((x, y))
            else:
                floors.add((x, y))
            if ch == "@":
                player = (x, y)
            if ch == ">":
                exit_pos = (x, y)
    candidates = sorted(floors - {player, exit_pos})
    monsters = {p: {"hp": 5} for p in random.sample(candidates, 3)}
    items = set(random.sample([p for p in candidates if p not in monsters], 4))
    return {"walls": walls, "floors": floors, "player": player, "exit": exit_pos,
            "monsters": monsters, "items": items, "hp": 18, "max_hp": 18,
            "turn": 0, "message": "出口 > を目指そう。敵は M、回復薬は !"}


def draw_game(game):
    print("\n" * 2 + "=== MINI ROGUELIKE ===")
    height = len(MAP)
    width = len(MAP[0])
    for y in range(height):
        line = ""
        for x in range(width):
            pos = (x, y)
            if pos == game["player"]:
                line += "@"
            elif pos in game["monsters"]:
                line += "M"
            elif pos in game["items"]:
                line += "!"
            elif pos == game["exit"]:
                line += ">"
            else:
                line += "#" if pos in game["walls"] else "."
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
    attacks = 0
    for pos, enemy in list(game["monsters"].items()):
        if adjacent(pos, game["player"]):
            attacks += 1
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
    if attacks:
        game["hp"] -= attacks * 2
        game["message"] += f" 敵から{attacks * 2}ダメージ！"


def main():
    game = new_game()
    while game["hp"] > 0:
        draw_game(game)
        if game["player"] == game["exit"]:
            print("ダンジョン脱出成功！")
            return
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
