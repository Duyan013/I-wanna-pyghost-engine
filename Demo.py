import pyghost as wanna
import pygame
import os


def loadimgs():  # 这个是测试时加载的图片，都是除了room，其他都是32*32
    wanna.imgs['mask'] = pygame.image.load('ghost/kid/Mask.png')
    wanna.imgs['save'] = pygame.image.load('ghost/other/Save.png')
    wanna.imgs['room'] = pygame.image.load('ghost/rooms/Room.png')
    animate: dict[str, str] = {}
    for i in ['idle', 'run', 'jump', 'fall']:
        for j in enumerate(wanna.addrs['kid'][i]):
            animate[f'{i}r{j[0]}'] = f'{i}r{(j[0]+1)%len(wanna.addrs["kid"][i])}'
            wanna.imgs[f'{i}r{j[0]}'] = pygame.image.load(os.path.join(
                'ghost', 'kid', j[1]))
            animate[f'{i}l{j[0]}'] = f'{i}l{(j[0]+1)%len(wanna.addrs["kid"][i])}'
            wanna.imgs[f'{i}l{j[0]}'] = pygame.transform.flip(
                wanna.imgs[f'{i}r{j[0]}'], True, False)
    return animate


def init():  # 初始化最好传给wanna.start
    print('i wanna create the ghost')
    wanna.layers.extend(['test', 'player'])
    kid = wanna.Player('idler3', loadimgs(), layer='player',
                       touch={'test'}, clid='mask')
    test = wanna.Obj('room', (0, 0), layer='test')

    def spawn(self: wanna.Trigger, hits: set[wanna.Obj]):
        if len(hits) != 1 or kid not in hits:
            return
        buff = (wanna.room, kid.pos)  # 当前房间号和坐标
        if wanna.saves[-1][0] != buff[0] or not self.mask.overlap(kid.mask,  # 同一房间同一个记录点不多次保存
                                                                  (wanna.saves[-1][1][0]-self.pos[0],
                                                                   wanna.saves[-1][1][1]-self.pos[1])):
            wanna.saves.append(buff)
        else:
            wanna.saves[-1] = buff  # 一个存档只保存最后一个位置
        print(f'已保存坐标{kid.pos}')
        self.state -= 1  # 存档可反复调用，一次性机关设置为0，如果不设置，离开后还会调用

    save1 = wanna.Trigger('save', (24*32, 9*32), touch={
                          'player'}, affairs=[spawn])
    wanna.rooms.append(wanna.Room((0, 17*32), kid, [test, save1]))  # 默认重生位置
    wanna.room = 0  # 初始房间


# 帧数15 建议debug=True时计时用的是thread time，虽然cpu占用会高，但不会波动
@wanna.start(init, (25*32, 19*32), 'Ghost Engine Demo', cps=15, debug=True)
def update(live: tuple[int, int], orders: list[wanna.Obj], pressed: tuple[int, ...], newindex: int) -> None:
    print(live)  # 一秒内多少帧和上一帧经过的毫秒数
    for i in orders:
        if isinstance(i, wanna.Player):
            print(i.pos)  # 打印kid坐标
    if pygame.K_RETURN in pressed and pressed.index(pygame.K_RETURN) >= newindex:
        print(pressed, newindex)  # >=newindex为这一帧刚按下
