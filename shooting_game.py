import pyxel
import random


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_TARGETS = 5
GAME_TIME = 30 * 60  # 30秒（60帧）




class Target:
    
    def __init__(self):
        self.radius = random.randint(10, 25)
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = random.randint(self.radius, SCREEN_HEIGHT - self.radius)
        self.color = random.randint(1, 15)  
 
    def draw(self):

        pyxel.circ(self.x, self.y, self.radius, self.color)

    def is_hit(self, mouse_x, mouse_y):
      
        distance = ((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2) ** 0.5
        return distance <= self.radius


class Game:
    """游戏主类"""
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.targets = []
        self.score = 0
        self.time_left = GAME_TIME
        self.game_over = False
        self.generate_targets()
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def generate_targets(self):
        """生成新的目标圆形"""
        self.targets = [Target() for _ in range(NUM_TARGETS)]

    def update(self):
        """游戏逻辑更新"""
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):  # 按 R 重启
                self.__init__()
            return

        # 更新倒计时
        if self.time_left > 0:
            self.time_left -= 1
        else:
            self.game_over = True

        # 鼠标点击检测
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x = pyxel.mouse_x
            mouse_y = pyxel.mouse_y

            # 检查是否命中任何目标
            for i, target in enumerate(self.targets):
                if target.is_hit(mouse_x, mouse_y):
                    self.score += 1
                    # 生成新的目标替代被击中的
                    self.targets[i] = Target()
                    break  # 一次只能击中一个

    def draw(self):
        """绘制游戏画面"""
        # 绘制白色背景
        pyxel.cls(7)

        # 绘制所有目标
        for target in self.targets:
            target.draw()

        # 绘制计分板
        score_text = f"Score: {self.score}"
        pyxel.text(10, 10, score_text, 7)

        # 绘制倒计时
        time_sec = max(0, self.time_left // 60)
        time_text = f"Time: {time_sec}s"
        pyxel.text(SCREEN_WIDTH - 120, 10, time_text, 7)

        # 绘制 Game Over
        if self.game_over:
            pyxel.text(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 20, "GAME OVER!", 7)
            final_score_text = f"Final Score: {self.score}"
            pyxel.text(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, final_score_text, 7)
            pyxel.text(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 30, "Press R to Restart", 7)

pyxel.run(Game().update, Game().draw)