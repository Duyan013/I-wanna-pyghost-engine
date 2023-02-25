import pygame
import pyghost as wanna
from pyghost import imgs
from typing import Union
import os


def nested(outside: tuple[tuple[int, int], Union[str, tuple[int, int, int]]],
           inside: tuple[tuple[int, int],  Union[str, tuple[int, int, int]]],
           pos: tuple[int, int], color: Union[str, tuple[int, int, int]]) \
        -> pygame.Surface:  # 生成透明的嵌套图片
    frame = pygame.Surface(outside[0])
    frame.fill(outside[1])
    buff = pygame.Surface(inside[0])
    buff.fill(inside[1])
    frame.blit(buff, pos)
    frame.set_colorkey(color)
    return frame


def resources():  # 加载测试的默认图片
    imgs['horizontal'] = pygame.Surface((25*32, 32)).convert()
    imgs['vertical'] = pygame.Surface((32, 19*32)).convert()
    imgs['frame'] = nested(((32, 32), 'black'), ((
        30, 30), 'white'), (1, 1), 'white').convert()
    imgs['mask'] = nested(((32, 32), 'white'), ((
        14, 21), 'black'), (9, 11), 'white').convert()

    for i in ['other', 'rooms', 'kid', 'spike']:
        for j in os.listdir(os.path.join('ghost', i)):
            imgs[os.path.splitext(j)[0]] = pygame.image.load(
                os.path.join('ghost', i, j)).convert_alpha()

    for k, v in list(imgs.items()):
        if k[-1].isdigit():
            imgs[f'{k[:-1]}r{k[-1]}'] = v
            imgs[f'{k[:-1]}l{k[-1]}'] = pygame.transform.flip(
                v, True, False)


def init():  # 初始化最好传给wanna.start
    print('I wanna create the Ghost')
    resources()
    gifs = {'fallr0': 'fallr1', 'falll0': 'falll1', 'fallr1': 'fallr0', 'falll1': 'falll0',
            'idler0': 'idler1', 'idlel0': 'idlel1', 'idler1': 'idler2', 'idlel1': 'idlel2',
            'idler2': 'idler3', 'idlel2': 'idlel3', 'idler3': 'idler0', 'idlel3': 'idlel0',
            'jumpr0': 'jumpr1', 'jumpl0': 'jumpl1', 'jumpr1': 'jumpr0', 'jumpl1': 'jumpl0',
            'runr0': 'runr1', 'runl0': 'runl1', 'runr1': 'runr2', 'runl1': 'runl2', 'runr2': 'runr3',
            'runl2': 'runl3', 'runr3': 'runr4', 'runl3': 'runl4', 'runr4': 'runr0', 'runl4': 'runl0',
            'slider0': 'slider1', 'slidel0': 'slidel1', 'slider1': 'slider0', 'slidel1': 'slidel0'}
    keys = {'jump': {pygame.K_SPACE, pygame.K_LSHIFT, pygame.K_RSHIFT},
            'left': {pygame.K_a, pygame.K_LEFT, pygame.K_KP_4},
            'right': {pygame.K_d, pygame.K_RIGHT, pygame.K_KP_6},
            'goal': {pygame.K_z, pygame.K_LCTRL, pygame.K_LALT, pygame.K_RALT, pygame.K_RCTRL}}

    wanna.layers = ['back', 'trigger', 'player', 'ghost']
    kid = wanna.Player('idler3', gifs, keys, touch={'back'}, clid='mask')
    back = wanna.Obj('room1', (0, 0), layer='back')
    save1 = wanna.Trigger('save', (24*32, 9*32),
                          [wanna.save], {}, {'ghost'})  # 出窍状态才能存档
    wanna.rooms.append(wanna.Room((0, 17*32), kid, [back, save1]))  # 默认重生位置
    wanna.room = 0  # 初始房间


# 帧数15 建议debug=True时计时用的是thread time，虽然cpu占用会高，但不会波动
@wanna.start(init, (25*32, 19*32), 'Ghost Engine Demo1', cps=30, debug=True)
def update(live: tuple[int, int], orders: list[wanna.Obj], pressed: tuple[int, ...], newindex: int) -> None:
    print(live)  # 一秒内多少帧和上一帧经过的毫秒数
    for i in orders:
        if isinstance(i, wanna.Player):
            print(i.pos)  # 打印kid坐标
    if pygame.K_RETURN in pressed and pressed.index(pygame.K_RETURN) >= newindex:
        print(pressed, newindex)  # >=newindex为这一帧刚按下
