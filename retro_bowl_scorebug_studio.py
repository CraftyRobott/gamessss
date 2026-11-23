
import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import json
import os
import re
W, H = 732, 338
TOKENS = [
    "{away_score}", "{home_score}", "{away_name}", "{home_name}",
    "{away_abbr}", "{home_abbr}", "{away_rank}", "{home_rank}",
    "{away_record}", "{home_record}", "{away_wins}", "{away_losses}",
    "{home_wins}", "{home_losses}", "{clock}", "{quarter}",
    "{down_distance}", "{timeouts}", "{away_timeouts}",
    "{home_timeouts}", "{possession}"
]
MODES = [
    "Fixed color", "Away team", "Home team",
    "Away lighter", "Home lighter",
    "Away darker", "Home darker"
]
SAMPLE = {
    "away_score": "24",
    "home_score": "21",
    "away_name": "TENNESSEE",
    "home_name": "ALABAMA",
    "away_abbr": "TENN",
    "home_abbr": "BAMA",
    "away_rank": "#8",
    "home_rank": "#3",
    "away_record": "8-2",
    "home_record": "9-1",
    "away_wins": "8",
    "away_losses": "2",
    "home_wins": "9",
    "home_losses": "1",
    "clock": "2:41",
    "quarter": "4TH",
    "down_distance": "3RD & 6",
    "timeouts": "2/1",
    "away_timeouts": "2",
    "home_timeouts": "1",
    "possession": "AWAY",
    "away_color": "#FF8200",
    "home_color": "#9E1B32"
}
DEFAULT = [
    {
        "type": "rect", "name": "Main background",
        "x": 95, "y": 222, "w": 542, "h": 76,
        "fill": "#101B2D", "fill_mode": "Fixed color",
        "outline": "#101B2D", "width": 0, "alpha": .96
    },
    {
        "type": "rect", "name": "Away panel",
        "x": 95, "y": 222, "w": 210, "h": 76,
        "fill": "#344E72", "fill_mode": "Away team",
        "outline": "#344E72", "width": 0, "alpha": 1
    },
    {
        "type": "rect", "name": "Home panel",
        "x": 427, "y": 222, "w": 210, "h": 76,
        "fill": "#7B3030", "fill_mode": "Home team",
        "outline": "#7B3030", "width": 0, "alpha": 1
    },
    {
        "type": "text", "name": "Away name / rank",
        "x": 112, "y": 201, "w": 180, "h": 24,
        "text": "{away_rank} {away_name}",
        "color": "#FFFFFF", "color_mode": "Fixed color",
        "font_scale": 1, "align": "left", "alpha": 1
    },
    {
        "type": "text", "name": "Home name / rank",
        "x": 620, "y": 201, "w": 180, "h": 24,
        "text": "{home_rank} {home_name}",
        "color": "#FFFFFF", "color_mode": "Fixed color",
        "font_scale": 1, "align": "right", "alpha": 1
    },
    {
        "type": "text", "name": "Away score",
        "x": 274, "y": 260, "w": 40, "h": 30,
        "text": "{away_score}", "color": "#FFFFFF",
        "color_mode": "Fixed color", "font_scale": 1.7,
        "align": "center", "alpha": 1
    },
    {
        "type": "text", "name": "Home score",
        "x": 458, "y": 260, "w": 40, "h": 30,
        "text": "{home_score}", "color": "#FFFFFF",
        "color_mode": "Fixed color", "font_scale": 1.7,
        "align": "center", "alpha": 1
    },
    {
        "type": "text", "name": "Away record",
        "x": 210, "y": 260, "w": 60, "h": 22,
        "text": "{away_record}", "color": "#FFFFFF",
        "color_mode": "Fixed color", "font_scale": .65,
        "align": "center", "alpha": 1
    },
    {
        "type": "text", "name": "Home record",
        "x": 500, "y": 260, "w": 60, "h": 22,
        "text": "{home_record}", "color": "#FFFFFF",
        "color_mode": "Fixed color", "font_scale": .65,
        "align": "center", "alpha": 1
    },
    {
        "type": "text", "name": "Clock",
        "x": 366, "y": 248, "w": 80, "h": 22,
        "text": "{clock}", "color": "#FFFFFF",
        "color_mode": "Fixed color", "font_scale": 1,
        "align": "center", "alpha": 1
    },
    {
        "type": "text", "name": "Quarter",
        "x": 366, "y": 276, "w": 80, "h": 20,
        "text": "{quarter}", "color": "#D8D8D8",
        "color_mode": "Fixed color", "font_scale": .75,
        "align": "center", "alpha": 1
    },
    {
        "type": "text", "name": "Down & distance",
        "x": 366, "y": 218, "w": 130, "h": 20,
        "text": "{down_distance}", "color": "#D8D8D8",
        "color_mode": "Fixed color", "font_scale": .8,
        "align": "center", "alpha": 1
    }
]
def rgb(h):
    s = str(h).replace("#", "").replace("$", "")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", s):
        return (255, 255, 255)
    return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
def shade(h, a):
    c = rgb(h)
    return "#" + "".join(
        "%02X" % round(v + (255-v)*a if a >= 0 else v*(1+a))
        for v in c
    )
