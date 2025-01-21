
import asyncio
import pygame,sys
import random
import os
# os.chdir("C:/Users/篠原尚希/mygit")
# 画面サイズ

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AVOID")


base_path = os.path.dirname(os.path.abspath(__file__))
player_image_path = os.path.join(base_path, "assets/player.jpg")
enemy_image_path = os.path.join(base_path, "assets/enemy.jpg")
player_image = pygame.image.load(player_image_path).convert_alpha()
enemy_image = pygame.image.load(enemy_image_path).convert_alpha()


# 初期化
pygame.init()



# 色定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)  

#フォント設定
font_path = "C:/Windows/Fonts/meiryo.ttc"
if not os.path.exists(font_path):
    raise FileNotFoundError(f"フォントファイルが見つかりません: {font_path}")
font = pygame.font.Font(font_path, 30)

# プレイヤーの設定
player_size = 80
player_pos = [WIDTH // 2, HEIGHT - player_size - 10]
player_speed = 30

#敵の設定
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_speed = 20

# 画像の読み込み
# player_image = pygame.image.load("C:/Users/篠原尚希/mygit/pythongame/images/player.jpg").convert_alpha()
# enemy_image = pygame.image.load("C:/Users/篠原尚希/mygit/pythongame/images/enemy.jpg").convert_alpha()

# 画像をリサイズ
# player_image = pygame.transform.scale(player_image, (player_size, player_size))
# enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

print(f"Player Position: {player_pos}, Player Size: {player_size}")
print(player_image.get_size())
print(f"Rendering Player at {player_pos}")

#スコア設定
score = 0
high_score = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())

# ゲームの状態管理
state = "tutorial"  # "menu", "game", "game_over"
running = True
clock = pygame.time.Clock()



