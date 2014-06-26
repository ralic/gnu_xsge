# The SGE Specification
# Written in 2012, 2013, 2014 by Julian Marchant <onpon4@riseup.net> 
# 
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty. 
# 
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

# INSTRUCTIONS FOR DEVELOPING AN IMPLEMENTATION: Replace  the notice
# above as well as the notices contained in other source files with your
# own copyright notice.  Recommended free  licenses are  the GNU General
# Public License, GNU Lesser General Public License, Expat License, or
# Apache License.

"""
This module provides functions related to the mouse input.

Many other mouse functionalities are provided through attributes of
:attr:`sge.game.mouse`:

- :attr:`sge.game.mouse.x` and :attr:`sge.game.mouse.y` indicate the
  position of the mouse relative to the room.  Set these attributes to
  change the position of the mouse.
- :attr:`sge.game.mouse.xvelocity`, :attr:`sge.game.mouse.yvelocity`,
  :attr:`sge.game.mouse.speed`, and
  :attr:`sge.game.mouse.move_direction` indicate the average movement of
  the mouse during the last 250 milliseconds.
- :attr:`sge.game.mouse.sprite` controls what the mouse cursor looks
  like.  Set to :const:`None` for the default mouse cursor.
- :attr:`sge.game.mouse.visible` controls whether or not the mouse
  cursor is visible.
"""

import sge


__all__ = ["get_pressed", "get_x", "get_y"]


def get_pressed(button):
    """Return whether or not a mouse button is pressed.

    See the documentation for :class:`sge.input.MouseButtonPress` for
    more information.

    """
    # TODO


def get_x():
    """Return the horizontal location of the mouse cursor.

    This function differs from :attr:`sge.game.mouse.x` in that the
    location returned is relative to the window, not the room.

    """
    # TODO


def get_y():
    """Return the vertical location of the mouse cursor.

    This function differs from :attr:`sge.game.mouse.y` in that the
    location returned is relative to the window, not the room.

    """
    # TODO