def generate_js(elements, title):
    layout = json.dumps(
        elements,
        separators=(",", ":"),
        ensure_ascii=False
    )
    return r"""// @name """ + title + r"""
// @description Custom scorebug created with Retro Bowl Scorebug Studio.
// @category presentation
(function(){
"use strict";
if(window.__scorebugStudioInstalled)return;
window.__scorebugStudioInstalled=true;
var LAYOUT=""" + layout + r""";
var attempts=0,timer=null;
function get(team,key,fallback){
 try{
  var v=ds_map_find_value(team,key);
  return v==null?fallback:v;
 }catch(e){
  return fallback;
 }
}
function shirt(inst,other,team){
 try{
  var h=String(get(team,"colshirt","777777")).replace(/^[$#]/,"");
  if(!/^[0-9a-fA-F]{6}$/.test(h))throw Error("invalid colshirt");
  return gml_Script_s_rgb_to_bgr(
   inst,other,
   gml_Script_s_hex_string_to_col(inst,other,h)
  );
 }catch(e){
  return make_color_rgb(119,119,119);
 }
}
function shadeColor(c,a){
 var r=c&255,g=(c>>8)&255,b=(c>>16)&255;
 if(a>=0){
  r=Math.round(r+(255-r)*a);
  g=Math.round(g+(255-g)*a);
  b=Math.round(b+(255-b)*a);
 }else{
  r=Math.round(r*(1+a));
  g=Math.round(g*(1+a));
  b=Math.round(b*(1+a));
 }
 return r|(g<<8)|(b<<16);
}
function fixed(inst,other,h){
 try{
  return gml_Script_s_rgb_to_bgr(
   inst,other,
   gml_Script_s_hex_string_to_col(
    inst,other,String(h||"#FFFFFF").replace("#","")
   )
  );
 }catch(e){
  return make_color_rgb(255,255,255);
 }
}
function data(inst,other){
 var a=inst.gmlteam&&inst.gmlteam[0];
 var h=inst.gmlteam&&inst.gmlteam[1];
 var aw=get(a,"wins","0");
 var al=get(a,"losses","0");
 var hw=get(h,"wins","0");
 var hl=get(h,"losses","0");
 function rank(t){
  try{
   var sub=gml_Script_s_get_subdivision(inst,other,t);
   var uid=get(t,"uid",null);
   if(sub==null||Number(sub)<0||uid==null)return "";
   var n=Number(
    gml_Script_s_subdivision_get_team_ranking(inst,other,sub,uid)
   );
   return isFinite(n)&&n>=0&&n<25?"#"+(n+1):"";
  }catch(e){
   return "";
  }
 }
 var clock="",quarter="",down="",timeouts="";
 try{
  clock=String(
   gml_Script_s_get_string_time(
    inst,other,inst.gmlminutes,inst.gmlseconds
   )
  );
 }catch(e){}
 try{
  quarter=String(
   gml_Script_s_str(inst,other,"quarter_"+String(inst.gmlquarter))
  );
 }catch(e){}
 try{
  down=String(gml_Script_s_get_string_downand(inst,other));
 }catch(e){}
 try{
  timeouts=String(gml_Script_s_count_timeouts(inst,other));
 }catch(e){}
 return {
  away_score:String(inst.gmlteam_score?inst.gmlteam_score[0]:0),
  home_score:String(inst.gmlteam_score?inst.gmlteam_score[1]:0),
  away_name:String(get(a,"name","AWAY")),
  home_name:String(get(h,"name","HOME")),
  away_abbr:String(get(a,"tla","AWY")),
  home_abbr:String(get(h,"tla","HME")),
  away_rank:rank(a),
  home_rank:rank(h),
  away_record:String(aw)+"-"+String(al),
  home_record:String(hw)+"-"+String(hl),
  away_wins:String(aw),
  away_losses:String(al),
  home_wins:String(hw),
  home_losses:String(hl),
  clock:clock,
  quarter:quarter,
  down_distance:down,
  timeouts:timeouts,
  away_timeouts:"",
  home_timeouts:"",
  possession:"",
  _away:shirt(inst,other,a),
  _home:shirt(inst,other,h)
 };
}
function color(inst,other,mode,hex,d){
 if(mode==="Away team")return d._away;
 if(mode==="Home team")return d._home;
 if(mode==="Away lighter")return shadeColor(d._away,.35);
 if(mode==="Home lighter")return shadeColor(d._home,.35);
 if(mode==="Away darker")return shadeColor(d._away,-.35);
 if(mode==="Home darker")return shadeColor(d._home,-.35);
 return fixed(inst,other,hex);
}
function expand(s,d){
 return String(s||"").replace(
  /\{([a-z_]+)\}/gi,
  function(m,k){
   return d[k]===undefined?m:String(d[k]);
  }
 );
}
function draw(inst,other){
 if(global.gmldebug_aa_hide_ui)return;
 var w=display_get_gui_width();
 var h=display_get_gui_height();
 if(!(w>0&&h>0))return;
 var s=Math.min(w/732,h/338);
 var ox=(w-732*s)/2;
 var oy=(h-338*s)/2;
 var d=data(inst,other);
 for(var i=0;i<LAYOUT.length;i++){
  var e=LAYOUT[i];
  var x=ox+(+e.x||0)*s;
  var y=oy+(+e.y||0)*s;
  var ww=(+e.w||0)*s;
  var hh=(+e.h||0)*s;
  draw_set_alpha(
   Math.max(0,Math.min(1,e.alpha===undefined?1:+e.alpha))
  );
  if(e.type==="rect"||e.type==="roundrect"||e.type==="ellipse"){
   var c=color(inst,other,e.fill_mode,e.fill,d);
   draw_set_color(c);
   if(e.type==="ellipse"&&typeof draw_ellipse_colour==="function"){
    draw_ellipse_colour(x,y,x+ww,y+hh,c,c,0);
   }else if(e.type==="roundrect"&&typeof draw_roundrect_colour==="function"){
    draw_roundrect_colour(x,y,x+ww,y+hh,c,c,0);
   }else{
    draw_rectangle_colour(x,y,x+ww,y+hh,c,c,c,c,0);
   }
   if((+e.width||0)>0){
    var o=fixed(inst,other,e.outline);
    draw_set_color(o);
    if(e.type==="ellipse"&&typeof draw_ellipse_colour==="function"){
     draw_ellipse_colour(x,y,x+ww,y+hh,o,o,1);
    }else{
     draw_rectangle_colour(x,y,x+ww,y+hh,o,o,o,o,1);
    }
   }
  }else if(e.type==="line"){
   draw_set_color(fixed(inst,other,e.color));
   draw_line_width(
    x,y,x+ww,y+hh,
    Math.max(1,+e.width||1)*s
   );
  }else if(e.type==="text"){
   draw_set_color(color(inst,other,e.color_mode,e.color,d));
   draw_set_font(global.gmlfnt_small_flex);
   draw_set_halign(
    e.align==="left"?0:e.align==="right"?2:1
   );
   draw_set_valign(1);
   var fs=(global.gmlhd_fonts?.25:1)*(+e.font_scale||1)*s;
   draw_text_transformed(
    x,y,expand(e.text,d),fs,fs,0
   );
  }
 }
 draw_set_color(0xFFFFFF);
 draw_set_alpha(1);
 draw_set_halign(0);
 draw_set_valign(1);
}
function install(){
 var original=window.gml_Script_s_draw_scoreboard;
 if(typeof original!=="function"){
  if(++attempts>200)clearInterval(timer);
  return;
 }
 clearInterval(timer);
 window.gml_Script_s_draw_scoreboard=function(inst,other){
  try{
   draw(inst,other);
  }catch(e){
   if(!window.__scorebugStudioErr){
    window.__scorebugStudioErr=true;
    console.error("[Scorebug Studio]",e);
   }
  }
 };
 console.log("[Scorebug Studio] Custom scorebug installed.");
}
timer=setInterval(install,50);
install();
})();
"""
class Studio:
    def __init__(self, root):
        self.root = root
        root.title("Retro Bowl Scorebug Studio")
        root.geometry("1280x850")
        root.minsize(1080, 720)
        self.elements = json.loads(json.dumps(DEFAULT))
        self.selected = 0
        self.selected_indices = [0]
        self.sample = dict(SAMPLE)
        self.vars = {}
        self._ui()
        self.refresh_list()
        self.select(0)
    def _ui(self):
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill="x")
        ttk.Label(
            top,
            text="RETRO BOWL  /  SCOREBUG STUDIO",
            font=("Segoe UI", 16, "bold")
        ).pack(side="left")
        for label, fn in [
            ("New", self.new),
            ("Open", self.open),
            ("Save project", self.save),
            ("Import uniforms", self.import_uniforms),
            ("Export JS mod", self.export)
        ]:
            ttk.Button(
                top, text=label, command=fn
            ).pack(side="right", padx=3)
        pane = ttk.Panedwindow(
            self.root, orient="horizontal"
        )
        pane.pack(fill="both", expand=True, padx=8, pady=5)
        left = ttk.Frame(pane, padding=7)
        mid = ttk.Frame(pane, padding=7)
        right = ttk.Frame(pane, padding=7)
        pane.add(left, weight=1)
        pane.add(mid, weight=3)
        pane.add(right, weight=2)
        # LEFT: Layers
        ttk.Label(
            left,
            text="LAYERS / ELEMENTS",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")
        self.lb = tk.Listbox(
            left, height=20, exportselection=False,
            selectmode=tk.EXTENDED
        )
        self.lb.pack(fill="both", expand=True, pady=6)
        self.lb.bind("<<ListboxSelect>>", self.lb_select)
        r = ttk.Frame(left)
        r.pack(fill="x")
        self.kind = ttk.Combobox(
            r,
            values=[
                "Rectangle", "Rounded rectangle",
                "Ellipse", "Line", "Text"
            ],
            state="readonly",
            width=16
        )
        self.kind.set("Rectangle")
        self.kind.pack(side="left", fill="x", expand=True)
        ttk.Button(
            r, text="+ Add", command=self.add
        ).pack(side="left", padx=3)
        for label, fn in [
            ("Duplicate", self.duplicate),
            ("Delete", self.delete),
            ("Move up", lambda: self.move(-1)),
            ("Move down", lambda: self.move(1))
        ]:
            ttk.Button(left, text=label, command=fn).pack(fill="x", pady=2)

        align_box = ttk.LabelFrame(left, text="Align / Distribute", padding=5)
        align_box.pack(fill="x", pady=(7, 3))
        ttk.Label(align_box, text="Align selected layers").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 3)
        )
        for col, (label, mode) in enumerate([
            ("Left", "left"), ("H Center", "center_x"), ("Right", "right"),
            ("Top", "top"), ("V Center", "center_y"), ("Bottom", "bottom")
        ]):
            ttk.Button(align_box, text=label, width=9,
                       command=lambda m=mode: self.align_layers(m)).grid(
                row=1 + col // 3, column=col % 3, sticky="ew", padx=1, pady=1
            )
        ttk.Label(align_box, text="Align selection to canvas").grid(
            row=3, column=0, columnspan=3, sticky="w", pady=(6, 3)
        )
        for col, (label, mode) in enumerate([
            ("Left", "left"), ("Center X", "center_x"), ("Right", "right"),
            ("Top", "top"), ("Center Y", "center_y"), ("Bottom", "bottom"),
            ("Center Both", "center_both")
        ]):
            ttk.Button(align_box, text=label, width=9,
                       command=lambda m=mode: self.align_canvas(m)).grid(
                row=4 + col // 3, column=col % 3, sticky="ew", padx=1, pady=1
            )
        ttk.Label(align_box, text="Distribute selected layers").grid(
            row=7, column=0, columnspan=3, sticky="w", pady=(6, 3)
        )
        ttk.Button(align_box, text="Horizontal",
                   command=lambda: self.distribute("x")).grid(
            row=8, column=0, sticky="ew", padx=1, pady=1
        )
        ttk.Button(align_box, text="Vertical",
                   command=lambda: self.distribute("y")).grid(
            row=8, column=1, sticky="ew", padx=1, pady=1
        )
        for col in range(3):
            align_box.columnconfigure(col, weight=1)

        scale_box = ttk.LabelFrame(left, text="Proportional scale", padding=5)
        scale_box.pack(fill="x", pady=(4, 3))
        ttk.Label(
            scale_box,
            text="Scale selected layers together (%)"
        ).pack(anchor="w")
        scale_row = ttk.Frame(scale_box)
        scale_row.pack(fill="x", pady=(3, 0))
        self.scale_percent_var = tk.StringVar(value="100")
        ttk.Entry(
            scale_row, textvariable=self.scale_percent_var, width=7
        ).pack(side="left", padx=(0, 4))
        ttk.Button(
            scale_row, text="Apply", command=self.scale_selection
        ).pack(side="left", expand=True, fill="x")
        quick_row = ttk.Frame(scale_box)
        quick_row.pack(fill="x", pady=(3, 0))
        ttk.Button(
            quick_row, text="−10%", command=lambda: self.scale_by(0.9)
        ).pack(side="left", expand=True, fill="x", padx=(0, 2))
        ttk.Button(
            quick_row, text="+10%", command=lambda: self.scale_by(1.1)
        ).pack(side="left", expand=True, fill="x", padx=(2, 0))

        ttk.Label(
            left,
            text="Select one or more layers. Drag to move, or use Proportional scale to resize around the selection's center.",
            wraplength=230
        ).pack(anchor="w", pady=8)
        # CENTER: Preview
        ttk.Label(
            mid,
            text="LIVE PREVIEW  •  DESIGN CANVAS 732 × 338",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")
        gridbar = ttk.Frame(mid)
        gridbar.pack(fill="x", pady=(5, 0))
        self.snap_var = tk.BooleanVar(value=True)
        self.grid_visible_var = tk.BooleanVar(value=True)
        self.grid_size_var = tk.StringVar(value="10")
        ttk.Checkbutton(
            gridbar,
            text="Snap to grid",
            variable=self.snap_var,
            command=self.preview
        ).pack(side="left")
        ttk.Checkbutton(
            gridbar,
            text="Show grid",
            variable=self.grid_visible_var,
            command=self.preview
        ).pack(side="left", padx=(12, 4))
        ttk.Label(
            gridbar, text="Grid spacing:"
        ).pack(side="left", padx=(12, 3))
        grid_size = ttk.Combobox(
            gridbar,
            textvariable=self.grid_size_var,
            values=["2", "5", "10", "20", "40"],
            state="readonly",
            width=5
        )
        grid_size.pack(side="left")
        grid_size.bind(
            "<<ComboboxSelected>>",
            lambda _: self.preview()
        )
        # Zoom selector
        zoombar = ttk.Frame(mid)
        zoombar.pack(fill="x", pady=(5, 0))
        ttk.Label(
            zoombar, text="Preview zoom:"
        ).pack(side="left")
        self.zoom_var = tk.StringVar(value="100%")
        zoom_box = ttk.Combobox(
            zoombar,
            textvariable=self.zoom_var,
            values=[
                "50%", "75%", "100%", "125%",
                "150%", "175%", "200%", "250%", "300%"
            ],
            state="readonly",
            width=7
        )
        zoom_box.pack(side="left", padx=5)
        zoom_box.bind(
            "<<ComboboxSelected>>",
            lambda _: self.preview()
        )
        # Scrollable preview canvas
        self.preview_frame = ttk.Frame(mid)
        self.preview_frame.pack(
            fill="both", expand=True, pady=8
        )
        self.cv = tk.Canvas(
            self.preview_frame,
            bg="#18212e",
            highlightthickness=1,
            highlightbackground="#64748b"
        )
        self.hscroll = ttk.Scrollbar(
            self.preview_frame,
            orient="horizontal",
            command=self.cv.xview
        )
        self.vscroll = ttk.Scrollbar(
            self.preview_frame,
            orient="vertical",
            command=self.cv.yview
        )
        self.cv.configure(
            xscrollcommand=self.hscroll.set,
            yscrollcommand=self.vscroll.set
        )
        self.cv.grid(row=0, column=0, sticky="nsew")
        self.vscroll.grid(row=0, column=1, sticky="ns")
        self.hscroll.grid(row=1, column=0, sticky="ew")
        self.preview_frame.rowconfigure(0, weight=1)
        self.preview_frame.columnconfigure(0, weight=1)
        self.cv.bind("<Button-1>", self.down)
        self.cv.bind("<B1-Motion>", self.drag)
        # Sample data editor
        box = ttk.LabelFrame(
            mid,
            text="Sample game data — edit to preview live fields",
            padding=6
        )
        box.pack(fill="x")
        self.samplevars = {}
        fields = [
            ("away_score", "Away score"),
            ("home_score", "Home score"),
            ("away_name", "Away name"),
            ("home_name", "Home name"),
            ("away_abbr", "Away abbr"),
            ("home_abbr", "Home abbr"),
            ("away_rank", "Away rank"),
            ("home_rank", "Home rank"),
            ("away_record", "Away record"),
            ("home_record", "Home record"),
            ("clock", "Clock"),
            ("quarter", "Quarter"),
            ("down_distance", "Down & distance"),
            ("timeouts", "Timeouts"),
            ("possession", "Possession")
        ]
        for i, (k, label) in enumerate(fields):
            rr = i // 3
            cc = (i % 3) * 2
            ttk.Label(
                box, text=label
            ).grid(
                row=rr, column=cc,
                sticky="w", padx=2
            )
            v = tk.StringVar(value=self.sample[k])
            self.samplevars[k] = v
            ttk.Entry(
                box, textvariable=v, width=13
            ).grid(
                row=rr, column=cc+1,
                sticky="ew", padx=2, pady=2
            )
            v.trace_add(
                "write",
                lambda *_: self.preview()
            )
        for i in range(6):
            box.columnconfigure(i, weight=1)
        # RIGHT: Properties
        ttk.Label(
            right,
            text="ELEMENT PROPERTIES",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")
        self.props = ttk.Frame(right)
        self.props.pack(fill="both", expand=True)
        self.status = tk.StringVar(value="Ready")
        ttk.Label(
            self.root,
            textvariable=self.status,
            relief="sunken",
            anchor="w"
        ).pack(fill="x", side="bottom")
    def refresh_list(self):
        self.lb.delete(0, "end")
        for i, e in enumerate(self.elements):
            self.lb.insert("end", f"{i+1:02d}  {e.get('name', e['type'])}  [{e['type']}]")
        valid = [i for i in getattr(self, "selected_indices", [])
                 if 0 <= i < len(self.elements)]
        if not valid and self.elements:
            valid = [max(0, min(self.selected, len(self.elements) - 1))]
        self.selected_indices = valid
        if valid:
            self.selected = valid[-1]
            for i in valid:
                self.lb.selection_set(i)

    def lb_select(self, _=None):
        selection = list(self.lb.curselection())
        if selection:
            self.selected_indices = selection
            self.selected = selection[-1]
            self.properties()
            self.preview()

    def select(self, i):
        if not self.elements:
            self.selected_indices = []
            self.lb.selection_clear(0, "end")
            return
        self.selected = max(0, min(i, len(self.elements) - 1))
        self.selected_indices = [self.selected]
        self.refresh_list()
        self.properties()
        self.preview()

    def get_selection(self):
        indices = sorted({i for i in getattr(self, "selected_indices", [])
                          if 0 <= i < len(self.elements)})
        if not indices and self.elements:
            indices = [max(0, min(self.selected, len(self.elements) - 1))]
        return indices

    def snap_coordinate(self, value):
        if self.snap_var.get():
            try:
                step = max(1, int(self.grid_size_var.get()))
                value = round(value / step) * step
            except (TypeError, ValueError):
                pass
        return round(value)

    def apply_positions(self, updates, description):
        if not updates:
            return
        for index, (x, y) in updates.items():
            if 0 <= index < len(self.elements):
                self.elements[index]["x"] = self.snap_coordinate(x)
                self.elements[index]["y"] = self.snap_coordinate(y)
        self.status.set(description)
        self.properties()
        self.preview()

    def align_layers(self, mode):
        indices = self.get_selection()
        if len(indices) < 2:
            self.status.set("Select at least two layers to align them.")
            return
        items = [self.elements[i] for i in indices]
        left = min(float(e.get("x", 0)) for e in items)
        top = min(float(e.get("y", 0)) for e in items)
        right = max(float(e.get("x", 0)) + float(e.get("w", 0)) for e in items)
        bottom = max(float(e.get("y", 0)) + float(e.get("h", 0)) for e in items)
        center_x, center_y = (left + right) / 2, (top + bottom) / 2
        updates = {}
        for i in indices:
            e = self.elements[i]
            x, y = float(e.get("x", 0)), float(e.get("y", 0))
            w, h = float(e.get("w", 0)), float(e.get("h", 0))
            if mode == "left": x = left
            elif mode == "center_x": x = center_x - w / 2
            elif mode == "right": x = right - w
            elif mode == "top": y = top
            elif mode == "center_y": y = center_y - h / 2
            elif mode == "bottom": y = bottom - h
            updates[i] = (x, y)
        self.apply_positions(updates, "Aligned selected layers.")

    def align_canvas(self, mode):
        indices = self.get_selection()
        if not indices:
            return
        items = [self.elements[i] for i in indices]
        left = min(float(e.get("x", 0)) for e in items)
        top = min(float(e.get("y", 0)) for e in items)
        right = max(float(e.get("x", 0)) + float(e.get("w", 0)) for e in items)
        bottom = max(float(e.get("y", 0)) + float(e.get("h", 0)) for e in items)
        if mode == "center_both":
            dx = W / 2 - (left + right) / 2
            dy = H / 2 - (top + bottom) / 2
        else:
            dx = -left if mode == "left" else (
                W / 2 - (left + right) / 2 if mode == "center_x" else
                W - right if mode == "right" else 0
            )
            dy = -top if mode == "top" else (
                H / 2 - (top + bottom) / 2 if mode == "center_y" else
                H - bottom if mode == "bottom" else 0
            )
        updates = {i: (float(self.elements[i].get("x", 0)) + dx,
                       float(self.elements[i].get("y", 0)) + dy) for i in indices}
        self.apply_positions(updates, "Aligned selection to canvas.")

    def distribute(self, axis):
        indices = self.get_selection()
        if len(indices) < 3:
            self.status.set("Select at least three layers to distribute them.")
            return
        dimension = "w" if axis == "x" else "h"
        ordered = sorted(indices, key=lambda i: float(self.elements[i].get(axis, 0)))
        first, last = self.elements[ordered[0]], self.elements[ordered[-1]]
        start = float(first.get(axis, 0))
        end = float(last.get(axis, 0)) + float(last.get(dimension, 0))
        total_size = sum(float(self.elements[i].get(dimension, 0)) for i in ordered)
        gap = (end - start - total_size) / (len(ordered) - 1)
        updates = {}
        cursor = start
        for i in ordered:
            e = self.elements[i]
            x, y = float(e.get("x", 0)), float(e.get("y", 0))
            if axis == "x": x = cursor
            else: y = cursor
            updates[i] = (x, y)
            cursor += float(e.get(dimension, 0)) + gap
        self.apply_positions(updates, "Distributed selected layers.")

    def scale_by(self, factor):
        """Scale the current selection by a relative factor."""
        self.scale_percent_var.set(str(round(factor * 100, 2)))
        self.scale_selection()

    def scale_selection(self):
        """Scale layer geometry and visual weights around the selection center."""
        indices = self.get_selection()
        if not indices:
            self.status.set("Select at least one layer to scale.")
            return
        try:
            factor = float(self.scale_percent_var.get().strip()) / 100.0
        except (TypeError, ValueError):
            messagebox.showerror("Invalid scale", "Enter a scale percentage, such as 80 or 125.")
            return
        if not 0.01 <= factor <= 100:
            messagebox.showerror("Invalid scale", "Scale must be between 1% and 10000%.")
            return
        items = [self.elements[i] for i in indices]
        left = min(float(e.get("x", 0)) for e in items)
        top = min(float(e.get("y", 0)) for e in items)
        right = max(float(e.get("x", 0)) + float(e.get("w", 0)) for e in items)
        bottom = max(float(e.get("y", 0)) + float(e.get("h", 0)) for e in items)
        center_x = (left + right) / 2.0
        center_y = (top + bottom) / 2.0

        for e in items:
            x = float(e.get("x", 0))
            y = float(e.get("y", 0))
            e["x"] = round(center_x + (x - center_x) * factor, 2)
            e["y"] = round(center_y + (y - center_y) * factor, 2)
            for key in ("w", "h", "width", "font_scale"):
                if key not in e:
                    continue
                value = float(e[key]) * factor
                if key in ("w", "h"):
                    # Keep ordinary shapes usable; zero-height/width lines stay zero.
                    original = float(e[key])
                    value = max(1.0, value) if original > 0 else 0.0
                elif key == "width":
                    value = max(0.0, value)
                else:
                    value = max(0.05, value)
                e[key] = round(value, 3)

        self.status.set(
            f"Scaled {len(indices)} layer(s) to {factor * 100:g}% around selection center."
        )
        self.properties()
        self.preview()

    def properties(self):
        for w in self.props.winfo_children():
            w.destroy()
        self.vars = {}
        e = self.elements[self.selected]
        fields = [
            ("name", "Name", "entry"),
            ("x", "X", "entry"),
            ("y", "Y", "entry"),
            ("w", "Width", "entry"),
            ("h", "Height", "entry"),
            ("alpha", "Opacity", "entry")
        ]
        if e["type"] in ("rect", "roundrect", "ellipse"):
            fields += [
                ("fill_mode", "Fill source", "mode"),
                ("fill", "Fill color", "color"),
                ("outline", "Outline color", "color"),
                ("width", "Outline width", "entry")
            ]
        elif e["type"] == "line":
            fields += [
                ("color", "Line color", "color"),
                ("width", "Line width", "entry")
            ]
        elif e["type"] == "text":
            fields += [
                ("text", "Text / tokens", "entry"),
                ("color_mode", "Text color source", "mode"),
                ("color", "Text color", "color"),
                ("font_scale", "Font scale", "entry"),
                ("align", "Alignment", "align")
            ]
        for k, label, typ in fields:
            row = ttk.Frame(self.props)
            row.pack(fill="x", pady=3)
            ttk.Label(
                row, text=label, width=17
            ).pack(side="left")
            v = tk.StringVar(value=str(e.get(k, "")))
            self.vars[k] = v
            if typ == "mode":
                w = ttk.Combobox(
                    row,
                    textvariable=v,
                    values=MODES,
                    state="readonly",
                    width=15
                )
                w.pack(side="left", fill="x", expand=True)
                w.bind(
                    "<<ComboboxSelected>>",
                    lambda _, key=k: self.change(key)
                )
            elif typ == "align":
                w = ttk.Combobox(
                    row,
                    textvariable=v,
                    values=["left", "center", "right"],
                    state="readonly"
                )
                w.pack(side="left", fill="x", expand=True)
                w.bind(
                    "<<ComboboxSelected>>",
                    lambda _, key=k: self.change(key)
                )
            elif typ == "color":
                ttk.Entry(
                    row, textvariable=v
                ).pack(side="left", fill="x", expand=True)
                ttk.Button(
                    row,
                    text="Pick",
                    command=lambda key=k: self.pick(key)
                ).pack(side="left", padx=2)
                v.trace_add(
                    "write",
                    lambda *_, key=k: self.change(key)
                )
            else:
                ttk.Entry(
                    row, textvariable=v
                ).pack(side="left", fill="x", expand=True)
                v.trace_add(
                    "write",
                    lambda *_, key=k: self.change(key)
                )
        if e["type"] == "text":
            ttk.Label(
                self.props,
                text="Click to insert a dynamic field:",
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", pady=(10, 3))
            grid = ttk.Frame(self.props)
            grid.pack(fill="x")
            for i, t in enumerate(TOKENS):
                ttk.Button(
                    grid,
                    text=t,
                    command=lambda token=t: self.token(token)
                ).grid(
                    row=i//2, column=i%2,
                    sticky="ew", padx=2, pady=2
                )
            grid.columnconfigure(0, weight=1)
            grid.columnconfigure(1, weight=1)
        ttk.Label(
            self.props,
            text="Team-linked colors use the live colshirt value from each team's home jersey."
        ).pack(anchor="w", pady=12)
    def change(self, k):
        if not self.elements:
            return
        v = self.vars[k].get()
        if k in (
            "x", "y", "w", "h",
            "alpha", "width", "font_scale"
        ):
            try:
                v = float(v)
            except ValueError:
                return
        self.elements[self.selected][k] = v
        self.refresh_list()
        self.preview()
    def pick(self, k):
        c = colorchooser.askcolor(
            initialcolor=self.vars[k].get()
        )[1]
        if c:
            self.vars[k].set(c)
    def token(self, t):
        v = self.vars.get("text")
        if v:
            v.set(v.get() + t)
    def add(self):
        typ = {
            "Rectangle": "rect",
            "Rounded rectangle": "roundrect",
            "Ellipse": "ellipse",
            "Line": "line",
            "Text": "text"
        }[self.kind.get()]
        n = len(self.elements) + 1
        if typ == "text":
            e = {
                "type": typ,
                "name": f"Text {n}",
                "x": 366, "y": 160, "w": 120, "h": 24,
                "text": "{away_score}",
                "color": "#FFFFFF",
                "color_mode": "Fixed color",
                "font_scale": 1,
                "align": "center",
                "alpha": 1
            }
        elif typ == "line":
            e = {
                "type": typ,
                "name": f"Line {n}",
                "x": 100, "y": 100,
                "w": 100, "h": 0,
                "color": "#FFFFFF",
                "width": 2,
                "alpha": 1
            }
        else:
            e = {
                "type": typ,
                "name": f"{typ.title()} {n}",
                "x": 100, "y": 100,
                "w": 180, "h": 60,
                "fill": "#344E72",
                "fill_mode": "Fixed color",
                "outline": "#FFFFFF",
                "width": 0,
                "alpha": 1
            }
        self.elements.append(e)
        self.select(len(self.elements)-1)
    def duplicate(self):
        if not self.elements:
            return
        e = json.loads(
            json.dumps(self.elements[self.selected])
        )
        e["name"] += " copy"
        e["x"] += 12
        e["y"] += 12
        if self.snap_var.get():
            step = max(1, int(self.grid_size_var.get()))
            e["x"] = round(e["x"]/step)*step
            e["y"] = round(e["y"]/step)*step
        self.elements.insert(self.selected+1, e)
        self.select(self.selected+1)
    def delete(self):
        indices = self.get_selection()
        if not indices:
            return
        primary = self.selected
        for index in reversed(indices):
            del self.elements[index]
        if self.elements:
            self.selected = min(primary, len(self.elements) - 1)
            self.selected_indices = [self.selected]
            self.refresh_list()
            self.properties()
        else:
            self.selected = 0
            self.selected_indices = []
            self.lb.selection_clear(0, "end")
            for widget in self.props.winfo_children():
                widget.destroy()
        self.preview()

    def move(self, d):
        j = self.selected + d
        if 0 <= j < len(self.elements):
            self.elements[self.selected], self.elements[j] = (
                self.elements[j], self.elements[self.selected]
            )
            self.select(j)
    # Convert zoom percentage into a scale factor
    def _zoom(self):
        try:
            return max(
                0.25,
                float(self.zoom_var.get().replace("%", "")) / 100
            )
        except Exception:
            return 1.0
    # Mouse position is converted back into design coordinates
    def down(self, event):
        if not self.elements:
            return
        z = self._zoom()
        px = self.cv.canvasx(event.x) / z
        py = self.cv.canvasy(event.y) / z
        indices = self.get_selection()
        self.drag_origin = (
            px, py,
            {i: (float(self.elements[i].get("x", 0)),
                 float(self.elements[i].get("y", 0))) for i in indices}
        )

    def drag(self, event):
        if not self.elements or not hasattr(self, "drag_origin"):
            return
        z = self._zoom()
        px = self.cv.canvasx(event.x) / z
        py = self.cv.canvasy(event.y) / z
        sx, sy, original_positions = self.drag_origin
        dx, dy = px - sx, py - sy
        for i, (x, y) in original_positions.items():
            self.elements[i]["x"] = self.snap_coordinate(x + dx)
            self.elements[i]["y"] = self.snap_coordinate(y + dy)
        primary = self.elements[self.selected]
        for key in ("x", "y"):
            if key in self.vars:
                self.vars[key].set(str(primary.get(key, 0)))
        self.preview()

    def preview(self):
        if not hasattr(self, "cv"):
            return
        self.sample.update({
            k: v.get() for k, v in self.samplevars.items()
        })
        c = self.cv
        c.delete("all")
        # Zoom factor
        z = self._zoom()
        # Scaled canvas dimensions
        cw = W * z
        ch = H * z
        c.configure(
            scrollregion=(0, 0, cw, ch),
            width=min(int(cw), 700),
            height=min(int(ch), 390)
        )
        # Background
        c.create_rectangle(
            0, 0, cw, ch,
            fill="#18212e",
            outline=""
        )
        # Grid
        if self.grid_visible_var.get():
            step = max(1, int(self.grid_size_var.get()))
            for gx in range(
                0, int(cw)+1, max(1, int(step*z))
            ):
                original_x = gx / z
                color = (
                    "#354456"
                    if round(original_x) % 40 == 0
                    else "#263342"
                )
                c.create_line(gx, 0, gx, ch, fill=color)
            for gy in range(
                0, int(ch)+1, max(1, int(step*z))
            ):
                original_y = gy / z
                color = (
                    "#354456"
                    if round(original_y) % 40 == 0
                    else "#263342"
                )
                c.create_line(0, gy, cw, gy, fill=color)
        # Dynamic color selection
        def col(e, key, modekey):
            m = e.get(modekey, "Fixed color")
            if m == "Away team":
                return self.sample["away_color"]
            if m == "Home team":
                return self.sample["home_color"]
            if m == "Away lighter":
                return shade(self.sample["away_color"], .35)
            if m == "Home lighter":
                return shade(self.sample["home_color"], .35)
            if m == "Away darker":
                return shade(self.sample["away_color"], -.35)
            if m == "Home darker":
                return shade(self.sample["home_color"], -.35)
            return e.get(key, "#FFFFFF")
        # Draw elements
        for i, e in enumerate(self.elements):
            x, y, w, h = [
                float(e.get(k, 0)) * z
                for k in ("x", "y", "w", "h")
            ]
            typ = e["type"]
            if typ in ("rect", "roundrect", "ellipse"):
                fill = col(e, "fill", "fill_mode")
                outline = e.get("outline", fill)
                width = max(
                    1,
                    int(float(e.get("width", 0)) * z)
                )
                if typ == "ellipse":
                    c.create_oval(
                        x, y, x+w, y+h,
                        fill=fill,
                        outline=outline,
                        width=width
                    )
                elif typ == "roundrect":
                    c.create_rectangle(
                        x, y, x+w, y+h,
                        fill=fill,
                        outline=outline,
                        width=width
                    )
                else:
                    c.create_rectangle(
                        x, y, x+w, y+h,
                        fill=fill,
                        outline=outline,
                        width=width
                    )
            elif typ == "line":
                c.create_line(
                    x, y, x+w, y+h,
                    fill=e.get("color", "#FFFFFF"),
                    width=max(
                        1,
                        int(float(e.get("width", 1))*z)
                    )
                )
            elif typ == "text":
                text = str(e.get("text", ""))
                for k, v in self.sample.items():
                    text = text.replace(
                        "{" + k + "}", str(v)
                    )
                anchor = {
                    "left": "w",
                    "center": "center",
                    "right": "e"
                }.get(e.get("align", "center"), "center")
                font_size = max(
                    7,
                    int(10 * float(e.get("font_scale", 1)) * z)
                )
                c.create_text(
                    x,
                    y,
                    text=text,
                    fill=col(e, "color", "color_mode"),
                    font=("Arial", font_size, "bold"),
                    anchor=anchor
                )
            # Selected element outline
            if i == self.selected:
                c.create_rectangle(
                    x-3*z,
                    y-3*z,
                    x+w+3*z,
                    y+h+3*z,
                    outline="#FFD166",
                    dash=(3, 2)
                )
    def new(self):
        if messagebox.askyesno(
            "New", "Start a blank scorebug?"
        ):
            self.elements = []
            self.selected = 0
            self.selected_indices = []
            self.refresh_list()
            for widget in self.props.winfo_children():
                widget.destroy()
            self.preview()
    def open(self):
        p = filedialog.askopenfilename(
            filetypes=[("Scorebug project", "*.json")]
        )
        if not p:
            return
        try:
            with open(p, encoding="utf-8") as f:
                d = json.load(f)
            self.elements = d["elements"]
            self.selected = 0
            self.selected_indices = [0] if self.elements else []
            self.refresh_list()
            if self.elements:
                self.select(0)
            else:
                for widget in self.props.winfo_children():
                    widget.destroy()
                self.preview()
            self.status.set("Opened " + os.path.basename(p))
        except Exception as ex:
            messagebox.showerror("Open failed", str(ex))
    def save(self):
        p = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Scorebug project", "*.json")]
        )
        if p:
            try:
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "format": "RetroBowlScorebugStudio",
                            "version": 1,
                            "canvas": [W, H],
                            "elements": self.elements
                        },
                        f,
                        indent=2
                    )
                self.status.set("Saved " + p)
            except Exception as ex:
                messagebox.showerror("Save failed", str(ex))
    def import_uniforms(self):
        p = filedialog.askopenfilename(
            title="Choose uniforms_default_CO.txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if not p:
            return
        try:
            with open(
                p, encoding="utf-8-sig", errors="replace"
            ) as f:
                raw = f.read()
            colors = re.findall(
                r"[$#]([0-9a-fA-F]{6})", raw
            )
            messagebox.showinfo(
                "Uniform file",
                f"Scanned file and found {len(colors)} color values. "
                "Runtime export uses each live team's colshirt value, "
                "matching the reference scorebug."
            )
            self.status.set("Scanned " + os.path.basename(p))
        except Exception as ex:
            messagebox.showerror("Import failed", str(ex))
    def export(self):
        p = filedialog.asksaveasfilename(
            defaultextension=".js",
            initialfile="custom_scorebug.js",
            filetypes=[("JavaScript mod", "*.js")]
        )
        if not p:
            return
        try:
            title = os.path.splitext(
                os.path.basename(p)
            )[0].replace("_", " ").title()
            with open(p, "w", encoding="utf-8") as f:
                f.write(generate_js(self.elements, title))
            self.status.set("Exported " + p)
            messagebox.showinfo(
                "Exported",
                "JS scorebug mod created. Import the JS file or its "
                "containing folder through the Mod Builder. The scorebug "
                "reads live game scores, team names/abbreviations, records, "
                "subdivision rankings, clock, quarter, down/distance "
                "and jersey colors."
            )
        except Exception as ex:
            messagebox.showerror("Export failed", str(ex))
if __name__ == "__main__":
    root = tk.Tk()
    app = Studio(root)
    root.mainloop()