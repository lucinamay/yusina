"""단청 sheet for the gallery: the colour logic, explained next to its visualisation,
and a few 문양 drawn with matplotlib patches.

    python scripts/collections/korea/dancheong.py [ko|en|all] [out.png]   # -> gallery/collections/korea/dancheong[_en].png

Colour values: MMCA 한국전통표준색명 as screen approximations (koreancoloratlas.com);
see ``palettes.csv`` rows Obangsaek / Ogansaek / Dancheong and ``colours.DANCHEONG_BARIM``.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, PathPatch, Rectangle, RegularPolygon, Wedge
from matplotlib.path import Path as MPath

from yusina import palettes as P
from yusina import set_style
from yusina.colours import DANCHEONG_BARIM, outline

GALLERY = Path(__file__).resolve().parents[3] / "gallery" / "collections" / "korea"
ASSETS = GALLERY / "assets"
# matplotlib falls back across fonts only when font.family itself is a list, not via the sans-serif alias
HANGUL = "Apple SD Gothic Neo"
SERIF = ["Gowun Batang", "Apple SD Gothic Neo"]  # hanja come from the Gothic; AppleMyungjo draws nothing as a fallback

OO = P.get("Obang-Ogansaek")  # 청 녹 적 홍 황 유황 백 벽 흑 자
OBANG = dict(zip("청적황백흑", OO[0::2]))
OGAN = dict(zip(["녹", "홍", "유황", "벽", "자"], OO[1::2]))
DC = P.get("Dancheong")
HWI_BANDS = [("장단", DC[0:3]), ("삼청", DC[3:6]), ("황", DC[6:7]), ("양록", DC[7:10]), ("육색", DC[10:11]), ("석간주", DC[11:13])]
HWI = {k: v[1 if len(v) == 3 else 0] for k, v in HWI_BANDS}  # the band's own colour (2빛 of a 3-step band)
BARIM_NAMES = {"red": "분홍 장단 주홍 다자", "green": "백록 양록 하엽 먹", "blue": "분삼청 삼청 군청 먹"}
BASES = {"뇌록": DC[13], "석간주": DC[11]}
INK = "#211F1E"  # 먹


# romanised pigment / colour names for the English sheet
ROMAN = {"청": "cheong", "적": "jeok", "황": "hwang", "백": "baek", "흑": "heuk", "녹": "nok", "홍": "hong", "유황": "yuhwang",
         "벽": "byeok", "자": "ja", "장단": "jangdan", "삼청": "samcheong", "양록": "yangnok", "육색": "yuksaek",
         "석간주": "seokganju", "주사": "jusa", "분홍": "bunhong", "주홍": "juhong", "백록": "baengnok", "분삼청": "bunsamcheong", "다자": "daja", "명록": "myeongnok", "석록": "seongnok", "하엽": "hayeop",
         "먹": "meok", "천청": "cheoncheong", "군청": "guncheong", "뇌록": "noerok"}

STRINGS = {
    "ko": {
        "suptitle": "단청 · 색의 원리와 무늬",
        "t_obang": "오방색 · 음양오행의 다섯 방위",
        "dirs": {"청": "동 · 목 · 봄", "적": "남 · 화 · 여름", "황": "중앙 · 토", "백": "서 · 금 · 가을", "흑": "북 · 수 · 겨울"},
        "pent": "오행 · 실선 상생, 점선 상극",
        "c_obang": "오방은 방위이므로 십자: 동서남북에 중앙. 오행의 관계(상생·상극)는 오각형으로 그린다.\n팔레트 순서는 상생 순서 목→화→토→금→수 = 청 적 황 백 흑.",
        "t_ogan": "오간색 · 이웃한 두 정색의 사이",
        "c_ogan": "녹=청+황, 홍=적+백, 유황=흑+황, 벽=청+백, 자=흑+적.\n팔레트 `Obang-Ogansaek`은 정색 뒤에 같은 방위의 간색을 둔다.",
        "t_bg": "단청이란",
        "bg": ("단청(丹靑)은 목조 건물에 칠하는 채색. 나무를 비바람과 벌레에서 지키고, 건물의 격을 드러낸다.\n\n"
               "색의 뿌리는 음양오행: 다섯 방위에 다섯 정색(오방색), 그 사이에 다섯 간색(오간색).\n\n"
               "칠하는 순서에도 논리가 있다. 바탕은 뇌록이나 석간주로 고르게 깔고, 무늬는 밝은 빛에서\n"
               "어두운 빛으로 단계(바림)를 두어 올린다. 부재 끝의 띠(휘)는 장단·삼청·황·양록·육색·석간주의\n"
               "고정 순서를 따라 난색과 한색이 교대한다.\n\n"
               "격에 따라 가칠단청(바탕만) → 긋기단청 → 모로단청(끝에만 무늬, 2빛) → 금단청(전면 무늬, 3빛)."),
        "t_barim": "바림 · 빛의 단계 (초빛 → 2빛 → 3빛 → 먹)",
        "steps": ["초빛", "2빛", "3빛", "먹"],
        "hues": {"red": "적", "green": "녹", "blue": "청"},
        "c_barim": "초빛은 안료에 호분을 섞은 것(분홍·백록·분삼청), 그 다음이 안료, 그 다음이 짙은 안료.\n모로단청은 2빛, 금단청은 3빛.",
        "t_cmaps": "같은 사다리를 연속 컬러맵으로",
        "c_cmaps": "`dancheong_red/green/blue`로 등록. 끝이 먹이라 최댓값이 검게 닫힌다.",
        "t_hwi": "휘(暉) · 부재 끝의 띠, 순서는 고정",
        "c_hwi": ("장단 → 삼청 → 황 → 양록 → 육색 → 석간주: 난색과 한색이 번갈아 와 이웃 띠끼리 보색 대비.\n"
                  "띠가 셋 이상이면 마지막은 석간주. 띠 안의 단계가 빛(초빛 바깥, 깊은 빛 안쪽). 바탕은 뇌록."),
        "t_meoricho": "연화머리초 · 꽃잎을 빛 단계로",
        "c_meoricho": "꽃잎 하나 안에서 분홍 → 장단 → 주홍(초빛→3빛), 먹선 안쪽에 백선, 잎 사이에 녹화 고리, 뒤로 휘 띠.\n오른쪽 사진의 서까래 머리초를 단순화한 것.",
        "t_geummun": "금문(錦紋) · 귀갑문, 거북 등처럼 이어지는 육각 격자",
        "c_geummun": "계풍(부재 가운데 빈 면)이나 금단청의 머리초 사이를 채우는 기하 무늬.\n두 색이 번갈아 가며 바탕 석간주 위에 놓이고, 겹선 안에 꽃술 점을 찍는다.",
        "t_plots": "팔레트 `Dancheong` 그대로: 휘 순서 + 빛 단계",
        "c_plots": "위 띠가 팔레트 순서: 분홍·장단·주홍 | 분삼청·삼청·군청 | 황 | 백록·양록·하엽 | 육색 | 석간주·다자 | 뇌록.\n14색, 쌓으면 휘가 된다.",
        "t_plate": "경복궁 교태전 천정 문양 · 조선총독부 조사 도판",
        "c_plate": "휘 띠와 빛 단계, 연분홍(장단육색)과 녹 사다리가 그대로 보인다.\n조선총독부 간행 도판, 퍼블릭 도메인. Wikimedia Commons: B004636 2 경복궁교태전천정문양.",
        "t_photo": "경복궁 서까래 끝 · 겹겹이 쌓인 머리초",
        "c_photo": "꽃잎마다 분홍·장단·주홍 세 빛, 먹선 안쪽의 백선, 사이사이 녹화(綠花) 고리, 마구리의 연화.\n사진: Huntsmanleader, CC BY 4.0 (Wikimedia Commons: Gyeongbokgung Close up details 2023-09-24).",
        "t_stack": "경복궁 근정전 공포 · 정면에서 본 겹겹의 살미",
        "c_stack": "구름 모양 살미와 첨차가 층층이 쌓이고, 층마다 녹·청·적 휘와 백선이 반복된다.\n사진: Ethan Doyle White, CC BY-SA 4.0 (Wikimedia Commons: Ceiling Detail at Geunjeongjeon).",
        "t_prov": "출처와 주의",
        "prov": ("색 값에 관하여\n\n"
                 "단청 안료의 공식 RGB 표준은 없다. 여기 쓴 값은 국립현대미술관 「한국전통표준색명」(1992)을\n"
                 "화면용으로 근사한 koreancoloratlas.com의 값이며, 사이트 스스로 측색값이 아니라고 밝힌다.\n\n"
                 "값은 안료 표(korea_pigments.csv)에서 가져오고, 초빛은 안료와 호분을 OKLab에서 반씩 섞은 것이다.\n"
                 "실물 안료와는 다르다고 보는 게 안전하다.\n\n"
                 "팔레트: Obang-Ogansaek · Dancheong (palettes.csv)\n"
                 "컬러맵: dancheong_red · dancheong_green · dancheong_blue (colours.py)"),
    },
    "en": {
        "suptitle": "Dancheong (단청) · the logic behind its colours and patterns",
        "t_obang": "Five cardinal colours (오방색) · directions of the five phases (오행)",
        "dirs": {"청": "east · wood · spring", "적": "south · fire · summer", "황": "centre · earth",
                 "백": "west · metal · autumn", "흑": "north · water · winter"},
        "pent": "five phases (오행) · solid: generating (상생), dashed: overcoming (상극)",
        "c_obang": "The five directions (오방) are a cross: four compass points around a centre. The relations between the five phases (오행) are the pentagon.\nThe palette follows the generating cycle wood → fire → earth → metal → water = blue, red, yellow, white, black.",
        "t_ogan": "Five intermediate colours (오간색) · between two neighbouring cardinal colours",
        "c_ogan": "nok = blue + yellow, hong = red + white, yuhwang = black + yellow, byeok = blue + white, ja = black + red.\nThe `Obang-Ogansaek` palette places each intermediate after the cardinal colour of its direction.",
        "t_bg": "What dancheong (단청) is",
        "bg": ("Dancheong (단청) is the painted decoration of wooden buildings. It shields the timber from weather and insects\n"
               "and shows the rank of the building.\n\n"
               "Its colours come from yin-yang and the five phases (음양오행): five cardinal colours (오방색) on the five\n"
               "directions, and five intermediate colours (오간색) between them.\n\n"
               "The order of painting has its own logic. A ground of noerok (뇌록) or seokganju (석간주) is laid first; patterns\n"
               "go on top in graded steps (바림) from a light tone to a dark one. The bands (휘) at the end of a beam follow the\n"
               "fixed sequence jangdan, samcheong, hwang, yangnok, yuksaek, seokganju, so warm and cool alternate.\n\n"
               "By rank: ground only (가칠단청) → lines (긋기단청) → patterns at the ends, two tones (모로단청) → full\n"
               "patterns, three tones (금단청)."),
        "t_barim": "Gradation (바림) · the tone steps (빛): first → second → third → ink (먹)",
        "steps": ["first (초빛)", "second (2빛)", "third (3빛)", "ink (먹)"],
        "hues": {"red": "red (적)", "green": "green (녹)", "blue": "blue (청)"},
        "c_barim": "The first tone is the pigment mixed with shell white (분홍, 백록, 분삼청), then the pigment, then its deep step.\nMoro dancheong (모로단청) uses two tones, geum dancheong (금단청) three.",
        "t_cmaps": "The same ladders as continuous colormaps",
        "c_cmaps": "Registered as `dancheong_red/green/blue`. The last step is ink (먹), so the maximum closes to black.",
        "t_hwi": "Bands (휘) · at the end of a member, in a fixed order",
        "c_hwi": ("jangdan → samcheong → hwang → yangnok → yuksaek → seokganju: warm and cool alternate, so neighbouring bands contrast.\n"
                  "With three or more bands the last is seokganju. The steps inside a band are the tones (빛): first tone outside, deeper inside. Ground: noerok (뇌록)."),
        "t_meoricho": "Lotus head pattern (연화머리초) · petals in tone steps",
        "c_meoricho": "Inside each petal bunhong → jangdan → juhong (first to third tone), a white line inside the ink outline, green hooks (녹화) between petals, bands (휘) behind.\nA simplified version of the rafter-end lotus heads in the photo on the right.",
        "t_geummun": "Brocade pattern (금문) · tortoise-shell lattice (귀갑문)",
        "c_geummun": "Geometric filler for the plain middle of a member (계풍) or between lotus heads in geum dancheong.\nTwo colours alternate on a seokganju ground, with a stamen dot inside the double line.",
        "t_plots": "The `Dancheong` palette as is: band order + tone steps",
        "c_plots": "The strip above is the palette order: bunhong·jangdan·juhong | bunsamcheong·samcheong·guncheong | hwang | baengnok·yangnok·hayeop | yuksaek | seokganju·daja | noerok.\n14 colours; stacked, they become a band (휘).",
        "t_plate": "Ceiling pattern of Gyotaejeon (교태전), Gyeongbokgung · survey plate",
        "c_plate": "Bands (휘) with their tone steps, the soft pink (장단육색) and the green ladder are all visible.\nPlate published by the Government-General of Chōsen, public domain. Wikimedia Commons: B004636 2 경복궁교태전천정문양.",
        "t_photo": "Rafter ends at Gyeongbokgung · lotus heads (머리초) stacked layer on layer",
        "c_photo": "Three tones per petal (bunhong, jangdan, juhong), a white line inside the ink outline, green hooks (녹화) between petals, a lotus on each end face.\nPhoto: Huntsmanleader, CC BY 4.0 (Wikimedia Commons: Gyeongbokgung Close up details 2023-09-24).",
        "t_stack": "Bracket cluster (공포) of Geunjeongjeon, Gyeongbokgung · the layers seen head-on",
        "c_stack": "Cloud-shaped bracket arms (살미, 첨차) stack layer on layer; each layer repeats the green, blue and red bands with white lines.\nPhoto: Ethan Doyle White, CC BY-SA 4.0 (Wikimedia Commons: Ceiling Detail at Geunjeongjeon).",
        "t_prov": "Sources and caveats",
        "prov": ("On the colour values\n\n"
                 "There is no official RGB standard for dancheong pigments. The values here are koreancoloratlas.com's screen\n"
                 "approximations of the MMCA Korean Traditional Standard Colour Names (한국전통표준색명, 1992); the site itself\n"
                 "states they are not colorimetric measurements.\n\n"
                 "Values come from the pigment table (korea_pigments.csv); each first tone is the pigment and shell white mixed\n"
                 "half and half in OKLab. Assume all of them differ from the real pigments.\n\n"
                 "Palettes: Obang-Ogansaek · Dancheong (palettes.csv)\n"
                 "Colormaps: dancheong_red · dancheong_green · dancheong_blue (colours.py)"),
    },
}
S = STRINGS["ko"]
LANG = "ko"


def _name(k, two_lines=True):
    """Colour name for the current language: Korean, or romanised with Korean in brackets."""
    if LANG == "ko":
        return k
    return f"{ROMAN[k]}\n({k})" if two_lines else f"{ROMAN[k]} ({k})"


def _blank(ax, title):
    ax.set_title(title, fontfamily=SERIF, fontweight="bold", fontsize=11 if LANG == "ko" else 10)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)


def _caption(ax, text):
    ax.text(0, -0.06, text, transform=ax.transAxes, va="top", ha="left", fontsize=8.5, linespacing=1.5)


# ------------------------------------------------------------ 1. 오방색 ----
def obang_wheel(ax):
    _blank(ax, S["t_obang"])
    ax.set_xlim(-1.6, 3.2); ax.set_ylim(-1.55, 1.55); ax.set_aspect("equal")
    pos = {"청": (1, 0), "적": (0, -1), "황": (0, 0), "백": (-1, 0), "흑": (0, 1)}  # 오방: a cross, 황 in the middle
    for k, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 0.36, color=OBANG[k], ec=outline(OBANG[k]) if k != "백" else "#C8C4BA", lw=1))
        ax.text(x, y, _name(k), ha="center", va="center", fontsize=15 if LANG == "ko" else 8, fontfamily=SERIF,
                color="white" if k in "청적흑" else INK)
        ax.text(x, y - 0.47, S["dirs"][k], ha="center", va="top", fontsize=7.5)
    # 오행: the pentagon, clockwise from the top 화 토 금 수 목; 상생 around the ring, 상극 as the star
    cx, r = 2.35, 0.62
    phase = {"적": "화", "황": "토", "백": "금", "흑": "수", "청": "목"}
    order = ["적", "황", "백", "흑", "청"]
    pts = {k: (cx + r * np.sin(np.radians(72 * i)), r * np.cos(np.radians(72 * i))) for i, k in enumerate(order)}
    for a, b in zip(order, order[1:] + order[:1]):  # 상생 목→화→토→금→수
        ax.annotate("", pts[b], pts[a], arrowprops={"arrowstyle": "->", "color": INK, "lw": 0.9, "shrinkA": 9, "shrinkB": 9})
    for a, b in zip(order, order[2:] + order[:2]):  # 상극 화→금→목→토→수
        ax.annotate("", pts[b], pts[a], arrowprops={"arrowstyle": "->", "color": INK, "lw": 0.5, "ls": "--", "shrinkA": 9, "shrinkB": 9, "alpha": 0.6})
    for k, (x, y) in pts.items():
        ax.add_patch(Circle((x, y), 0.14, color=OBANG[k], ec=outline(OBANG[k]) if k != "백" else "#C8C4BA", lw=0.8))
        ax.text(x, y, phase[k] if LANG == "ko" else {"화": "fire", "토": "earth", "금": "metal", "수": "water", "목": "wood"}[phase[k]],
                ha="center", va="center", fontsize=7 if LANG == "ko" else 5, color="white" if k in "청적흑" else INK)
    ax.text(cx, -0.95, S["pent"], ha="center", va="top", fontsize=7.5)
    _caption(ax, S["c_obang"])


# ------------------------------------------------------------ 2. 오간색 ----
def ogan_mixes(ax):
    _blank(ax, S["t_ogan"])
    ax.set_xlim(-0.3, 5.3); ax.set_ylim(-0.75, 2.3); ax.set_aspect("equal")
    parents = {"녹": "청황", "홍": "적백", "유황": "흑황", "벽": "청백", "자": "흑적"}
    for i, (k, pq) in enumerate(parents.items()):
        for j, pk in enumerate(pq):
            ax.add_patch(Circle((i + 0.3 + 0.4 * j, 1.6), 0.19, color=OBANG[pk], ec="#C8C4BA" if pk == "백" else outline(OBANG[pk]), lw=0.6))
        ax.text(i + 0.5, 1.15, "+", ha="center", va="center", fontsize=9, color=INK)
        ax.add_patch(Rectangle((i + 0.1, 0.1), 0.8, 0.8, color=OGAN[k]))
        ax.text(i + 0.5, -0.1, _name(k), ha="center", va="top", fontsize=10 if LANG == "ko" else 8, fontfamily=SERIF)
    _caption(ax, S["c_ogan"])


# ------------------------------------------------------- 3. 빛 ladders ----
def barim(ax):
    _blank(ax, S["t_barim"])
    rows = list(DANCHEONG_BARIM.items())
    ax.set_xlim(-1.4, 4.1); ax.set_ylim(-0.3, len(rows) + 0.6)
    for h, step in enumerate(S["steps"]):
        ax.text(h + 0.5, len(rows) + 0.15, step, ha="center", va="bottom", fontsize=9)
    for r, (hue, cols) in enumerate(rows):
        y = len(rows) - 1 - r
        for h, c in enumerate(cols):
            ax.add_patch(Rectangle((h, y + 0.08), 1, 0.84, color=c))
        ax.text(-0.1, y + 0.5, S["hues"][hue], ha="right", va="center", fontsize=11 if LANG == "ko" else 9, fontfamily=SERIF)
        for h, name in enumerate(BARIM_NAMES[hue].split()):
            ax.text(h + 0.5, y + 0.5, _name(name), ha="center", va="center", fontsize=8, color="white" if h >= 2 else INK)
    _caption(ax, S["c_barim"])


def barim_cmaps(ax):
    _blank(ax, S["t_cmaps"])
    grad = np.linspace(0, 1, 256)[None, :]
    for i, hue in enumerate(DANCHEONG_BARIM):
        ax.imshow(grad, cmap=f"dancheong_{hue}", aspect="auto", extent=(0, 1, 2.1 + i * 0.6, 2.6 + i * 0.6))
        ax.text(1.02, 2.35 + i * 0.6, f"dancheong_{hue}", va="center", fontsize=8, family="monospace")
    ax.set_xlim(0, 1.6); ax.set_ylim(0, 3.95)
    z = np.add.outer(np.linspace(0, 1, 20), np.linspace(0, 1, 20)) / 2
    for x0, hue in [(0.0, "blue"), (0.34, "red"), (0.68, "green")]:
        ins = ax.inset_axes((x0, 0.0, 0.3, 0.47)); ins.imshow(z, cmap=f"dancheong_{hue}")
        ins.set_xticks([]); ins.set_yticks([]); ins.grid(False)
    _caption(ax, S["c_cmaps"])


# ------------------------------------------------------------- 4. 휘 ----
def hwi(ax):
    _blank(ax, S["t_hwi"])
    ax.set_xlim(-0.2, 3.3); ax.set_ylim(-0.1, 2.1); ax.set_aspect("equal")
    ax.add_patch(Rectangle((-0.2, -0.1), 3.5, 2.2, color=BASES["뇌록"]))
    r = 0.3
    for i, (name, steps) in enumerate(HWI_BANDS):
        w = 0.14 * len(steps) + 0.1
        for j, c in enumerate(steps):  # 초빛 outside, deeper steps inside
            sw = w / len(steps)
            ax.add_patch(Wedge((3.3, 1.0), r + w - j * sw, 90, 270, width=sw, color=c))
        ax.text(3.3 - (r + w / 2), 0.02 if i % 2 else 1.98, name if LANG == "ko" else ROMAN[name], ha="center",
                va="bottom" if i % 2 else "top", fontsize=7.5 if LANG == "ko" else 6, color="white" if name != "황" else INK)
        r += w + 0.03
    _caption(ax, S["c_hwi"])


# ------------------------------------------------------- 5. 연화머리초 ----
def _petal(ax, cx, cy, angle, length, width, colours, ink=INK):
    """One lotus petal: nested bezier lenses in 초빛/2빛/3빛, ink outline, white line inside it."""
    def path(scale, shift=0.0):
        L, W = length * scale, width * scale
        pts = np.array([[shift, 0], [shift + L * 0.25, W], [shift + L * 0.85, W * 0.75], [shift + L, 0],
                        [shift + L * 0.85, -W * 0.75], [shift + L * 0.25, -W], [shift, 0]])
        a = np.radians(angle); R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
        pts = pts @ R.T + [cx, cy]
        return MPath(pts, [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4])
    for scale, col in zip((1.0, 0.68, 0.36), colours):
        ax.add_patch(PathPatch(path(scale, length * (1 - scale) * 0.15), fc=col, ec="none"))
    ax.add_patch(PathPatch(path(1.0), fc="none", ec=ink, lw=1.1))
    ax.add_patch(PathPatch(path(0.88, length * 0.03), fc="none", ec="white", lw=0.6))


def _hook(ax, cx, cy, angle, size, colours):
    """녹화: a curling green hook between petals, drawn as a spiral stroke in three widths."""
    t = np.linspace(0, 1.9 * np.pi, 60)
    r = size * (0.55 + 0.45 * t / t[-1])[::-1]
    x, y = r * np.cos(t), r * np.sin(t)
    a = np.radians(angle); X = cx + x * np.cos(a) - y * np.sin(a); Y = cy + x * np.sin(a) + y * np.cos(a)
    for lw, col in zip((5.0, 3.4, 1.4), (INK, colours[1], colours[0])):
        ax.plot(X, Y, color=col, lw=lw, solid_capstyle="round")


def meoricho(ax):
    _blank(ax, S["t_meoricho"])
    ax.set_xlim(-1.75, 1.75); ax.set_ylim(-0.15, 1.85); ax.set_aspect("equal")
    ax.add_patch(Rectangle((-1.75, -0.15), 3.5, 2.0, color=BASES["뇌록"]))
    cx, cy = 0.0, 0.0
    red = DANCHEONG_BARIM["red"][:3]; green = DANCHEONG_BARIM["green"]; blue = DANCHEONG_BARIM["blue"]
    for i, (r0, col) in enumerate([(1.55, blue), (1.38, green)]):  # 휘 behind the head: 초빛 outside, deeper inside
        for j, c in enumerate(col[:3]):
            ax.add_patch(Wedge((cx, cy), r0 - j * 0.045, 0, 180, width=0.045, color=c))
    ax.add_patch(Wedge((cx, cy), 1.25, 0, 180, color=BASES["뇌록"]))
    for R, n, L, W in [(0.62, 9, 0.62, 0.2), (0.36, 7, 0.56, 0.19)]:  # broad, overlapping rings
        for a in np.linspace(10, 170, n):
            ar = np.radians(a)
            _petal(ax, cx + R * np.cos(ar), cy + R * np.sin(ar), a, L, W, red)
    for a in np.linspace(10 + 160 / 16, 170 - 160 / 16, 8):  # hooks between the outer petal tips
        ar = np.radians(a)
        _hook(ax, cx + 1.12 * np.cos(ar), cy + 1.12 * np.sin(ar), a + 90, 0.09, green)
    for a in np.linspace(5, 175, 8):  # inner ring of short petals
        _petal(ax, cx + 0.2 * np.cos(np.radians(a)), cy + 0.2 * np.sin(np.radians(a)), a, 0.26, 0.09, red)
    ax.add_patch(Circle((cx, cy), 0.27, fc=HWI["황"], ec=INK, lw=1))
    ax.add_patch(Circle((cx, cy), 0.23, fc="none", ec="white", lw=0.6))
    ax.add_patch(Circle((cx, cy), 0.12, fc=HWI["삼청"], ec=INK, lw=0.8))
    _caption(ax, S["c_meoricho"])


# ------------------------------------------------------------- 6. 금문 ----
def geummun(ax):
    _blank(ax, S["t_geummun"])
    ax.set_xlim(-0.6, 7.4); ax.set_ylim(-0.6, 4.4); ax.set_aspect("equal")
    ax.add_patch(Rectangle((-0.6, -0.6), 8, 5, color=BASES["석간주"]))
    r = 0.58  # hexagon circumradius; flat-top tiling
    dx, dy = 1.5 * r, np.sqrt(3) * r
    for j in range(-1, 6):
        for i in range(-1, 9):
            x, y = i * dx, j * dy + (dy / 2 if i % 2 else 0)
            outer, inner = (HWI["황"], HWI["삼청"]) if (i + j) % 2 else (HWI["삼청"], HWI["황"])
            ax.add_patch(RegularPolygon((x, y), 6, radius=r * 0.94, orientation=np.pi / 6, fc="none", ec=outer, lw=2.4))
            ax.add_patch(RegularPolygon((x, y), 6, radius=r * 0.62, orientation=np.pi / 6, fc="none", ec=inner, lw=1.2))
            ax.add_patch(Circle((x, y), r * 0.14, color=HWI["육색"]))
    _caption(ax, S["c_geummun"])


# ------------------------------------------------------ 7. 보통 그래프 ----
def plots_in_dancheong(ax):
    _blank(ax, S["t_plots"])
    cols = DC
    rng = np.random.default_rng(3)
    x = np.arange(6); bottom = np.zeros(6)
    for c in cols:
        v = rng.integers(1, 4, 6); ax.bar(x, v, bottom=bottom, color=c, width=0.7); bottom += v
    for i, c in enumerate(cols):  # the palette strip itself, in band order
        ax.add_patch(Rectangle((i * 6 / len(cols) - 0.5, bottom.max() * 1.08), 6 / len(cols), bottom.max() * 0.12, color=c))
    ax.set_ylim(0, bottom.max() * 1.3); ax.set_xlim(-0.6, 5.6)
    _caption(ax, S["c_plots"])


# --------------------------------------------------------- 8. 배경 글 ----
def photo_panel(filename, key_title, key_caption):
    def fn(ax):
        _blank(ax, S[key_title])
        ax.imshow(plt.imread(ASSETS / filename))
        _caption(ax, S[key_caption])
    fn.__name__ = key_title
    return fn


def text_panel(key_title, key_body):
    def fn(ax):
        _blank(ax, S[key_title])
        ax.text(0, 1, S[key_body], transform=ax.transAxes, va="top", ha="left", fontsize=9, linespacing=1.6)
    fn.__name__ = key_title
    return fn


PANELS = [obang_wheel, ogan_mixes, text_panel("t_bg", "bg"),
          barim, barim_cmaps, hwi,
          meoricho, geummun, plots_in_dancheong,
          photo_panel("gyotaejeon_ceiling_plate_pd.jpg", "t_plate", "c_plate"),
          photo_panel("gyeongbokgung_rafters_ccby4.jpg", "t_photo", "c_photo"),
          photo_panel("geunjeongjeon_brackets_ccbysa4.jpg", "t_stack", "c_stack"),
          text_panel("t_prov", "prov")]


def build(lang="ko"):
    global S, LANG
    S, LANG = STRINGS[lang], lang
    set_style("notebook", "clean")
    plt.rcParams["font.family"] = [plt.rcParams["font.sans-serif"][0], HANGUL]
    fig = plt.figure(figsize=(19, 27))
    gs = fig.add_gridspec(5, 3, height_ratios=[1, 1, 1, 1.35, 0.45], hspace=0.45, wspace=0.25, top=0.965, bottom=0.02, left=0.04, right=0.97)
    slots = [gs[r, c] for r in range(4) for c in range(3)] + [gs[4, :]]
    for fn, slot in zip(PANELS, slots):
        fn(fig.add_subplot(slot))
    fig.suptitle(S["suptitle"], fontfamily=SERIF, fontweight="bold", fontsize=18, y=0.985)
    return fig


if __name__ == "__main__":
    args = sys.argv[1:]
    langs = ["ko", "en"] if "all" in args else [a for a in args if a in STRINGS] or ["ko"]
    rest = [a for a in args if a not in ("all", "ko", "en")]
    for lang in langs:
        out = Path(rest[0]) if rest else GALLERY / ("dancheong.png" if lang == "ko" else f"dancheong_{lang}.png")
        build(lang).savefig(out, dpi=130)
        plt.close("all")
        print("wrote", out)
