import pygame
import os

from pygame.constants import KEYDOWN
##########################################################
#기본 초기화(반드시 해야하는 것들)
pygame.init() #초기화, 반드시 필요

#화면크기 설정
screen_width = 640 #가로크기
screen_height = 480 #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("공 피하기!") #게임 이름

#FPS
clock = pygame.time.Clock()
###########################################################


#1. 사용자 게임 초기화(배경화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) #현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") #image 폴더 위치 반환

#배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #스테이지의 높이 위에 캐릭터를 두기 위해

#캐릭터 만들기
chacracter = pygame.image.load(os.path.join(image_path, "chacracter.png"))
chacracter_size = chacracter.get_rect().size
chacracter_width = chacracter_size[0]
chacracter_height = chacracter_size[1]
chacracter_x_pos = (screen_width/2) - (chacracter_width/2)
chacracter_y_pos = screen_height - chacracter_height - stage_height

#캐릭터 이동 방향
chacracter_to_x = 0

#캐릭터 이동 속도
chacracter_speed = 5

#무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#무기는 한번에 여러개 발사 가능
weapons = []

#무기 이동 속도
weapon_speed = 10

running = True 
while running:
    dt = clock.tick(30) 

    #2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 

        if event.type == KEYDOWN:
            if event.key == pygame.K_LEFT: #캐릭터를 왼쪽으로
                chacracter_to_x -= chacracter_speed
            elif event.key == pygame.K_RIGHT: #캐릭터를 오른쪽으로
                chacracter_to_x += chacracter_speed
            elif event.key == pygame.K_SPACE: #무기 발사
                weapon_x_pos = chacracter_x_pos + (chacracter_width / 2) - (weapon_width / 2)
                weapon_y_pos = chacracter_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                chacracter_to_x = 0
        
    #3. 게임 캐릭터 위치 정의
    chacracter_x_pos += chacracter_to_x

    if chacracter_x_pos < 0:
        chacracter_x_pos = 0
    elif chacracter_x_pos > screen_width - chacracter_width:
        chacracter_x_pos = screen_width - chacracter_width

    #무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] #무기위치를 위로

    #천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    #4. 충돌 처리

    #5. 화면에 그리기
    screen.blit(background, (0,0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos,weapon_y_pos))

    screen.blit(stage, (0,screen_height - stage_height))
    screen.blit(chacracter, (chacracter_x_pos,chacracter_y_pos))
   
    pygame.display.update() 


pygame.quit()