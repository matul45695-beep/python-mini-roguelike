"""モンスターのステータスや行動を管理する"""

from config import MONSTER_TYPES

class Monster:
    """モンスターのステータスや行動を管理するクラス"""

    def __init__(self, name):
        """モンスターの初期化"""

        data = MONSTER_TYPES[name]

        self.name = name
        self.symbol = data["symbol"]
        self.color = data["color"]
        self.hp = data["hp"]
        self.attack = data["attack"]
        self.ai = data["ai"]
        self.invincible = data["invincible"]


    def take_damage(self, damage):
        """無敵判定を行い、ダメージを受ける"""

        if not self.invincible:
            self.hp -= damage


    def is_alive(self):
        """モンスターが生存しているかを判定する"""

        return self.hp > 0

