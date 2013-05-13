#!/usr/bin/env python

# Copyright (C) 2013 Julian Marchant <onpon4@lavabit.com>
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

"""1945

A scrolling shooter in the style of 1943.

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import math

import sge


class glob(object):

    player = None
    lives = 3
    score = 0

    music = None


class Game(sge.Game):

    def event_key_press(self, key):
        if key == 'escape':
            self.end()
        elif key == 'p':
            self.pause()

    def event_close(self):
        self.end()

    def event_paused_key_press(self, key):
        if key == 'escape':
            self.end()
        else:
            self.unpause()

    def event_paused_close(self):
        self.end()


class Player(sge.StellarClass):

    def __init__(self):
        self.up_key = 'up'
        self.down_key = 'down'
        self.left_key = 'left'
        self.right_key = 'right'
        x = sge.game.width / 2
        y = sge.game.height - 64
        glob.player = self
        super(Player, self).__init__(x, y, 10, 'player', '1945_playerplane',
                                     collision_precise=True)

    def event_create(self):
        self.can_shoot = True
        self.upgrade_level = 0
        self.shield = 10
        self.exploding = False

    def event_step(self, time_passed):
        self.xvelocity = (sge.get_key_pressed(self.right_key) -
                          sge.get_key_pressed(self.left_key)) * 6
        self.yvelocity = (sge.get_key_pressed(self.down_key) -
                          sge.get_key_pressed(self.up_key))

        if self.bbox_left < 0:
            self.bbox_left = 0
        elif self.bbox_right > sge.game.width:
            self.bbox_right = sge.game.width
        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom > sge.game.height:
            self.bbox_bottom = sge.game.height

        if self.can_shoot and sge.get_key_pressed('space'):
            self.shoot()

    def event_key_press(self, key):
        if key == 'space':
            # can_shoot is ignored, allowing a player to shoot faster by
            # pressing the space bar repeatedly.
            self.shoot()

    def event_alarm(self, alarm_id):
        if alarm_id == 'shoot':
            self.can_shoot = True

    def event_collision(self, other):
        if not self.exploding:
            if isinstance(other, Enemy):
                self.hurt()
                other.kill()

    def event_animation_end(self):
        if self.exploding:
            self.exploding = False
            self.sprite = '1945_playerplane'
            self.x = self.xstart
            self.y = self.ystart
            self.shield = 10

    def shoot(self):
        self.can_shoot = False
        self.set_alarm('shoot', 30)

        sge.create_object(PlayerBullet, self.x - 5, self.y, 0)
        sge.create_object(PlayerBullet, self.x + 5, self.y, 0)

        if self.upgrade_level >= 1:
            sge.create_object(PlayerBullet, self.x, self.y, 90)
            sge.create_object(PlayerBullet, self.x, self.y, -90)

        if self.upgrade_level >= 2:
            sge.create_object(PlayerBullet, self.x, self.y, 180)

        if self.upgrade_level >= 3:
            sge.create_object(PlayerBullet, self.x, self.y, 45)
            sge.create_object(PlayerBullet, self.x, self.y, -45)

    def hurt(self):
        if self.shield > 0:
            self.shield -= 1
        else:
            self.kill()

    def kill(self):
        if self.lives > 0:
            self.lives -= 1
            self.exploding = True
            self.sprite = '1945_explosion_large'
            self.image_index = 0
        else:
            # TODO: game over
            pass


class PlayerBullet(sge.StellarClass):

    def __init__(self, x, y, rotation=0):
        super(PlayerBullet, self).__init__(x, y, 3, sprite='1945_playerbullet',
                                           collision_precise=True)
        self.speed = 12
        self.move_direction = rotation + 90
        self.image_rotation = rotation


class Enemy(sge.StellarClass):

    def kill(self):
        self.destroy()


class EnemyBullet(Enemy):

    def __init__(self, x, y, xvelocity=0, yvelocity=12):
        super(EnemyBullet, self).__init__(x, y, 2, sprite='1945_enemybullet',
                                          collision_precise=True)


class EnemyPlane(Enemy):

    sprite_normal = "1945_enemyplane_green"
    sprite_flipping = "1945_enemyplane_green_flip"
    sprite_flipped = "1945_enemyplane_green_flipped"
    retreats = True
    follows_player = False
    directional_guns = False
    shoot_delay = 90

    def __init__(self, x, y):
        super(EnemyPlane, self).__init__(x, y, 5, sprite=self.sprite_normal,
                                         collision_precise=True, yvelocity=8)

    def retreat(self):
        self.retreating = True
        self.turning = True
        self.sprite = self.sprite_flipping
        self.image_index = 0
        self.image_rotation = 0
        self.xvelocity = 0
        self.yvelocity = 0

    def event_create(self):
        self.retreating = False
        self.turning = False
        self.set_alarm('shoot', self.shoot_delay)

    def event_step(self, time_passed):
        if not self.retreating:
            if self.retreats and self.y >= game.height - 32:
                self.retreat()
            elif self.follows_player:
                if self.y < glob.player.y and self.x != glob.player.x:
                    d = (glob.player.x - self.x) / abs(glob.player.x - self.x)
                    self.image_rotation = 45 * d
                    angle = math.radians(self.image_rotation + 270)
                    self.xvelocity = math.cos(angle) * 8
                    self.yvelocity = math.sin(angle) * 8
                else:
                    self.image_rotation = 0
                    self.xvelocity = 0
                    self.yvelocity = 8

    def event_alarm(self, alarm_id):
        if alarm.id == 'shoot':
            self.shoot()
            self.set_alarm('shoot', self.shoot_delay)

    def event_animation_end(self):
        if self.turning:
            self.turning = False
            self.sprite = self.sprite_flipped
            self.image_index = 0
            self.yvelocity = -8

    def shoot(self):
        if self.directional_guns:
            xdistance = glob.player.x - self.x
            ydistance = glob.player.y - self.y
            h = math.sqrt(xdistance ** 2 + ydistance ** 2)
            xvelocity = 12 * xdistance / h
            yvelocity = 12 * ydistance / h
        else:
            xvelocity = 0
            yvelocity = 12

        EnemyBullet.create(self.x, self.y, xvelocity, yvelocity)

    def kill(self):
        SmallExplosion.create(self.x, self.y)
        self.destroy()


class Kamikaze(EnemyPlane):

    sprite_normal = "1945_enemyplane_orange"
    retreats = False
    follows_player = True
    directional_guns = False
    shoot_delay = None


class Coward(EnemyPlane):

    sprite_normal = "1945_enemyplane_orange"
    retreats = True
    follows_player = False
    directional_guns = True


class Follower(EnemyPlane):

    sprite_normal = "1945_enemyplane_orange"
    retreats = True
    follows_player = True
    directional_guns = False
    shoot_delay = 60


class Chaser(EnemyPlane):

    sprite_normal = "1945_enemyplane_orange"
    retreats = True
    follows_player = True
    directional_guns = True
    shoot_delay = 45


class SmallExplosion(sge.StellarClass):

    def __init__(self, x, y):
        super(SmallExplosion, self).__init__(
            x, y, 5, sprite="1945_explosion_small", detects_collisions=False)

    def event_animation_end(self):
        self.destroy()


def main():
    # Create Game object
    Game(480, 800)

    # Load sprites
    sge.Sprite('1945_enemybullet.png', origin_x=3, origin_y=3,
               transparent=True, bbox_x=-3, bbox_y=-3)
    sge.Sprite('1945_enemyplane_blue', origin_x=16, origin_y=16,
               transparent=True, fps=4, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_blue_flip', origin_x=16, origin_y=16,
               transparent=True, fps=6, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_blue_flipped', origin_x=16, origin_y=16,
               transparent=True, fps=4, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_dkgreen', origin_x=16, origin_y=16,
               transparent=True, fps=4, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_dkgreen_flip', origin_x=16, origin_y=16,
               transparent=True, fps=6, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_dkgreen_flipped', origin_x=16, origin_y=16,
               transparent=True, fps=4, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_green', origin_x=16, origin_y=16,
               transparent=True, fps=4, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_green_flip', origin_x=16, origin_y=16,
               transparent=True, fps=6, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_green_flipped', origin_x=16, origin_y=16,
               transparent=True, fps=4, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_orange', origin_x=16, origin_y=16,
               transparent=True, fps=4, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_white', origin_x=16, origin_y=16,
               transparent=True, fps=4, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_white_flip', origin_x=16, origin_y=16,
               transparent=True, fps=6, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_enemyplane_white_flipped', origin_x=16, origin_y=16,
               transparent=True, fps=4, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_explosion_large', origin_x=32, origin_y=23,
               transparent=True, fps=5)
    sge.Sprite('1945_explosion_small', origin_x=16, origin_y=16,
               transparent=True, fps=6)
    sge.Sprite('1945_friendlyplane', origin_x=16, origin_y=16,
               transparent=True, fps=4, bbox_x=-16, bbox_y=-16)
    sge.Sprite('1945_gameover', origin_x=97, origin_y=6, transparent=True,
               fps=4)
    sge.Sprite('1945_getready', origin_x=98, origin_y=6, transparent=True,
               fps=4)
    sge.Sprite('1945_hud', transparent=True)
    sge.Sprite('1945_hud_life', origin_x=13, origin_y=10, transparent=True,
               bbox_x=-13, bbox_y=-10)
    sge.Sprite('1945_hud_shieldbar')
    sge.Sprite('1945_islands', origin_x=32, origin_y=32, transparent=True,
               fps=0)
    sge.Sprite('1945_main_menu', transparent=True)
    sge.Sprite('1945_numbers', transparent=True, fps=0)
    sge.Sprite('1945_playerbullet', origin_x=3, origin_y=8, transparent=True,
               bbox_x=-3, bbox_y=-8)
    sge.Sprite('1945_playerplane', origin_x=29, origin_y=12, transparent=True,
               fps=4, bbox_x=-29, bbox_y=-12)
    sge.Sprite('1945_powerup_backguns', origin_x=16, origin_y=10,
               transparent=True, bbox_x=-16, bbox_y=-10)
    sge.Sprite('1945_powerup_backup', origin_x=15, origin_y=7,
               transparent=True, bbox_x=-15, bbox_y=-7)
    sge.Sprite('1945_powerup_bomb', origin_x=5, origin_y=11, transparent=True,
               bbox_x=-5, bbox_y=-11)
    sge.Sprite('1945_powerup_extralife', origin_x=11, origin_y=9,
               transparent=True, bbox_x=-11, bbox_y=-9)
    sge.Sprite('1945_powerup_shield', origin_x=10, origin_y=14,
               transparent=True, bbox_x=-10, bbox_y=-14)
    sge.Sprite('1945_powerup_sideguns', origin_x=16, origin_y=7,
               transparent=True, bbox_x=-16, bbox_y=-7)
    sge.Sprite('1945_powerup_spreadguns', origin_x=16, origin_y=12,
               transparent=True, bbox_x=-16, bbox_y=-12)
    sge.Sprite('1945_selection_arrow', origin_x=6, origin_y=6,
               transparent=True)
    sge.Sprite('1945_title')
    sge.Sprite('1945_water')

    # Load backgrounds
    water_layer = sge.BackgroundLayer('1945_water', 0, 0, -10000)
    layers = (water_layer,)
    background = sge.Background(layers, "#083681")

    # Load sounds
    #TODO

    # Load music
    glob.music = sge.Music("DST-TowerDefenseTheme.ogg")

    # Create objects
    #TODO
    objects = ()

    # Create rooms
    sge.Room(objects, background=background)

    sge.game.start()


if __name__ == '__main__':
    main()
