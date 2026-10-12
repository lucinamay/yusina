"""Scoarța oltenească: natural-dyed wool of a late 18th-century rug as the `Oltenia` palette.

    python scripts/collections/romania/oltenia.py [ro|en|all]   # -> gallery/collections/romania/oltenia[_en].png
"""

from _sheet import main, standard_sheet

SRC = "oltenia_carpet_detail_ccbysa40.jpg"
PAL = "Oltenia"
T = {
    "ro": {"sup": "Scoarța oltenească · lână vopsită cu plante",
           "art": "Scoarță din Oltenia, sfârșitul sec. XVIII sau începutul sec. XIX (detaliu)", "credit": "Foto: Joe Mabel, Wikimedia Commons File:Carpet - Oltenia - late 18th- or early 19th-century - detail.jpg, CC BY-SA 4.0; redusă la 2000 px.",
           "pal": f"Paleta `{PAL}`", "pal_c": "roz de roibă · indigo · galben de rezedă · mov · albastru de lână · piersică · lână nealbită. Valori eșantionate din fotografia covorului; numele vopselelor sunt cele obișnuite ale epocii, nu analize.",
           "plots": "Grafice în paletă",
           "how": "Vopselele dinainte de anilină",
           "how_b": ("Până spre 1880 lâna se vopsea cu ce creștea pe lângă casă: roibă (Rubia tinctorum) pentru roșu și roz, indigo adus de negustori\n"
                     "pentru albastru închis, rezedă și drobiță pentru galben, coji de nucă pentru brun, frunze de nuc cu alaun pentru verde,\n"
                     "cârmâz (coșenilă) importat pentru roz-carmin. Plantele se fierbeau, iar culoarea se fixa cu alaun.\n\n"
                     "Scoarța oltenească, țesută în tehnica chilimului, cu motive vegetale și 'pomul vieții', ține culorile acestea pe un fond\n"
                     "indigo sau roșu. Paleta de aici e a unui singur covor, bine păstrat, de muzeu: lână de două secole, deci mai moale decât\n"
                     "vopseaua proaspătă."),
           "prov": "Surse și limite",
           "prov_b": ("Rețete de vopsit: eliznik.org.uk, Threads and dyes. Identificarea coloranților pe textile românești de sec. XIX–XX (LC–MS): Petroviciu et al.,\n"
                      "Heritage Science 7 (2019), pe piese ASTRA Sibiu. Pentru acest covor nu există analiză; numele vopselelor din paletă sunt atribuiri după culoare\n"
                      "și epocă, nu identificări. Valorile sunt eșantionate dintr-o fotografie de muzeu.")},
    "en": {"sup": "The Oltenian rug · plant-dyed wool",
           "art": "Oltenia rug, late 18th or early 19th century (detail)", "credit": "Photo: Joe Mabel, Wikimedia Commons File:Carpet - Oltenia - late 18th- or early 19th-century - detail.jpg, CC BY-SA 4.0; reduced to 2000 px.",
           "pal": f"Palette `{PAL}`", "pal_c": "madder pink · indigo · weld yellow · mauve · wool blue · peach · raw wool. Values sampled from the photograph of the rug; the dye names are the usual ones of the period, not analyses.",
           "plots": "Plots in the palette",
           "how": "The dyes before aniline",
           "how_b": ("Until about 1880 wool was dyed with what grew nearby: madder (Rubia tinctorum) for red and pink, indigo brought by traders for\n"
                     "dark blue, weld and dyer's broom for yellow, walnut husks for brown, walnut leaves with alum for green, imported cochineal\n"
                     "for carmine pink. The plants were boiled and the colour fixed with alum.\n\n"
                     "The Oltenian rug, flat-woven in kilim technique with plant motifs and the tree of life, carries these colours on an indigo\n"
                     "or red ground. The palette here is one well-kept museum rug: two-century-old wool, so softer than fresh dye."),
           "prov": "Sources and caveats",
           "prov_b": ("Dye recipes: eliznik.org.uk, Threads and dyes. Dye identification on 19th–20th-century Romanian textiles (LC–MS): Petroviciu et al., Heritage\n"
                      "Science 7 (2019), on ASTRA Sibiu pieces. This rug has not been analysed; the dye names in the palette are attributions by colour and period,\n"
                      "not identifications. Values are sampled from a museum photograph.")},
}


def sheet(lang):
    return standard_sheet(T[lang], SRC, PAL)


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "oltenia")
