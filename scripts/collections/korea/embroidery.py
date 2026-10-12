"""자수 sheet: the dyes of a rank badge (흉배) as the `Bidan` palette, and the hue-changing
thread gradients (바림) as colormaps. Values come from the dye table, not the photo.

    python scripts/collections/korea/embroidery.py [ko|en|all]   # -> gallery/collections/korea/embroidery[_en].png
"""

from functools import partial

from _sheet import (
    P,
    artwork,
    gradients,
    heatmaps,
    main,
    names,
    plots,
    swatches,
    text_panel,
)

SRC = "hyungbae_cranes_met_cc0.jpg"
CMAPS = ["silk_petal", "silk_leaf", "silk_cloud", "silk_feather", "silk_osaek"]
CREDIT = {"ko": "자수 쌍학 흉배, 조선 19세기. 사진: The Metropolitan Museum of Art, CC0 (53.60.9), 하단 바위 부분은 잘라냄.",
          "en": "Embroidered rank badge with a pair of cranes, Joseon, 19th c. Photo: The Metropolitan Museum of Art, CC0 (53.60.9); lower rocks cropped."}
T = {
    "ko": {
        "sup": "자수 · 비단의 색", "art": "쌍학 흉배 (雙鶴胸背)",
        "pal": "팔레트 `Bidan`: 비단에 쓰인 염료", "pal_c": "홍화·쪽·자초·치자·괴화 염색 비단과 소색 명주, 현 테두리. 문헌 설명대로 고른 염료, 값은 `korea_pigments.csv`.",
        "grad": "자수의 바림: 색상이 바뀌는 그라데이션", "grad_c": "꽃잎 소색→연홍→홍→자초, 잎 송화→괴화→쪽, 구름 소색→연홍→자초→쪽, 깃 소색→옥색→쪽→현, 오색 띠 홍→치자→괴화→쪽→자초. 염료 사이를 OKLab으로 보간 (`palettes.through`).",
        "heat": "히트맵에 얹으면",
        "how": "자수의 바림",
        "how_b": ("궁중 자수는 한 모티프를 한 색실로 메우지 않는다. 실을 3~5단계 갈아 끼우며 꽃잎·구름·깃털의 안쪽으로\n"
                  "들어가는데, 그 단계는 밝기만 바뀌는 게 아니라 색상이 바뀐다: 꽃잎은 흰 명주에서 연홍·홍을 지나 자초로,\n"
                  "잎은 송화빛에서 괴화 녹을 지나 쪽으로, 구름은 연홍에서 자초를 지나 쪽으로 간다. 단청의 빛 단계보다 자유롭다.\n\n"
                  "사진에서 값을 읽지 않는 이유: 19세기 비단은 바랬고 박물관 사진의 화이트밸런스도 제각각이다.\n"
                  "대신 자수가 실제로 거치는 염료 순서를 표에서 가져와 그 사이를 보간한다."),
        "prov": "출처와 주의",
        "prov_b": ("염료 값: 국립현대미술관 「한국전통표준색명」의 같은 이름 색(화면 근사값), `korea_pigments.csv`.\n"
                   "컬러맵: silk_petal · leaf · cloud · feather · osaek (colours.py, collection Korea). 염료 순서는 궁중자수 통례. 사진은 전부 설명용."),
    },
    "en": {
        "sup": "Embroidery (자수) · the colours of silk", "art": "Rank badge with a pair of cranes (쌍학 흉배)",
        "pal": "Palette `Bidan`: the dyes used on silk", "pal_c": "Safflower, indigo, gromwell, gardenia and pagoda-tree dyed silks, undyed silk, black border. Dyes chosen from descriptions; values from `korea_pigments.csv`.",
        "grad": "Embroidery shading: gradients that change hue", "grad_c": "petal undyed→light safflower→safflower→gromwell, leaf pine-pollen→pagoda→indigo, cloud undyed→light safflower→gromwell→indigo, feather undyed→jade→indigo→black, five-colour band safflower→gardenia→pagoda→indigo→gromwell. Interpolated between dyes in OKLab (`palettes.through`).",
        "heat": "On heatmaps",
        "how": "Shading in embroidery (바림)",
        "how_b": ("Court embroidery never fills a motif with one thread colour. Threads are changed in three to five steps while\n"
                  "working into a petal, a cloud or a feather, and the steps change hue, not just lightness: a petal runs from\n"
                  "undyed silk through light and full safflower into gromwell purple, a leaf from pine-pollen yellow through\n"
                  "pagoda-tree green into indigo, a cloud from pink through purple into indigo. Freer than dancheong's tone steps.\n\n"
                  "Nothing is read off the photographs: 19th-century silk has faded and museum white balance varies.\n"
                  "Instead the dye sequences the embroiderer actually ran through are taken from the table and\n"
                  "interpolated between."),
        "prov": "Sources and caveats",
        "prov_b": ("Dye values: the MMCA standard colour of the same name (screen approximations), `korea_pigments.csv`.\n"
                   "Colormaps: silk_petal · leaf · cloud · feather · osaek (colours.py, collection Korea). Dye sequences follow court-embroidery convention. Photographs are illustration only."),
    },
}


def sheet(lang):
    t = T[lang]
    panels = [
        partial(artwork, filename=SRC, title=t["art"], credit=CREDIT[lang], crop=(0, 0, 1, 0.74)),
        partial(swatches, colours=P.get("Bidan"), title=t["pal"], labels=names(P.get("Bidan")), text=t["pal_c"]),
        partial(gradients, cmaps=CMAPS, title=t["grad"], text=t["grad_c"]),
        partial(heatmaps, cmaps=CMAPS, title=t["heat"]),
        partial(plots, colours=P.get("Bidan"), title=t["pal"]),
        partial(text_panel, title=t["how"], body=t["how_b"]),
        partial(text_panel, title=t["prov"], body=t["prov_b"]),
    ]
    return panels, t["sup"], {"ncols": 3, "row_heights": [1.2, 1, 0.7], "figsize": (19, 15)}


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "embroidery")
