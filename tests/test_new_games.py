"""テトリス・四目並べ・シューティングの基本ロジックを検査。"""
import sys
from pathlib import Path
import random
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from connect_four import ConnectFour
from tetris import Tetris, COLS, ROWS
from shooting import ShootingGame, Enemy, HeavyEnemy, Bullet, HEIGHT, WIDTH


class ConnectFourTests(unittest.TestCase):
    def test_gravity_and_turns(self):
        g = ConnectFour()
        self.assertEqual(g.drop_piece(0), (0, 5))
        self.assertEqual(g.drop_piece(0), (0, 4))
        self.assertEqual(g.board[5][0], 'O')
        self.assertEqual(g.board[4][0], 'X')

    def test_vertical_win(self):
        g = ConnectFour()
        for col in [0, 1, 0, 1, 0, 1, 0]:
            g.drop_piece(col)
        self.assertEqual(g.winner, 'O')
        self.assertIsNone(g.drop_piece(2))

    def test_horizontal_win(self):
        g = ConnectFour()
        for col in [0, 0, 1, 1, 2, 2, 3]:
            g.drop_piece(col)
        self.assertEqual(g.winner, 'O')

    def test_diagonal_win(self):
        g = ConnectFour()
        # Oの右上がり斜め4連、Xが下から支える
        for col in [0, 1, 1, 2, 4, 2, 2, 3, 4, 3, 5, 3, 3]:
            g.drop_piece(col)
        self.assertEqual(g.winner, 'O')

    def test_full_column(self):
        g = ConnectFour()
        for _ in range(6):
            g.drop_piece(0)
        self.assertNotIn(0, g.legal_columns())
        self.assertIsNone(g.drop_piece(0))


class TetrisTests(unittest.TestCase):
    def test_starts_and_moves(self):
        g = Tetris(random.Random(0))
        self.assertFalse(g.game_over)
        self.assertTrue(g.move(0, 1))
        self.assertEqual(g.y, 1)

    def test_lines_clear(self):
        g = Tetris(random.Random(0))
        g.board[-1] = ['I'] * COLS
        g.board[-2][0] = 'T'
        self.assertEqual(g.clear_lines(), 1)
        self.assertEqual(g.lines, 1)
        self.assertEqual(g.score, 100)
        self.assertEqual(g.board[-1][0], 'T')

    def test_hard_drop_locks(self):
        g = Tetris(random.Random(0))
        g.hard_drop()
        self.assertTrue(any(v != ' ' for row in g.board for v in row))

    def test_game_over_on_blocked_spawn(self):
        g = Tetris(random.Random(0))
        g.board[0] = ['X'] * COLS
        g.board[1] = ['X'] * COLS
        g.spawn()
        self.assertTrue(g.game_over)

    def test_rotation_near_boundary(self):
        g = Tetris(random.Random(0))
        g.kind = 'I'
        g.cells = [(0, 1), (1, 1), (2, 1), (3, 1)]
        self.assertTrue(g.rotate())
        self.assertTrue(g.can_place(g.cells, g.x, g.y))


class ShootingTests(unittest.TestCase):
    def test_player_boundary(self):
        g = ShootingGame(random.Random(0))
        g.player.move(-100)
        self.assertEqual(g.player.x, 0)
        g.player.move(100)
        self.assertEqual(g.player.x, WIDTH - 1)

    def test_fire_cooldown(self):
        g = ShootingGame(random.Random(0))
        self.assertTrue(g.fire())
        self.assertFalse(g.fire())
        self.assertEqual(len(g.bullets), 1)

    def test_enemy_hit(self):
        g = ShootingGame(random.Random(0))
        g.enemies.append(Enemy(10, 5))
        g.bullets.append(Bullet(10, 6))
        g.update()
        self.assertFalse(g.enemies)
        self.assertEqual(g.score, 10)

    def test_heavy_enemy_three_hits(self):
        e = HeavyEnemy(5)
        self.assertFalse(e.take_hit())
        self.assertFalse(e.take_hit())
        self.assertTrue(e.take_hit())

    def test_lose_lives(self):
        g = ShootingGame(random.Random(0))
        g.enemies.extend(Enemy(i, HEIGHT - 1) for i in range(3))
        g.update()
        self.assertTrue(g.game_over)
        self.assertEqual(g.player.lives, 0)


if __name__ == '__main__':
    unittest.main()
