import pyxel
import time

class ClickerGame:
    def __init__(self):
        # 初期設定
        self.money = 0                # 所持金
        self.click_income = 1         # クリック収入
        self.passive_income = 0       # 受動的収入
        self.last_time = time.time()  # 受動的収入の更新時間
        self.upgrade_cost = 10        # アップグレードのコスト

        # Pyxelの初期化
        pyxel.init(160, 120, caption="クリックでお金を増やすゲーム")
        pyxel.run(self.update, self.draw)

    def update(self):
        # クリックでお金を増やす
        if pyxel.mouse_x >= 50 and pyxel.mouse_x <= 110 and pyxel.mouse_y >= 30 and pyxel.mouse_y <= 50:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.money += self.click_income

        # アップグレードの購入
        if pyxel.mouse_x >= 50 and pyxel.mouse_x <= 110 and pyxel.mouse_y >= 70 and pyxel.mouse_y <= 90:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.money >= self.upgrade_cost:
                self.money -= self.upgrade_cost
                self.click_income += 1
                self.upgrade_cost *= 2  # アップグレードのコストを倍にする

        # 受動的収入の追加（1秒ごとに増える）
        current_time = time.time()
        if current_time - self.last_time >= 1:
            self.money += self.passive_income
            self.last_time = current_time

        # 受動的収入をアップグレード可能にする（資金が一定額を超えるごとに）
        if self.money >= 50 and self.passive_income == 0:
            self.passive_income = 1  # 受動的収入が1に
        elif self.money >= 100 and self.passive_income == 1:
            self.passive_income = 2  # 受動的収入が2に

    def draw(self):
        pyxel.cls(0)  # 画面をクリア

        # 資金表示
        pyxel.text(10, 10, f"Money: {self.money}", pyxel.COLOR_WHITE)

        # クリックエリア
        pyxel.rect(50, 30, 60, 20, pyxel.COLOR_RED)
        pyxel.text(55, 35, f"Click +{self.click_income}", pyxel.COLOR_WHITE)

        # アップグレードボタン
        pyxel.rect(50, 70, 60, 20, pyxel.COLOR_GREEN)
        pyxel.text(55, 75, f"Upgrade ({self.upgrade_cost})", pyxel.COLOR_WHITE)

        # 受動的収入の表示
        if self.passive_income > 0:
            pyxel.text(10, 30, f"Passive income: +{self.passive_income}/s", pyxel.COLOR_YELLOW)

if __name__ == "__main__":
    ClickerGame()
