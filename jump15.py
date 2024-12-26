import pyxel
import math
import random

class AngleJumpGame:
    def __init__(self):
        pyxel.init(160, 240)  # captionを削除
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """ゲームの状態をリセット"""
        self.platforms = []
        self.platform_interval = 50  # 足場生成間隔
        self.last_platform_y = 200  # 最初の足場のY座標
        self.scroll_offset = 0
    
        # 足場を初期生成
        current_y = self.last_platform_y
        while current_y > -pyxel.height:
            x = random.randint(10, 140)
            self.platforms.append([x, current_y])
            self.last_platform_y = current_y
            current_y -= self.platform_interval
        self.player_x = self.platforms[0][0] + 8  # 足場のX座標の中央にプレイヤーを配置
        self.player_y = self.platforms[0][1] - 8  # 足場の上にプレイヤーを配置
        self.player_vx = 0  # プレイヤーのX方向速度
        self.player_vy = 0  # プレイヤーのY方向速度
        self.on_platform = True  # プレイヤーが足場にいるかどうか
        self.angle_mode = False  # 角度指定モード
        self.angle_set = False  # 角度が決まったかどうか
        self.jump_angle = 0  # ジャンプの角度（ラジアン）
        self.angle_direction = 1  # 角度の方向（1:増加, -1:減少）
        self.jump_strength = 0  # ジャンプの強さ
        self.strength_mode = False  # 強さ指定モード
        self.strength_set = False # 強さが決まったか
        self.scroll_offset = 0  # スクロールのオフセット
        self.score = 0  # スコア
        self.game_over = False
        self.facing_right = True  # プレイヤーが右向きか左向きかのフラグ
        self.reset_indicators()  # インジケーターをリセット


    def reset_indicators(self):
        """インジケーターをリセット"""
        self.angle_mode = False
        self.angle_set = False
        self.jump_angle = 0
        self.jump_strength = 0
        self.strength_mode = False

    def update(self):
        """ゲームロジックを更新"""
        if pyxel.btnp(pyxel.KEY_R):  # Rキーでリスタート
            self.reset_game()

        if self.game_over:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  # MOUSE_BUTTON_LEFTキーでリスタート
                self.reset_game()
            return

        # ジャンプ角度指定モード
        if self.on_platform and not self.angle_mode and not self.angle_set and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.angle_mode = True
            self.jump_angle = 0  # 初期角度をリセット
            self.angle_direction = 1  # 増加方向で開始
            self.angle_set = False  # 角度が決まっていない状態
            self.strength_set = False # 強さが決まっていない状態

        # 角度指定処理
        if self.angle_mode:
            # 角度を変更
            self.jump_angle += 1.5 * self.angle_direction
            if self.jump_angle >= 90:
                self.jump_angle = 90
                self.angle_direction = -1  # 反転して減少
            elif self.jump_angle <= 0:
                self.jump_angle = 0
                self.angle_direction = 1  # 反転して増加

            # クリックを離したら強さ指定モードに移行
            if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and not self.angle_set:
                self.angle_set = True  # 角度が決まった
                self.angle_mode = False  # 角度指定モード終了

        # 強さ指定処理
        if self.angle_set and not self.strength_mode and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # 強さ指定モードに移行
            self.strength_mode = True
            self.jump_strength = 0  # 強さの初期化

        if self.strength_mode:
            # クリックしている間に強さを増加
            self.jump_strength = min(self.jump_strength + 0.25, 10)  # 最大強さは10

            # クリックを離すとジャンプ実行
            if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.strength_mode = False  # 強さモード終了
                self.strength_set = True #強さが決まった
                self.on_platform = False
                radian_angle = math.radians(self.jump_angle)
                self.player_vx = math.cos(radian_angle) * self.jump_strength  # X方向速度
                if not self.facing_right:
                    self.player_vx = -1 * self.player_vx
                self.player_vy = -math.sin(radian_angle) * self.jump_strength  # Y方向速度

                # ジャンプ開始後はインジケーターをリセット
                self.reset_indicators()

        # プレイヤーの移動
        self.player_x += self.player_vx
        self.player_y += self.player_vy

        # 重力の適用
        if not self.on_platform:
            self.player_vy += 0.25  # 重力を加算

        # 画面端で反射
        if self.player_x < 0:  # 左端で反射
            self.player_x = 0
            self.player_vx = -self.player_vx  # 水平速度反転
            self.facing_right = True  # 反転後右向き
        elif self.player_x > pyxel.width - 8:  # 右端で反射
            self.player_x = pyxel.width - 8
            self.player_vx = -self.player_vx  # 水平速度反転
            self.facing_right = False  # 反転後左向き

        # 足場の壁で反射
        for platform in self.platforms:
            px, py = platform
            if (px - 8 < self.player_x < px + 32 and
                py - 8 < self.player_y < py and
                self.player_vy > 0):  # 降下中に足場に触れる
                self.player_vy = 0
                self.player_vx = 0  # 水平速度をリセットして静止
                self.player_x = max(min(self.player_x, px + 32), px - 16)  # 足場上に位置調整
                self.player_y = py - 8
                self.on_platform = True

            # 足場の壁で反射（左壁と右壁で反射）
            if (self.player_vx > 0 and px - 8 < self.player_x < px and py - 8 < self.player_y < py + 4):
                self.player_vx = -self.player_vx  # 水平速度反転
                self.facing_right = False  # 反転後左向き
            elif (self.player_vx < 0 and px + 24 < self.player_x < px + 32 and py - 8 < self.player_y < py + 4):
                self.player_vx = -self.player_vx  # 水平速度反転
                self.facing_right = True  # 反転後右向き

        # スクロール処理
        if self.player_y + self.scroll_offset < 80 :  # プレイヤーが画面中央より上に来たらスクロール
            self.scroll_offset += 2
            #self.player_y += 2
            #self.platforms = [[x, y + 2] for x, y in self.platforms]  # 足場の位置もスクロール

        # 新しい足場の生成
        if self.scroll_offset > self.last_platform_y - self.platform_interval:
            new_x = random.randint(10, 140)
            new_y = self.last_platform_y - self.platform_interval
            self.platforms.append([new_x, new_y])
            self.last_platform_y = new_y

        # 足場が画面外に消えないように保持
        self.platforms = [p for p in self.platforms if p[1] + self.scroll_offset < 240]

        # ゲームオーバー判定
        if self.player_y + self.scroll_offset > pyxel.height:
            self.game_over = True

        # スコアを更新
        self.score = self.scroll_offset // 10

    def draw(self):
        """画面を描画"""
        pyxel.cls(0)  # 背景を黒でクリア

        if self.game_over:
            pyxel.text(50, 100, "GAME OVER", pyxel.COLOR_RED)
            pyxel.text(40, 120, f"Score: {self.score}", pyxel.COLOR_WHITE)
            pyxel.text(30, 140, "Press CLICK to Restart", pyxel.COLOR_YELLOW)
        else:
            # プレイヤーを描画
            if self.facing_right:
                pyxel.rect(self.player_x, self.player_y + self.scroll_offset , 8, 8, pyxel.COLOR_GREEN)  # 右向き
            else:
                pyxel.rect(self.player_x, self.player_y + self.scroll_offset , 8, 8, 14)  # 左向き（反転）

            # 足場を描画
            for px, py in self.platforms:
                pyxel.rect(px, py + self.scroll_offset , 32, 4, 12)  # 12 = BLUE

            # 角度指定用の矢印を描画（強さ指定モード中でも表示）
            if self.angle_mode or self.angle_set:
                arrow_length = 20
                if self.facing_right:
                    end_x = self.player_x + math.cos(math.radians(self.jump_angle - 12)) * arrow_length
                else:
                    end_x = self.player_x + math.cos(math.radians(180 - self.jump_angle + 12)) * arrow_length

                end_y = self.player_y + self.scroll_offset - math.sin(math.radians(self.jump_angle - 12)) * arrow_length
                pyxel.line(self.player_x + 4, self.player_y + self.scroll_offset + 4,
                           end_x, end_y , pyxel.COLOR_YELLOW)

            # 強さインジケーターを描画
            if self.strength_mode or (self.angle_set and not self.strength_mode):
                pyxel.line(self.player_x + 4, self.player_y + self.scroll_offset + 7, 
                           self.player_x + 4, self.player_y + self.scroll_offset + 7 - self.jump_strength * 5, 
                           pyxel.COLOR_RED)

            # スコアを表示
            pyxel.text(5, 5, f"Score: {self.score}", pyxel.COLOR_WHITE)

# ゲームを起動
AngleJumpGame()
