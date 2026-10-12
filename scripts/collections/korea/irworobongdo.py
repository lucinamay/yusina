"""일월오봉도 sheet: the Sun, Moon and Five Peaks screen, its palette, and the
composition logic next to plots in those colours.

    python scripts/collections/korea/irworobongdo.py [ko|en|all]   # -> gallery/collections/korea/irworobongdo[_en].png
"""

from functools import partial

from _sheet import P, artwork, main, names, plots, swatches, text_panel

SRC = "irworobongdo_pd.jpg"
T = {
    "ko": {"sup": "일월오봉도 · 해와 달과 다섯 봉우리", "art": "일월오봉도 병풍", "credit": "조선. Wikimedia Commons File:Irworobongdo.jpg, 퍼블릭 도메인.",
           "pal": "팔레트 `Irworobongdo`", "pal_c": "군청 하늘·물결 · 석록·석청 봉우리 · 주사 해 · 석간주 소나무 줄기 · 호분 달·폭포·물보라 · 먹 윤곽. 국립고궁박물관 설명의 안료, 값은 안료 표에서.",
           "plots": "팔레트로 그린 그래프",            "how": "구도의 논리", "how_b": ("왕의 자리 뒤에만 세우던 병풍이다. 오른쪽에 해, 왼쪽에 달, 가운데 다섯 봉우리, 양 끝에 붉은 줄기의\n"
                                        "소나무, 봉우리 사이로 두 줄기 폭포, 아래에 파도. 해와 달은 음양, 다섯 봉우리는 오행(또는 오악),\n"
                                        "왕은 그 앞에 앉아 구도를 완성한다.\n\n"
                                        "색도 그 논리를 따른다. 하늘과 봉우리의 군청, 해의 적, 달의 백, 소나무의 적·녹, 물결의 백과 청.\n"
                                        "팔레트의 첫 색이 군청인 것은 면적이 가장 넓기 때문이고, 영어 이름은 국립고궁박물관 표기\n"
                                        "Irworobongdo를 그대로 썼다."),
           "prov": "출처와 주의", "prov_b": "이미지: Wikimedia Commons, 퍼블릭 도메인 (8030px 원본, 3200px로 축소), 설명용. 값은 korea_pigments.csv의 안료색, palettes.csv에 고정, collection = Korea."},
    "en": {"sup": "Irworobongdo (일월오봉도) · Sun, Moon and Five Peaks", "art": "Irworobongdo screen", "credit": "Joseon. Wikimedia Commons File:Irworobongdo.jpg, public domain.",
           "pal": "Palette `Irworobongdo`", "pal_c": "ultramarine sky and waves · malachite and azurite peaks · cinnabar sun · iron-oxide pine trunks · shell-white moon, waterfalls and spray · ink outlines. Pigments as the National Palace Museum describes them; values from the pigment table.",
           "plots": "Plots in the palette",            "how": "The logic of the composition", "how_b": ("The screen stood only behind the king's seat. Sun on the right, moon on the left, five peaks in the middle,\n"
                                                           "red-trunked pines at both ends, two waterfalls between the peaks, waves below. Sun and moon are yin and\n"
                                                           "yang, the five peaks the five phases (or five sacred mountains); the king in front completes the picture.\n\n"
                                                           "The colours follow the same logic: ultramarine for sky and peaks, red for the sun, white for the moon, red and\n"
                                                           "green for the pines, white and blue for the waves. Ultramarine leads the palette because it covers the most\n"
                                                           "area. The English name follows the National Palace Museum's romanisation, Irworobongdo."),
           "prov": "Sources and caveats", "prov_b": "Image: Wikimedia Commons, public domain (8030 px original, reduced to 3200 px), illustration only. Values are pigment colours from korea_pigments.csv, frozen in palettes.csv, collection = Korea."},
}


def sheet(lang):
    t = T[lang]; cols = P.get("Irworobongdo")
    panels = [partial(artwork, filename=SRC, title=t["art"], credit=t["credit"]),
              partial(swatches, colours=cols, title=t["pal"], labels=names(cols), text=t["pal_c"]),
              partial(plots, colours=cols, title=t["plots"]),
              partial(text_panel, title=t["how"], body=t["how_b"]),
              partial(text_panel, title=t["prov"], body=t["prov_b"])]
    return panels, t["sup"], {"ncols": 3, "row_heights": [1, 0.8], "figsize": (19, 10)}


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "irworobongdo")
