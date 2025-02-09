import pyxel

# 画面サイズ
WIDTH = 128
HEIGHT = 128
CHAR_SIZE = 16  # キャラのサイズ

# キャラクターの初期位置
x = 56
y = 100
direction = 0  # 初期向きは下

# マップデータ（4x4）
# 15: 葉（進入不可）, 14-1: 水面（進入不可）, 0: 底（進入可能）
upper_layer = [
    [15, 14, 14, 14],
    [14, 15, 14, 14],
    [14, 14, 14, 15],
    [13, 15, 14, 13]
]
lotus_layer = [
    [0, 0, 0, 4],
    [0, 1, 0, 0],
    [3, 0, 2, 0],
    [0, 1, 0, 0]
]

# マップの左上の座標
map_x = 30
map_y = 20

def draw_upper_layer():
    """ 表層レイヤーを描画する関数 """
    for row in range(4):
        for col in range(4):
            pyxel.blt(map_x + col * CHAR_SIZE, map_y + row * CHAR_SIZE, 1, 0 + 16 * (15-upper_layer[row][col]), 0, 16, 16, 0)

def draw_lotus_layer():
    """ 蓮根レイヤーを描画する関数 """
    for row in range(4):
        for col in range(4):
            if lotus_layer[row][col] == 0:
                pyxel.blt(map_x + col * CHAR_SIZE, map_y + row * CHAR_SIZE, 1, 0, 112, 16, 16, 0)
            else:
                pyxel.blt(map_x + col * CHAR_SIZE, map_y + row * CHAR_SIZE, 1, 16 * (lotus_layer[row][col]-1), 16, 16, 16, 12)

def is_wall(px, py):
    """指定座標(px, py) が壁かどうかを判定"""
    col = (px - map_x) // CHAR_SIZE
    row = (py - map_y) // CHAR_SIZE

    if 0 <= row < 4 and 0 <= col < 4:
        return upper_layer[row][col] != 0  # 0（底）以外なら True（通れない）
    return False  # マップ範囲外なら False（通れる）

def can_move(new_x, new_y):
    """キャラクターの4点（左上・右上・左下・右下）で移動可能か判定"""
    return not (
        is_wall(new_x + 1, new_y + 1) or  # 左上
        is_wall(new_x + CHAR_SIZE - 2, new_y + 1) or  # 右上
        is_wall(new_x + 1, new_y + CHAR_SIZE - 2) or  # 左下
        is_wall(new_x + CHAR_SIZE - 2, new_y + CHAR_SIZE - 2)  # 右下
    )

def dig_block(px, py, direction):
    if direction == 0: # 上向き
        new_x = px + CHAR_SIZE - 5
        new_y = py
    elif direction == 1: # 右向き
        new_x = px + CHAR_SIZE - 1
        new_y = py + CHAR_SIZE - 4
    elif direction == 2: # 下向き
        new_x = px + 4
        new_y = py + CHAR_SIZE - 1
    elif direction == 3: # 左向き
        new_x = px
        new_y = py + CHAR_SIZE - 4
    
    if is_wall(new_x, new_y) or is_wall(new_x + CHAR_SIZE - 1, new_y) or is_wall(new_x, new_y + CHAR_SIZE - 1) or is_wall(new_x + CHAR_SIZE - 1, new_y + CHAR_SIZE - 1):
        col = (new_x - map_x) // CHAR_SIZE
        row = (new_y - map_y) // CHAR_SIZE
        if 0 <= row < 4 and 0 <= col < 4 and upper_layer[row][col] > 0:
            upper_layer[row][col] -= 1

def is_lotus(px, py):
    """指定座標(px, py) が蓮根があるか判定"""
    col = (px - map_x) // CHAR_SIZE
    row = (py - map_y) // CHAR_SIZE

    if 0 <= row < 4 and 0 <= col < 4:
        return lotus_layer[row][col]
    return 0

def can_get(new_x, new_y):
    if is_lotus(new_x, new_y) == 0:
        return False
    else:
        return True

def get_lotus(px, py, direction):
    if direction == 0: # 上向き
        new_x = px + CHAR_SIZE - 5
        new_y = py
    elif direction == 1: # 右向き
        new_x = px + CHAR_SIZE - 1
        new_y = py + CHAR_SIZE - 4
    elif direction == 2: # 下向き
        new_x = px + 4
        new_y = py + CHAR_SIZE - 1
    elif direction == 3: # 左向き
        new_x = px
        new_y = py + CHAR_SIZE - 4
    if is_lotus(new_x, new_y) or is_lotus(new_x + CHAR_SIZE - 1, new_y) or is_lotus(new_x, new_y + CHAR_SIZE - 1) or is_lotus(new_x + CHAR_SIZE - 1, new_y + CHAR_SIZE - 1):
        col = (new_x - map_x) // CHAR_SIZE
        row = (new_y - map_y) // CHAR_SIZE
        if 0 <= row < 4 and 0 <= col < 4 and lotus_layer[row][col] > 0:
            lotus_layer[row][col] = 0
    
def update():
    global x, y, direction

    # キャラクター移動処理
    new_x, new_y = x, y  # 仮の移動位置

    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
        new_y -= 1
        direction = 0  # 上向き
        # dig_block(new_x, new_y, direction)
    elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
        new_y += 1
        direction = 2  # 下向き
        # dig_block(new_x, new_y, direction)
    elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
        new_x -= 1
        direction = 3  # 左向き
        # dig_block(new_x, new_y, direction)
    elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
        new_x += 1
        direction = 1  # 右向き
        # dig_block(new_x, new_y, direction)

    # ブロック通過チェック
    if can_move(new_x, new_y): 
        x = max(0, min(new_x, WIDTH - CHAR_SIZE))
        y = max(0, min(new_y, HEIGHT - CHAR_SIZE))

    # 水掛け判定
    if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
        dig_block(x, y, direction)

    # 収穫判定
    if pyxel.btn(pyxel.KEY_B) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
        get_lotus(x, y, direction)


def draw():
    pyxel.cls(12)  # 画面をクリア（背景色）
    draw_lotus_layer()
    draw_upper_layer()

    # キャラクターを描画
    if direction == 0:
        pyxel.blt(x, y, 0, 48, 16, 16, 16, 7)  # 上向き
    elif direction == 1:
        pyxel.blt(x, y, 0, 16, 16, 16, 16, 7)  # 右向き
    elif direction == 2:
        pyxel.blt(x, y, 0, 0, 16, 16, 16, 7)  # 下向き
    elif direction == 3:
        pyxel.blt(x, y, 0, 32, 16, 16, 16, 7)  # 左向き

pyxel.init(WIDTH, HEIGHT)  # 画面サイズ128x128
pyxel.load("assets.pyxres")  # スプライトシートをロード
pyxel.run(update, draw)  # ゲームループを開始
