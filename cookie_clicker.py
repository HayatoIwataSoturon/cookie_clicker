import pygame
from pygame import mixer
import random as ram
import math
import sys
import os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

#画像のリサイズ
def get_size(image,bai=0.5):
    width, height = image.get_size()
    image = pygame.transform.scale(image, (width*bai,height*bai)) 
    return image



# スプライトアニメーションさせるクラス
class Animation(pygame.sprite.Sprite):
    # コンストラクタ
    def __init__(self,image1,image2,x,y):
        super(Animation, self).__init__()

        # 画像をリストで読み込み
        self.images = list()
        self.images.append(image1)
        self.images.append(image2)

        # 画像はindexで管理すると楽
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() # 描写範囲(必須)
        self.rect.x = x
        self.rect.y = y

    # 1フレーム事に実行される関数
    def update(self):
        # ループ処理
        if self.index >= len(self.images):
            self.index = 0

        self.image = self.images[self.index]
        self.index += 1

#クリックしたときの映像処理
class Click(pygame.sprite.Sprite):
    # コンストラクタ
    def __init__(self,image1,image2):
        super(Click, self).__init__()

        # 画像をリストで読み込み
        self.images = list()
        self.images.append(image1)
        self.images.append(image2)

        # 画像はindexで管理すると楽
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() # 描写範囲(必須)
        self.rect.x = 200
        self.rect.y = 100

    # 1フレーム事に実行される関数
    def update(self,event,sound):
        x, y = pygame.mouse.get_pos()
        zouka = False
        if x < 550 and x > 400 and y < 550 and y > 300:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.index = 1
            if event.type == pygame.MOUSEBUTTONUP:
                self.index = 0
                sound.play()
                zouka = True
            
            self.image = self.images[self.index]
            return zouka
        
#クッキーをクリックした後に飛び出るアニメーションをさせるクラス
class AnimationCookie(pygame.sprite.Sprite):
    # コンストラクタ
    def __init__(self,image1):
        super(AnimationCookie, self).__init__()

        # 画像はindexで管理すると楽
        self.image = image1
        self.rect = self.image.get_rect() # 描写範囲(必須)
        self.rect.x = 200
        self.rect.y = 100
        self.second = 0
        self.sokudo = ram.randint(-100,100)
        self.theta = math.radians(ram.randint(0,360))

    # 1フレーム事に実行される関数
    def update(self):
        # ループ処理
        self.image = self.image
        self.second = self.second + 0.8
        self.rect.x = self.sokudo * math.cos(self.theta) * self.second + 200
        self.rect.y = self.sokudo * math.sin(self.theta) * self.second + 0.5 * 9.8 * self.second ** 2 + 100

#怒奴我尾の神のアニメーションをさせるクラス
class AnimationDoya(pygame.sprite.Sprite):
    # コンストラクタ
    def __init__(self,image1,image2):
        super(AnimationDoya, self).__init__()

        # 画像はindexで管理すると楽
        self.images = list()
        self.images.append(image1)
        self.images.append(image2)

        # 画像はindexで管理すると楽
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() # 描写範囲(必須)
        self.rect.x = 400
        self.rect.y = -200
        self.maturi = False
        self.maturi_time = 200
        self.kakuritu = []
        self.Switch = False

    # 1フレーム事に実行される関数
    def update(self,event,sound):
        # ループ処理
        self.Switch = True
        x, y = pygame.mouse.get_pos()
        if self.rect.y < 80 and self.maturi == False:
            self.rect.y = self.rect.y + 10
        if x < 550 and x > 430 and y < self.rect.y + 150 and y > self.rect.y + 50 and self.maturi == False:
            if event.type == pygame.MOUSEBUTTONUP:
                self.index = 1
                sound.play()
                self.maturi = True
        if self.maturi == True and self.rect.y > -200 and self.maturi_time < 180:
            self.rect.y = self.rect.y - 10
        if self.maturi == True:
            self.maturi_time = self.maturi_time - 1
            self.kakuritu = (ram.randint(0,255),ram.randint(0,255),ram.randint(0,255))
            if self.maturi_time == 0:
                self.maturi = False
                self.maturi_time = 200
                self.index = 0
                self.Switch = False

        self.image = self.images[self.index]



