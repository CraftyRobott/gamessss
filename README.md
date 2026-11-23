# Retro Bowl Scorebug Studio

A Python/Tkinter editor for designing custom Retro Bowl scorebugs and exporting them as JavaScript mods.

## Run

Requires Python 3 with Tkinter available (included with the standard Windows Python installer).

```powershell
py -3 retro_bowl_scorebug_studio.py
```

## Features

- Visual 732 × 338 scorebug canvas with zoom, grid display, and grid snapping
- Editable text, rectangles, rounded rectangles, ellipses, and lines
- Dynamic game-data tokens for scores, team names, records, clock, quarter, and down/distance
- Team-linked uniform colors
- Save and open scorebug project JSON files
- Export a JavaScript scorebug mod
- Multi-select layers with Ctrl/Shift selection
- Drag selected layers together
- Align selected layers by left, horizontal center, right, top, vertical center, or bottom
- Align the selection to the canvas edges or center
- Distribute three or more selected layers horizontally or vertically

The property inspector edits the primary selected layer. Alignment, distribution, deletion, and dragging can operate on multiple selected layers.