#チュートリアル画面 
async def display_tutorial():
    screen.fill(WHITE)
    title = font.render("~AVOID~", True, RED)
    start  = font.render("スペースキーをタップしてゲームを開始してください", True, BLACK)
    made = font.render("produced by Naoki & Chat GPT", True, BLACK)
   
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    screen.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2 ))
    screen.blit(made, (WIDTH // 2 - made.get_width() // 2 + 160, HEIGHT // 2 + 250))
    pygame.display.flip()
    await asyncio.sleep(0)

# メニュー画面
async def display_menu():
    screen.fill(BLACK)
    menu_title = font.render("メニュー画面", True, WHITE)
    menu_option = font.render("スペースキーでゲーム開始", True, WHITE)
    screen.blit(menu_title, (WIDTH // 2 - menu_title.get_width() // 2, HEIGHT // 3))
    screen.blit(menu_option, (WIDTH // 2 - menu_option.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    await asyncio.sleep(0)

# メインゲーム

# スピードレベルの初期化
speed_level = 1  # 初期スピードレベル
speedup_timer = 0
max_speed_level = 10

# 入力ロックのフラグ
input_locked = False

# カウントダウン画面を表示する関数
async def countdown():
    global input_locked
    input_locked = True  # カウントダウン中は入力をロック

    for i in range(3, 0, -1):  # 3から1までのカウントダウン
        screen.fill(WHITE)  # 背景をリセット
        screen.blit(player_image, (player_pos[0], player_pos[1]))  # プレイヤー
        # pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))  # 敵
        countdown_text = font.render(str(i), True, RED)  # カウントダウンの数字を描画
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()  # 描画を更新
        await asyncio.sleep(1)  # 1秒間待機
    
    # 最後に "スタート!" を表示
    start_text = font.render("スタート!", True, GREEN)
    screen.fill(WHITE)
    screen.blit(player_image, (player_pos[0], player_pos[1]))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
    pygame.display.flip()
      # 1秒間待機

    input_locked = False   # カウントダウン終了後に入力ロック解除

    await asyncio.sleep(1)



# プレイヤーの描画処理を修正
async def draw_player():
    # 通常の描画
    screen.blit(player_image, (round(player_pos[0]), round(player_pos[1])))
    
    # 画面左端を超えた場合、右端にも描画
    if player_pos[0] < 0:
        screen.blit(player_image, (round(player_pos[0] + WIDTH), round(player_pos[1])))
    
    # 画面右端を超えた場合、左端にも描画
    if player_pos[0] + player_size > WIDTH:
        screen.blit(player_image, (round(player_pos[0] - WIDTH), round(player_pos[1])))

    await asyncio.sleep(0)



#メイン
async def main_game():
    global high_score
    global player_pos, enemy_pos, enemy_speed, score, state, speed_level, speedup_timer
    screen.fill(WHITE)

 # 入力がロックされている場合はキー入力を無視
    if not input_locked:
       # プレイヤーの動き
       keys = pygame.key.get_pressed()
       if keys[pygame.K_LEFT]:
           player_pos[0] -= player_speed
       if keys[pygame.K_RIGHT]:
           player_pos[0] += player_speed

    # プレイヤーの画面端でのループ処理
    if player_pos[0] < 0:  # 左端を超えた場合
        player_pos[0] = WIDTH - player_size  # 右端に移動
    elif player_pos[0] + player_size > WIDTH:  # 右端を超えた場合
        player_pos[0] = 0  # 左端に移動

 # プレイヤーの描画
    await draw_player()

# 敵の動き
    enemy_pos[1] += enemy_speed
    if enemy_pos[1] > HEIGHT:
       enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
       score += 1  # スコア加算


# スコアに応じて敵のスピードを上昇させる
       if score % 3 == 0 and speed_level < max_speed_level:  # スピードレベルが上限未満なら
          enemy_speed += 2
          speed_level += 1 
          speedup_timer = 20

# 衝突判定
    if (player_pos[0] < enemy_pos[0] + enemy_size and
        player_pos[0] + player_size > enemy_pos[0] and
        player_pos[1] < enemy_pos[1] + enemy_size and
        player_pos[1] + player_size > enemy_pos[1]):
        state = "game_over"

          # スコアボードのテキストを初期化
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))


     # スピードレベルがMAXかどうかを表示
    if speed_level >= max_speed_level:
        speed_level_text = font.render("Speed Level: MAX", True, RED)
    else:
        speed_level_text = font.render(f"Speed Level: {speed_level}", True, RED)
    screen.blit(speed_level_text, (10, 90))

# スピードアップの文字を表示（タイマーが残っている間）
    if speedup_timer > 0 and score > 0:  # スコアが1以上のときのみ表示
        speedup_text = font.render("スピードアップ！", True, RED)
        screen.blit(speedup_text, (WIDTH // 2 - speedup_text.get_width() // 2, HEIGHT // 2 - 50))
        speedup_timer -= 1  # タイマーを減らす
    
# スコアボード表示
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    speed_level_text = font.render(f"Speed Level: {speed_level}", True, RED)  # スピードレベル表示
   
# 敵の描画
    screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))
    pygame.display.flip()
    await asyncio.sleep(0)


# ゲームオーバー画面
    async def display_game_over():
      global high_score, score, state,enemy_speed,speed_level

    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as file:
           file.write(str(high_score))

    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, RED)
    restart_text = font.render("スペースキーで再スタート", True, WHITE)
    score_text = font.render(f"得点: {score}", True, GREEN)  # スコアを描画
    high_score_text = font.render(f"最高得点: {high_score}", True, BLUE)  # ハイスコアを描画


    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 150))
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()  #画面を更新
    enemy_speed =30
    speed_level = 1
    await asyncio.sleep(0)



# メインループ
    


    # メインループ
    async def main_loop():
        global running, state
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if state == "tutorial" and event.key == pygame.K_SPACE:
                        state = "menu"
                    elif state == "menu" and event.key == pygame.K_SPACE:
                        state = "game"
                    elif state == "game_over" and event.key == pygame.K_SPACE:
                        state = "menu"
                 

        # 状態に応じた関数を呼び出す
        if state == "tutorial":
            await display_tutorial()
        elif state == "menu":
            await display_menu()
        elif state == "game":
            await main_game()  # コメントアウトを解除してゲームプレイロジックを実行
        elif state == "game_over":
            await display_game_over()

        # フレームレートを調整
        await asyncio.sleep(1 / 60)  # 60FPS

    # async def main_loop():
    #     global running
    #     while running:
    #         for event in pygame.event.get():
    #            if event.type == pygame.QUIT:
    #                running = False
    #         # その他のイベント処理...

    #         if state == "tutorial":
    #              await display_tutorial()
    #         elif state == "menu":
    #              await display_menu()
    #         # elif state == "game":
    #         #      await main_loop()
    #         elif state == "game_over":
    #              await display_game_over()

    # while running:
    # #   for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     if event.type == pygame.KEYDOWN:
    #         if state == "tutorial" and event.key == pygame.K_SPACE:
    #               state = "menu"
    #         elif state == "menu" and event.key == pygame.K_SPACE:
    #             state = "game"
               
    #             await countdown()  # カウントダウンを表示
        

    #         elif state == "game_over" and event.key == pygame.K_SPACE:
    #             state = "menu"
    #             score = 0
    #             player_pos = [WIDTH // 2, HEIGHT - player_size - 10]
    #             enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]


    #   if state == "tutorial":
    #     await display_tutorial()
    #   elif state == "menu":
    #     await display_menu()
    #   elif state == "game":
    #     await main_game()
    #   elif state == "game_over":
    #     await display_game_over()

        await asyncio.sleep(1 / 60)  # 60FPS相当のフレームレート制御


asyncio.run(main_game())  
  # ゲーム終了処理
pygame.quit()