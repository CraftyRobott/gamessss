# Retro Bowl Scorebug Studio

A visual editor for designing custom Retro Bowl scorebugs and exporting executable JavaScript mods for the Retro Bowl College mod loader.

## Browser editor (new)

The browser-based editor is available at **[Open Scorebug Studio](https://craftyrobott.github.io/gamessss/)** after the pull request is merged and GitHub Pages is enabled for `main` / root (Settings → Pages → Deploy from a branch).

You can also run it locally by opening `index.html` in a modern browser. There is no build step. The editor uses **Lilita One** as a browser-preview stand-in; it is not the game's proprietary font.

### Browser editor features

- Visual canvas with zoom, grid, snapping, safe-area guides, and adjustable dimensions
- Rectangle, rounded rectangle, ellipse, line, freehand pen, text, and image layers
- Solid fills, linear gradients, radial gradients, gradient angle and midpoint controls
- Layer visibility and lock toggles, multi-select, grouping, duplicate, delete, and z-order controls
- Drag to move, resize handles, keyboard nudging, alignment, and proportional canvas positioning
- Text styling, preview font, size, weight, alignment, letter spacing, line height, and dynamic game-data tokens
- Score count-up animation settings for selected Away/Home score layers: enable/disable, duration, count style, easing, and an in-editor preview
- Opacity, stroke, shadows, and per-layer styling
- Undo/redo history and keyboard shortcuts
- Import existing Studio JSON projects; export editable JSON, a design specification, or an executable game mod

**Game mod export:** Use **Export Game Mod** to download `custom_scorebug.js`. Put that file in `engine/mods/` in your Retro Bowl College installation and let the existing mod loader discover it. The mod waits for the game's `gml_Script_s_draw_scoreboard` function, then replaces the default scoreboard drawing with the exported layout. Use **Export spec** only when you want the editable design data; that file is not a game mod.

The generated runtime mod currently supports text/tokens, solid rectangles, ellipses, lines, freehand strokes, team-uniform colors and shades, and score count-up settings. The exported mod explicitly selects the game's `global.gmlfnt_small_flex` HUD font, matching the font used by the original scoreboard. Text scaling follows the game's HD/non-HD font behavior and is kept separate from the scorebug geometry scale. The editor preview still uses Lilita One as a stand-in, so browser typography will not be pixel-identical to the game. Rounded rectangles currently render as regular rectangles, gradients render as their base fill color, and imported image layers are skipped with a console warning. Test in your specific Retro Bowl College build; this exporter targets the scoreboard hook and drawing functions found in the supplied game source and is not guaranteed compatible with other versions.

## Desktop editor

The original Python/Tkinter editor remains available:

```powershell
py -3 retro_bowl_scorebug_studio.py
```

Requires Python 3 with Tkinter (included with the standard Windows Python installer).

The desktop editor includes a 732 × 338 scorebug canvas, dynamic game-data tokens, team-linked uniform colors, multi-selection, alignment, distribution, and JavaScript mod export.

## Project compatibility

The browser editor imports the existing `RetroBowlScorebugStudio` JSON format and keeps the existing dynamic token names such as `{away_score}`, `{home_score}`, `{clock}`, `{quarter}`, and `{down_distance}`.
