#!/usr/bin/env python

# TMX example
# Written in 2014, 2016 by onpon4 <onpon4@riseup.net>
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

import sge
import xsge_tmx


DATA = os.path.join(os.path.dirname(__file__), "data")


class Game(sge.dsp.Game):

    def event_key_press(self, key, char):
        if key == "up":
            self.current_room.views[0].y -= 32
        elif key == "down":
            self.current_room.views[0].y += 32
        elif key == "left":
            self.current_room.views[0].x -= 32
        elif key == "right":
            self.current_room.views[0].x += 32
        elif key == "escape":
            self.end()

    def event_close(self):
        self.end()


Game(800, 600)
sge.game.start_room = xsge_tmx.load(os.path.join(DATA, "map.tmx"))


if __name__ == "__main__":
    sge.game.start()
