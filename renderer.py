"""ゲーム画面の描画や表示を管理するモジュール"""

from config import RESET, CYAN, YELLOW, BLUE, GRAY

def draw_game(game):
    # 既存の描写処理
    print("\n" * 2 + f"=== MINI ROGUELIKE : Stage {game['stage']} ===")

    height, width = game["height"], game["width"]

    for y in range(height):
        line = ""
        for x in range(width):
            pos = (x, y)

            # プレイヤーの描画
            if pos == game["player"]:
                line += CYAN + "@" + RESET

            # モンスターの描画
            elif pos in game["monsters"]:
                enemy = game["monsters"][pos]
                line += enemy.color + enemy.symbol + RESET

            # アイテムの描画
            elif pos in game["items"]:
                line += YELLOW + "!" + RESET

            # 出口の描画
            elif pos == game["exit"]:
                line += BLUE + ">" + RESET

            # 壁と床の描画
            else:
                line += GRAY + "#" + RESET if pos in game["walls"] else " "

        print(line)
    print(f"HP {game['hp']}/{game['max_hp']}  累計ターン {game['turn']}  滞在ターン {game['stage_turn']}")
    print(game['message'])
    print("WASD: 移動と攻撃 / .: 待機 / Q: 終了")