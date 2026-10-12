"""민화·궁중장식화 sheet: famous screens, the pigments each is described with as a
palette, and a contemporary reading. Values come from the pigment table, never
from the photographs.

    python scripts/collections/korea/minhwa.py [ko|en|all]   # -> gallery/collections/korea/minhwa[_en].png
"""

from functools import partial

from _sheet import P, artwork, main, names, plots, swatches, text_panel

WORKS = [  # (palette, asset or None, title ko, title en, credit ko, credit en)
    ("Jangsikhwa", "sipjangsaengdo_6447_pd.jpg", "십장생도 병풍", "Ten Symbols of Longevity (십장생도)",
     "조선 19세기, 창덕궁 소장 (국립고궁박물관). Wikimedia Commons, 퍼블릭 도메인.", "Joseon, 19th c., Changdeokgung Palace (National Palace Museum). Wikimedia Commons, public domain."),
    ("Hwajo", None, "궁모란도·화조도 (사진 없음)", "Peonies, birds and flowers (모란도·화조도), no image",
     "", ""),
]
T = {
    "ko": {"sup": "민화와 궁중장식화 · 그림 한 점이 팔레트 하나", "pal": "팔레트 `{}`",
           "noimg": "공개 이미지가 없어 그림은 싣지 않는다.\n안료는 박물관 해설과 장식화 통례에서:\n{}",
           "pal_c": "같은 안료로 그린 그림은 한 팔레트: 십장생도·요지연도 등 궁중 병풍 → `Jangsikhwa`, 모란도·화조도 → `Hwajo`. 값은 안료 표(`korea_pigments.csv`), 사진은 보여줄 뿐이다.",
           "plots": "팔레트 `{}`로 그린 그래프", "how": "장식화의 안료",
           "how_b": ("조선 후기 장식화(병풍)는 안료를 아끼지 않았다. 17~20세기 회화 채색안료 연구(서울역사박물관 소장 17점 μ-XRF)는\n"
                     "청색 석청·회청, 녹색 석록, 적색 주사·연단·석간주, 황색 자황·밀타승, 백색 연분, 흑색 먹, 그리고 장식화에만\n"
                     "나타나는 금·은을 보고한다. 청록산수의 봉우리는 석록 위에 석청을 올렸고, 19세기 말부터 양록·양청이 섞인다.\n\n"
                     "그래서 이 시트의 팔레트는 사진이 아니라 그 목록에서 나온다. 어떤 안료가 어디에 쓰였는지는 박물관 해설과\n"
                     "문헌이, 값은 안료 표가 정한다. 바랜 그림과 제각각인 사진의 화이트밸런스는 그렇게 비켜 간다."),
           "prov": "출처와 주의",
           "prov_b": ("안료 목록: 「조선중기 이후 회화의 채색안료 연구: 17~20C 초상화, 기록화, 장식화를 중심으로」(학위논문, ScienceON DIKO0012155968);\n"
                      "「신구법천문도 채색 안료 비교」(보존과학회지 2020, 석청·청화·석록·주·석간주·연지). 작품별 배치는 박물관 해설과 통례.\n"
                      "안료 hex: 국립현대미술관 표준색명의 같은 이름 색(화면 근사값), 군청·삼청은 안료 견본값. 모란도는 이미지 없이 문헌만으로.")},
    "en": {"sup": "Minhwa and court decorative painting · one painting, one palette", "pal": "Palette `{}`",
           "noimg": "No open-licence image, so none is shown.\nPigments from museum texts and genre convention:\n{}",
           "pal_c": "Paintings made with the same pigments share one palette: court screens such as longevity and banquet scenes → `Jangsikhwa`, peonies and birds → `Hwajo`. Values from the pigment table (`korea_pigments.csv`); the photo only illustrates.",
           "plots": "Plots in palette `{}`", "how": "The pigments of decorative painting",
           "how_b": ("Late-Joseon decorative screens did not economise on pigment. A μ-XRF study of 17 paintings (17th to 20th c.,\n"
                     "Seoul Museum of History) reports azurite and smalt for blue, malachite for green, cinnabar, red lead and iron oxide\n"
                     "for red, orpiment and litharge for yellow, lead white, ink, and gold and silver found only in decorative works.\n"
                     "Blue-green peaks were azurite laid over malachite; emerald green and Prussian blue appear from the late 19th c.\n\n"
                     "So the palettes here come from that list, not from the photographs. Museum texts and the literature say which\n"
                     "pigment went where; the pigment table supplies the value. Faded paint and inconsistent white balance are sidestepped."),
           "prov": "Sources and caveats",
           "prov_b": ("Pigment lists: 'Colouring pigments of Joseon painting after the mid period: portraits, documentary and decorative painting,\n"
                      "17th to 20th c.' (thesis, ScienceON DIKO0012155968); 'Comparison of pigments in old and new celestial-chart screens'\n"
                      "(J. Conservation Science 2020). Placement per work follows museum texts and genre conventions. Pigment hex: MMCA\n"
                      "standard colour of the same name (screen approximation), ultramarine and samcheong as pigment swatches. The peony screen has no image.")},
}


def sheet(lang):
    """One column per palette: the work above, its swatches, then plots in it."""
    t = T[lang]; k = 2 if lang == "ko" else 3; c = 4 if lang == "ko" else 5
    top, mid, low = [], [], []
    for i, (pal, f, *rest) in enumerate(WORKS):
        if f:
            top.append(partial(artwork, filename=f, title=rest[k - 2], credit=rest[c - 2]))
        else:
            top.append(partial(text_panel, title=rest[k - 2], body=t["noimg"].format(" · ".join(names(P.get(pal))))))
        cols = P.get(pal)
        mid.append(partial(swatches, colours=cols, title=t["pal"].format(pal), labels=names(cols), text=t["pal_c"] if i == 0 else None))
        low.append(partial(plots, colours=cols, title=t["plots"].format(pal), seed=i))
    panels = top + mid + low + [partial(text_panel, title=t["how"], body=t["how_b"]), partial(text_panel, title=t["prov"], body=t["prov_b"])]
    return panels, t["sup"], {"ncols": len(WORKS), "row_heights": [1.1, 0.5, 0.9, 1.0], "figsize": (18, 17)}


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "minhwa")
