# Retro Bowl Scorebug Studio

A visual editor for designing custom Retro Bowl scorebugs and exporting structured JavaScript specifications for conversion into game mods.

## Browser editor (new)

The browser-based editor is available at **[Open Scorebug Studio](https://craftyrobott.github.io/gamessss/)** after the pull request is merged and GitHub Pages is enabled for `main` / root (Settings → Pages → Deploy from a branch).

You can also run it locally by opening `index.html` in a modern browser. There is no build step; the Retro Bowl-inspired **Lilita One** typeface is loaded from Google Fonts, so the font requires an internet connection.

### Browser editor features

- Visual canvas with zoom, grid, snapping, safe-area guides, and adjustable dimensions
- Rectangle, rounded rectangle, ellipse, line, freehand pen, text, and image layers
- Solid fills, linear gradients, radial gradients, gradient angle and midpoint controls
- Layer visibility and lock toggles, multi-select, grouping, duplicate, delete, and z-order controls
- Drag to move, resize handles, keyboard nudging, alignment, and proportional canvas positioning
- Text styling, font family, size, weight, alignment, letter spacing, line height, and dynamic game-data tokens
- Score count-up animation settings for selected Away/Home score layers: enable/disable, duration, count style, easing, and an in-editor preview
- Opacity, stroke, shadows, and per-layer styling
- Undo/redo history and keyboard shortcuts
- Import existing Studio JSON projects; export editable JSON or a JavaScript design specification

**Export note:** The JavaScript export is a design specification, not yet a fully generated Retro Bowl runtime mod. It preserves the design details (including gradients, layers, and per-score animation settings) so they can be translated into the game's drawing API without guessing from screenshots. The browser editor uses Lilita One as a close visual match; it does not redistribute a proprietary game font file.

## Desktop editor

The original Python/Tkinter editor remains available:

```powershell
py -3 retro_bowl_scorebug_studio.py
```

Requires Python 3 with Tkinter (included with the standard Windows Python installer).

The desktop editor includes a 732 × 338 scorebug canvas, dynamic game-data tokens, team-linked uniform colors, multi-selection, alignment, distribution, and JavaScript mod export.

## Project compatibility

The browser editor imports the existing `RetroBowlScorebugStudio` JSON format and keeps the existing dynamic token names such as `{away_score}`, `{home_score}`, `{clock}`, `{quarter}`, and `{down_distance}`.
