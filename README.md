# Origin Tools

[English](README.md) | [日本語](README_JP.md)

## Overview

In Blender, adjusting the origin position of objects is an unavoidable step during modeling and scene layout. However, relying solely on standard features to accurately align the origin to specific edges or faces often requires multiple steps, such as moving the 3D cursor, which can interrupt your creative flow.

**Origin Tools** is a Blender add-on designed to eliminate the frustration associated with origin adjustment, allowing you to snap the origin to your desired location with just a few clicks. It works flawlessly even with applied transform values (location, rotation, scale) and complex parenting hierarchies. It also supports batch processing of multiple objects simultaneously, significantly enhancing workflow efficiency for intermediate to advanced users.

<img src="images/UI_EN.webp" width="35%">

## Installation

1. Download the ZIP file from the [Releases] page of the GitHub repository, or via `Code > Download ZIP`.
2. Open Blender and go to `Edit > Preferences`.
3. Select the `Add-ons` tab, click on the top-right arrow icon and select `Install from Disk...` (or just `Install`), then select the downloaded ZIP file.
4. Check the box next to `Origin Tools` to enable the add-on.

## Panel Location

Once enabled, a dedicated UI panel is added to the 3D Viewport's Sidebar (N-key) under the `Origin Tools` tab.

## Key Features

Origin Tools' functions are consolidated into a simple UI in the sidebar. Details of each function and option are as follows:

### Basic Operations and Options

| Feature/Option            | Description                                                                                                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **X / Y / Z Axis Move**   | Moves the origin along the specified axis to the Min, Center, or Max of the bounding box.                                                                                  |
| **Center (All Axes)**     | Moves the origin to the center of the bounding box across all axes simultaneously.                                                                                         |
| **Local / Global Toggle** | Choose whether to base operations on the object's Local axes or the World's Global axes.                                                                                   |
| **Move Mesh**             | Moves the mesh itself instead of the origin to match the specified position. Highly effective when you want to maintain the object's origin location in world coordinates. |
| **Center Before Move**    | An option that automatically resets the origin to the center of all axes before moving to the specified Min or Max position on a specific axis.                            |

### Edit Mode Exclusive: Origin to Face

**Origin to Face** is a powerful feature available only in Edit Mode.
When you select a specific face of a mesh and press this button, the following processes occur automatically:

1. The object's origin moves to the center of the selected face.
2. The entire object is rotated so that the selected face's normal points downwards towards the world's -Z direction.

_For objects with applied rotation:_

- The origin assumes the position and angle of the selected face.
- Clearing the transform rotation (`Alt+R`) will straighten the face.

|                   1. Face Selection                    |                                2. Result (Auto Rotation)                                 |                       3. Clear Rotation (`Alt+R`)                       |
| :----------------------------------------------------: | :--------------------------------------------------------------------------------------: | :---------------------------------------------------------------------: |
| <img src="images/origin_to_face_01.webp" width="100%"> |                  <img src="images/origin_to_face_02.webp" width="100%">                  |         <img src="images/origin_to_face_03.webp" width="100%">          |
|    Select any face and execute<br>`Origin to Face`.    | Origin moves to the face center, and the<br>object rotates so the face points down (-Z). | Clearing rotation straightens the<br>object based on the selected face. |

This feature makes it extremely easy to level tilted faces parallel to the ground, or to create assets based on their connection surfaces.

## Practical Use Cases

Origin Tools truly shines in everyday workflows like the following:

- **Grounding Assets**
  When you need to accurately place furniture or characters on the floor, simply pressing the Z-axis Min button sets the origin to the lowest point of the object. Then, just set the Z-coordinate to 0 for perfect grounding.
- **Optimizing Rotation Axes and Scale Origins**
  For door hinges or parts you want to scale in only one direction, you can instantly create the intended transform origin using the X or Y axis Min/Max buttons. Since you can process multiple selected objects simultaneously, organizing origins for large groups of parts takes only a moment.
- **Standardizing Kitbash Parts**
  When saving modeled details as kitbash assets, using the `Origin to Face` feature to orient the attachment face downwards (-Z direction) dramatically smooths out placement using snapping features later.

## Requirements and Languages

- **Blender Version**: Blender 4.2 or newer.
- **Languages**: Default is English UI, but automatically switches to Japanese UI if Blender's language setting is Japanese.

## License

[GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.html)  
Copyright (C) 2025 Amatsukast
