import pygame
import random
import time

#화면구성
pygame.init()
width, height = 430, 600
screen = pygame.display.set_mode((width, height))
background = pygame.image.load('C:/Users/Administrator/Downloads/df.jpg')
background = pygame.transform.scale(background, (width, height))

bookImage = pygame.image.load('C:/Users/Administrator/Downloads/pe.jpg')
bookImage = pygame.transform.scale(bookImage, (70,70))

sulImage = pygame.image.load('C:/Users/Administrator/Downloads/sul.png')
sulImage = pygame.transform.scale(sulImage, (70,70))
pygame.display.set_caption("Major Book For You") #배경화면도 깃허브에 올려줘야함

#변수
#font = pygame.font.Font(None, 36) <- 한글깨짐..
font = pygame.font.SysFont("Malgun Gothic", 20)
clock = pygame.time.Clock()
bg_y1 = 0
bg_y2 = -height
background_speed = 1
score = 0
missCount = 0

player = pygame.Rect(width // 2, height - 60, 50, 50)
tempSpeed = 350
speed = 350

bookList = []
bookSpeed = 4
bookTimer = 0
bookInterval = 1500

sulList = []
sulSpeed = 3
sulTimer = 0
sulInterval = 2000

slowCheck = False
slowStartTime = 0
slowDuration = 1000 #슬로우는 1초

#시작화면
def startScreen():
    global startBg
    startBg = pygame.image.load('C:/Users/Administrator/Downloads/sbg.jpg')
    startBg = pygame.transform.scale(startBg, (width, height))

    while True:
        screen.blit(startBg, (0,0))

        title = font.render("Major Book For You", True, (0, 0, 0))
        caption1 = font.render("세창이는 요즘 술을 너무 많이 마셔서", True, (0, 0, 0))
        caption2 = font.render("이젠 전공책을 모아 공부를 하고자 합니다.", True, (0, 0, 0))
        caption3 = font.render("전공책을 5번 놓치면 게임이 끝나고,", True, (0, 0, 0))
        caption4 = font.render("술과 충돌하면 1초간 속도가 느려집니다.", True, (0, 0, 0))
        caption5 = font.render("세창이를 도와서 책을 최대한 모아주세요.", True, (0, 0, 0))
        start_text = font.render("엔터키를 누르면 시작합니다!", True, (0, 0, 255))

        screen.blit(title, (width//2 - title.get_width()//2, 155))
        screen.blit(caption1, (width//2 - caption1.get_width()//2, 217))
        screen.blit(caption2, (width//1.9 - caption2.get_width()//2, 246))
        screen.blit(caption3, (width//2 - caption3.get_width()//2, 305))
        screen.blit(caption4, (width//2 - caption3.get_width()//2, 335))
        screen.blit(caption5, (width//2.1 - caption3.get_width()//2, 367))
        screen.blit(start_text, (width//2 - start_text.get_width()//2, 425))

        pygame.display.update()

        #pygame 창 종료버튼 -> 종료 or 엔터로 시작
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return


#종료화면
def overScreen(score):

    while True:
        screen.blit(startBg, (0,0))
        overText = font.render("책을 5회 놓쳤습니다. -ㅅ-", True, (0, 0, 255))
        scoreText = font.render(f"모은 책 수 : {score}개", True, (0, 0, 0))
        if(score==0):
            lastText = font.render("공부할 책이 없는 세창이는 실망했습니다..", True, (0, 0, 0))
        else:
            lastText = font.render("공부할 책이 생긴 세창이는 기쁘겠죠?", True, (0, 0, 0))

        screen.blit(overText, (width//2 - overText.get_width()//2, 246))
        screen.blit(scoreText, (width//2 - scoreText.get_width()//2, 305))
        screen.blit(lastText, (width//2 - lastText.get_width()//2, 335))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

startScreen()

#메인 루프
running = True
while running:
    dt = clock.tick(60)
    bookTimer += dt
    sulTimer += dt

    #슬로우 판단 (술 충돌)
    if(slowCheck == True):
        if pygame.time.get_ticks() - slowStartTime > slowDuration:
            speed = tempSpeed
            slowCheck = False

    #pygame 창 종료버튼 -> 종료
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #플레이어 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= speed * (dt/1000)
    if keys[pygame.K_RIGHT] and player.right < width:
        player.x += speed * (dt/1000)

    #책 이동 + 속도 빨라지게
    if(bookTimer > bookInterval):
        bookList.append(pygame.Rect(random.randint(0, width-45), 0, 70, 70))
        bookTimer = 0
        if bookInterval > 450:
            bookInterval -= 150

    for book in bookList.copy():
        book.y += bookSpeed
        if(book.y > 610):
            bookList.remove(book)
            missCount += 1
        if(player.colliderect(book)):
            score += 1
            bookList.remove(book)
    
    #술 이동 + 속도는 그대로
    if(sulTimer > sulInterval):
        sulList.append(pygame.Rect(random.randint(0, width-45), 0, 50, 50)) 
        sulTimer = 0
    
    for sul in sulList.copy():
        sul.y += sulSpeed
        if(sul.y > 610):
            sulList.remove(sul)
        if(player.colliderect(sul)):
            sulList.remove(sul)
            speed = 175 #술에 충돌시 1초간 속도 50% 됨
            slowCheck = True
            slowStartTime = pygame.time.get_ticks()
    
    #데스카운트 구현
    if(missCount == 5):
        overScreen(score)
        break

    #화면스크롤
    bg_y1 += background_speed
    bg_y2 += background_speed

    if bg_y1 >= height:
        bg_y1 = -height

    if bg_y2 >= height:
        bg_y2 = -height

    #화면스크롤과 객체 그리기
    screen.fill((0, 0, 0))
    screen.blit(background, (0, bg_y1)) #배경이 계속 이어지게
    screen.blit(background, (0, bg_y2))

    scoreBox = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(scoreBox, (10,10))

    missCountBox = font.render(f"Missed: {missCount}", True, (255, 255, 255))
    screen.blit(missCountBox, (300,10))

    pygame.draw.rect(screen, (0, 255, 0), player)
    for book in bookList:
        screen.blit(bookImage, book)
    for sul in sulList:
        screen.blit(sulImage, sul)

    pygame.display.update()
    
pygame.quit()