def main():
        #初期化
    pygame.init()

    #クッキーの現在の枚数
    cookie_num = 0

    #スクリーンの設定
    screen = pygame.display.set_mode((1000, 800))
    running = True
    #windowの名前
    pygame.display.set_caption("cookie clicker")
    #windowの色
    BACKGROUND_COLOR = (0,0,0)
    screen.fill(BACKGROUND_COLOR)
    #ボタンの準備
    button = pygame.Rect(900, 30, 80, 80)  # creates a rect object
    #強化画面の準備
    gamen = pygame.Rect(800, 0, 200, 800)
    #サブ画面の準備
    sub = pygame.Rect(100, 200, 500, 300)
    #エンディング画面の準備
    ending1 = pygame.Rect(300, 300, 500, 100)
    ending2 = pygame.Rect(305, 305, 490, 90)

    #exe化準備
    resource_path('cookie.png')



    #画像の準備
    Cookie = pygame.image.load("image/cookie.png")
    Uhho_1 = pygame.image.load("image/uhho_1.png")
    Uhho_2 = pygame.image.load("image/uhho_2.png")
    Chef_1 = pygame.image.load("image/chef_1.png")
    Chef_2 = pygame.image.load("image/chef_2.png")
    Scientist_1 = pygame.image.load("image/scientist_1.png")
    Scientist_2 = pygame.image.load("image/scientist_2.png")
    Doyagao_1 = pygame.image.load("image/doyagao_1.png")
    Doyagao_2 = pygame.image.load("image/doyagao_2.png")
    Hand = pygame.image.load("image/hand.png")
    Koumoku_1 = pygame.image.load("image/koumoku_1.png")
    Koumoku_2 = pygame.image.load("image/koumoku_2.png")
    Koumoku_3 = pygame.image.load("image/koumoku_3.png")
    Koumoku_4 = pygame.image.load("image/koumoku_4.png")
    Batu = pygame.image.load("image/batu.png")
    Shoukan = pygame.image.load("image/shoukan.png")
    Cookie_icon = pygame.image.load("image/cookie_icon.png")


    #音声の準備
    miyoin = mixer.Sound("sound/myoi-n.wav")
    hikariare = mixer.Sound("sound/hikari_are.wav")
    coin = mixer.Sound("sound/coin.wav")
    po = mixer.Sound("sound/po.wav")
    boo = mixer.Sound("sound/boo.wav")

    #画像のリサイズ
    cookie = get_size(Cookie,0.5)
    cookie_end = get_size(Cookie,0.2)
    cookie_click = get_size(Cookie,0.49)
    uhho_1 = get_size(Uhho_1,0.1)
    uhho_2 = get_size(Uhho_2,0.1)
    chef_1 = get_size(Chef_1,0.15)
    chef_2 = get_size(Chef_2,0.15)
    scientist_1 = get_size(Scientist_1,0.15)
    scientist_2 = get_size(Scientist_2,0.15)
    doyagao_1 = get_size(Doyagao_1,0.15)
    doyagao_2 = get_size(Doyagao_2,0.15)
    hand = get_size(Hand,0.15)
    uhho_menu = get_size(Uhho_1,0.2)
    chef_menu = get_size(Chef_1,0.15)
    scientist_menu = get_size(Scientist_1,0.18)
    koumoku_1 = get_size(Koumoku_1,0.45)
    koumoku_2 = get_size(Koumoku_2,0.45)
    koumoku_3 = get_size(Koumoku_3,0.45)
    koumoku_4 = get_size(Koumoku_4,0.45)
    batu = get_size(Batu,0.1)
    shoukan = get_size(Shoukan,0.38)

    #アイコンの設定
    pygame.display.set_icon(Cookie_icon)

    #変数など
    x_random = ram.randint(0,800)
    y_random = ram.randint(100,700)
    kakuritu = []
    kakushi_time = 0
    cookie_fps = 0


    # アニメーションの準備
    cookie_uhho = Click(cookie,cookie_click)
    cookie_group = pygame.sprite.Group(cookie_uhho)
    doya = AnimationDoya(doyagao_1,doyagao_2)
    doya_group = pygame.sprite.Group(doya)
    uhho_group = pygame.sprite.Group()
    chef_group = pygame.sprite.Group()
    scientist_group = pygame.sprite.Group()
    cookie_tobu_group = pygame.sprite.Group()

    #アニメーションが何体いるか
    uhho_num = 0
    chef_num = 0
    scientist_num = 0

    # クロックを開始
    clock = pygame.time.Clock() 
    #FPS
    FPS = 10

    #購入金額
    yubi_gold = 10
    uhho_gold = 100
    chef_gold = 1000
    scientist_gold = 100000

    #レベル
    yubi_lebel = 1
    uhho_lebel = 1
    chef_lebel = 1
    scientist_lebel = 1


    #TorF
    step1 = False
    step2 = False
    step3 = False
    kyouka_gamen = False
    sub_btn = False
    yubi_btn = False
    uhho_btn = False
    chef_btn = False
    scientist_btn = False
    doya_btn = False
    end = False




    #フォントの準備
    font = pygame.font.SysFont(None, 80)
    font_jp = pygame.font.Font('ipaexm.ttf', 40)
    font_jp_k = pygame.font.Font('ipaexm.ttf', 30)
    font_jp_end = pygame.font.Font('ipaexm.ttf', 80)

    #ゲームのループ開始
    while running:
        doya_shutugen = ram.randint(0,3000)
        x, y = pygame.mouse.get_pos()
        #背景色で塗りつぶし        
        screen.fill(BACKGROUND_COLOR)
        if doya_btn == True:
            screen.fill(kakuritu)
        if step1 == True:
            if kyouka_gamen == False:
                #ボタンの表示
                pygame.draw.rect(screen, (255, 255, 255), button)
                kyouka = font_jp.render('強化', True, (0,0,0))
                screen.blit(kyouka,(900,50))
            if kyouka_gamen == True:
                pygame.draw.rect(screen, (255, 255, 255), gamen)
                screen.blit(koumoku_2,(800,250))
                screen.blit(koumoku_1,(800,50))
                if step2 == True:
                    screen.blit(koumoku_3,(800,450))
                if step3 == True:
                    screen.blit(koumoku_4,(795,650))
        message = font.render(f"{cookie_num}", False, (255,255,255))
        screen.blit(message,(100,50))

        #イベント処理
        for event in pygame.event.get():
            #終了処理
            if event.type == pygame.QUIT:
                running = False
            #強化画面遷移
            if step1 == True:
                if kyouka_gamen == True:
                    if sub_btn == False and x < 800 and event.type == pygame.MOUSEBUTTONUP:
                        pygame.draw.rect(screen, (255, 255, 255), button)
                        screen.blit(koumoku_1,(800,50))
                        kyouka_gamen = False
                    #ゆびボタン
                    if x > 800 and x < 1000 and y > 50 and y < 130 and event.type == pygame.MOUSEBUTTONUP:
                        po.play()
                        pygame.draw.rect(screen, (255, 255, 255), sub)
                        sub_btn = True
                        yubi_btn = True
                        uhho_btn = False
                        chef_btn = False
                        scientist_btn = False
                    #ゆびサブ
                    if x > 270 and x < 430 and y > 430 and y < 500 and event.type == pygame.MOUSEBUTTONUP and yubi_btn == True:
                            if cookie_num >= yubi_gold:
                                yubi_lebel = yubi_lebel + 1
                                cookie_num = cookie_num - yubi_gold
                                yubi_gold = yubi_gold * 10
                                coin.play()
                            else:
                                boo.play()
                    #ウッホボタン
                    if x > 800 and x < 1000 and y > 250 and y < 330 and event.type == pygame.MOUSEBUTTONUP:
                            po.play()
                            pygame.draw.rect(screen, (255, 255, 255), sub)
                            sub_btn = True
                            uhho_btn = True
                            yubi_btn = False
                            chef_btn = False
                            scientist_btn = False
                    #ウッホサブ
                    if x > 270 and x < 430 and y > 430 and y < 500 and event.type == pygame.MOUSEBUTTONUP and uhho_btn == True:
                            if cookie_num >= uhho_gold:
                                uhho_lebel = uhho_lebel + 1
                                cookie_num = cookie_num - uhho_gold
                                uhho_gold = int(uhho_gold * 1.05)
                                coin.play()
                            else:
                                boo.play()
                    if step2 == True:
                        #シェフボタン
                        if x > 800 and x < 1000 and y > 450 and y < 530 and event.type == pygame.MOUSEBUTTONUP:
                            po.play()
                            pygame.draw.rect(screen, (255, 255, 255), sub)
                            sub_btn = True
                            chef_btn = True
                            yubi_btn = False
                            uhho_btn = False
                            scientist_btn = False
                        #シェフサブ
                        if x > 270 and x < 430 and y > 430 and y < 500 and event.type == pygame.MOUSEBUTTONUP and chef_btn == True:
                            if cookie_num >= chef_gold:
                                chef_lebel = chef_lebel + 1
                                cookie_num = cookie_num - chef_gold
                                chef_gold = int(chef_gold * 1.2)
                                coin.play()
                            else:
                                boo.play()
                    if step3 == True:
                        #サイエンティストボタン
                        if x > 800 and x < 1000 and y > 660 and y < 730 and event.type == pygame.MOUSEBUTTONUP:
                            po.play()
                            pygame.draw.rect(screen, (255, 255, 255), sub)
                            sub_btn = True
                            scientist_btn = True
                            yubi_btn = False
                            uhho_btn = False
                            chef_btn = False
                        #サイエンティストサブ
                        if x > 270 and x < 430 and y > 430 and y < 500 and event.type == pygame.MOUSEBUTTONUP and scientist_btn == True:
                            if cookie_num >= scientist_gold:
                                scientist_lebel = scientist_lebel + 1
                                cookie_num = cookie_num - scientist_gold
                                scientist_gold = int(scientist_gold * 2)
                                coin.play()
                            else:
                                boo.play()
                if kyouka_gamen == False:
                    if x < 980 and x > 900 and y < 100 and y > 30 and event.type == pygame.MOUSEBUTTONUP:
                        po.play()
                        pygame.draw.rect(screen, (255, 255, 255), gamen)
                        kyouka_gamen = True
            if sub_btn == False:
                zouka = cookie_uhho.update(event,miyoin)
                #zoukaがTrueならば+1
                if zouka == True:
                    cookie_tobu = AnimationCookie(cookie)
                    cookie_tobu_group.add(cookie_tobu)
                    if doya_btn == False:
                        cookie_num = cookie_num + yubi_lebel ** 2
                    if doya_btn == True:
                        cookie_num = cookie_num + yubi_lebel ** 10

        #ウッホのアニメーションを増やす
        if uhho_num < uhho_lebel-1:
            x_random = ram.randint(0,700)
            y_random = ram.randint(100,700)
            uhho_num = uhho_num + 1
            uhho = Animation(uhho_1,uhho_2,x_random,y_random)
            uhho_group.add(uhho)
        #シェフのアニメーションを増やす
        if chef_num < chef_lebel-1:
            x_random = ram.randint(0,700)
            y_random = ram.randint(100,700)
            chef_num = chef_num + 1
            chef = Animation(chef_1,chef_2,x_random,y_random)
            chef_group.add(chef)
        #サイエンティストのアニメーションを増やす
        if scientist_num < scientist_lebel-1:
            x_random = ram.randint(0,700)
            y_random = ram.randint(100,700)
            scientist_num = scientist_num + 1
            scientist = Animation(scientist_1,scientist_2,x_random,y_random)
            scientist_group.add(scientist)

        #怒奴我尾の神の出現確率
        if doya_shutugen == 548:
            doya.Switch = True
        if doya.Switch == True:
            doya_group.update(event,hikariare)
            kakuritu = doya.kakuritu
            doya_btn = doya.maturi
        if doya.Switch == False:
            doya_shutugen = 0
        # 画像を更新して描写
        uhho_group.update()
        chef_group.update()
        scientist_group.update()
        cookie_tobu_group.update()
        uhho_group.draw(screen)
        chef_group.draw(screen)
        scientist_group.draw(screen)
        doya_group.draw(screen)
        cookie_group.draw(screen)
        cookie_tobu_group.draw(screen)
        
        if sub_btn == True:
            pygame.draw.rect(screen, (255, 255, 255), sub)
            screen.blit(batu,(550,200))
            if x > 550 and x < 600 and y > 200 and y < 250:
                    if event.type == pygame.MOUSEBUTTONUP:
                        sub_btn = False
                        yubi_btn = False
                        uhho_btn = False
                        chef_btn = False
                        scientist_btn = False
            #ゆび
            if yubi_btn == True:
                screen.blit(hand,(300,250))
                screen.blit(shoukan,(270,430))
                message1 = font_jp.render('ゆび', True, (0,0,0))
                message2 = font_jp_k.render('クリック時に獲得できる', True, (0,0,0))
                message3 = font_jp_k.render('クッキー数がレベルの2乗になる', True, (0,0,0))
                message4 = font_jp_k.render(f'レベル{yubi_lebel}', True, (0,0,0))
                message5 = font_jp_k.render('購入金額', True, (0,0,0))
                message6 = font_jp_k.render(f'{yubi_gold}', True, (0,0,0))
                screen.blit(message1,(100,200))
                screen.blit(message2,(100,350))
                screen.blit(message3,(100,400))
                screen.blit(message4,(150,300))
                screen.blit(message5,(100,240))
                screen.blit(message6,(100,275))

            #ウッホ
            if uhho_btn == True:
                screen.blit(uhho_menu,(200,180))
                screen.blit(shoukan,(270,430))
                message1 = font_jp.render('ウッホ', True, (0,0,0))
                message2 = font_jp_k.render('ふつうのウッホ', True, (0,0,0))
                message3 = font_jp_k.render('クッキー作りを手伝ってくれる', True, (0,0,0))
                message4 = font_jp_k.render(f'レベル{uhho_lebel}', True, (0,0,0))
                message5 = font_jp_k.render('購入金額', True, (0,0,0))
                message6 = font_jp_k.render(f'{uhho_gold}', True, (0,0,0))
                screen.blit(message1,(100,200))
                screen.blit(message2,(100,350))
                screen.blit(message3,(100,400))
                screen.blit(message4,(100,300))
                screen.blit(message5,(100,240))
                screen.blit(message6,(100,275))
            #シェフ
            if chef_btn == True:
                screen.blit(chef_menu,(280,200))
                screen.blit(shoukan,(270,430))
                message1 = font_jp.render('シェフ', True, (0,0,0))
                message2 = font_jp_k.render('シェフウッホ', True, (0,0,0))
                message3 = font_jp_k.render('クッキーしか作れない', True, (0,0,0))
                message4 = font_jp_k.render(f'レベル{chef_lebel}', True, (0,0,0))
                message5 = font_jp_k.render('購入金額', True, (0,0,0))
                message6 = font_jp_k.render(f'{chef_gold}', True, (0,0,0))
                screen.blit(message1,(100,200))
                screen.blit(message2,(100,350))
                screen.blit(message3,(100,400))
                screen.blit(message4,(100,300))
                screen.blit(message5,(100,240))
                screen.blit(message6,(100,275))
            #サイエンティスト
            if scientist_btn == True:
                screen.blit(scientist_menu,(250,180))
                screen.blit(shoukan,(270,430))
                message1 = font_jp.render('サイエンティスト', True, (0,0,0))
                message2 = font_jp_k.render('マッドサイエンティスト', True, (0,0,0))
                message3 = font_jp_k.render('博士号は持っていない', True, (0,0,0))
                message4 = font_jp_k.render(f'レベル{scientist_lebel}', True, (0,0,0))
                message5 = font_jp_k.render('購入金額', True, (0,0,0))
                message6 = font_jp_k.render(f'{scientist_gold}', True, (0,0,0))
                screen.blit(message1,(100,200))
                screen.blit(message2,(100,350))
                screen.blit(message3,(100,400))
                screen.blit(message4,(100,300))
                screen.blit(message5,(100,240))
                screen.blit(message6,(100,275))

        if doya_btn == True:
            cookie_tobu = AnimationCookie(cookie)
            cookie_tobu_group.add(cookie_tobu)
            #自動で増える分
            cookie_fps = (uhho_lebel-1) * 10 + (chef_lebel-1) * 100 + (scientist_lebel-1) * 10000
            cookie_num = cookie_num + cookie_fps


        if doya_btn == False:
            #自動で増える分
            cookie_fps = (uhho_lebel-1) * 1 + (chef_lebel-1) * 10 + (scientist_lebel-1) * 1000
            cookie_num = cookie_num + cookie_fps

        #fpsの表示 
        fps_font = font.render(f'{cookie_fps}/fps', True, (255,255,255))
        screen.blit(fps_font,(100,150))

            
        pygame.display.update()

        clock.tick(FPS) # フレームレート分待機

        if cookie_num >= 10:
            step1 = True

        if cookie_num >= 1000:
            step2 = True
        
        if cookie_num > 100000:
            step3 = True

        if cookie_num > 1000000000000 and end == False:
            end = True
        while end == True:
            if kakushi_time < 270:
                kakushi_time = kakushi_time + 0.1
                screen.fill(BACKGROUND_COLOR)
                pygame.draw.rect(screen, (255, 255, 255), ending1)
                pygame.draw.rect(screen, (0, 0, 0), ending2)
                kan = font_jp_end.render('完', True, (255,255,255))
                erai = font_jp_k.render('えらいっ', True, (255,255,255))
                screen.blit(erai,(320,320))
                screen.blit(kan,(800,600))
                screen.blit(cookie_end,(100,100))
                #イベント処理
            for event in pygame.event.get():
                #終了処理
                if event.type == pygame.QUIT:
                    running = False
                    end = False
            if kakushi_time > 270:
                screen.fill(BACKGROUND_COLOR)
                pygame.draw.rect(screen, (255, 255, 255), ending1)
                pygame.draw.rect(screen, (0, 0, 0), ending2)
                kan = font_jp_end.render('完', True, (255,255,255))
                konna = font_jp_k.render('こんなゲームにまじに', True, (255,255,255))
                dousuruno = font_jp_k.render('なっちゃってどうするの', True, (255,255,255))
                screen.blit(konna,(320,320))
                screen.blit(dousuruno,(320,350))
                screen.blit(kan,(800,600))
                screen.blit(cookie_end,(100,100))
            clock.tick(FPS) # フレームレート分待機
            pygame.display.update()





if __name__ == '__main__':
    main()