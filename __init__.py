"""
Copyright (C) 2025 Amatsukast
Amatsukast@MAIL.COM

Created by Amatsukast

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

bl_info = {
    "name": "Origin Tools",
    "description": "Add-on to move object origin to Min/Max/Center of each axis",
    "author": "Amatsukast",
    "version": (1, 1, 6),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Origin Tools",
    "category": "Object",
}

if "bpy" in locals():
    import importlib

    importlib.reload(Origin_Tools)
    importlib.reload(translation)
else:
    from . import Origin_Tools
    from . import translation


def register():
    Origin_Tools.register()
    translation.register(__name__)


def unregister():
    Origin_Tools.unregister()
    translation.unregister(__name__)


if __name__ == "__main__":
    register()
