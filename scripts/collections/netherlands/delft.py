"""Delfts blauw: cobalt on tin glaze as the continuous `delft` colormap (no categorical palette).

    python scripts/collections/netherlands/delft.py [nl|en|all]   # -> gallery/collections/netherlands/delft[_en].png
"""

from functools import partial

from _sheet import artwork, gradients, heatmaps, main, text_panel

SRC = "delft_plate_1921_cc0.jpg"
CMAPS = ["delft", "delft_r"]
T = {
    "nl": {"sup": "Delfts blauw · één kleur, alle tinten",
           "art": "Herdenkingsbord, Delft 1921", "credit": "Rijksmuseum, NG-2003-85. Wikimedia Commons File:Dat Eyken de roem van Henley wordt, NG-2003-85.jpg, CC0; verkleind tot 2000 px.",
           "grad": "Colormap `delft` · van tinglazuur naar kobalt", "grad_c": "Zeven stappen, in OKLab geïnterpoleerd door de kobaltwassingen die van het bord zijn afgelezen (`gradient_from_image`), net als de zijdeladders van de Koreaanse borduurkaart.",
           "heat": "Op een heatmap",
           "how": "Waarom geen palet",
           "how_b": ("Delfts aardewerk (vanaf ca. 1620) imiteert Chinees porselein met één kleur: kobaltoxide, geschilderd op het nog ongebakken\n"
                     "tinglazuur, dat bij het bakken blauw wordt. Alles wat het bord vertelt, vertelt het met de dikte van die ene kleur: dunne\n"
                     "wassingen voor luchten en schaduw, dikke lijnen voor contouren.\n\n"
                     "Een categorisch palet heeft meerdere tinten nodig; Delfts blauw heeft er één en alle lichtheden ervan. Daarom is Delft hier\n"
                     "een colormap, zoals de `silk_*`-ladders van de Koreaanse collectie: licht naar donker, voor dichtheden, rasters en heatmaps."),
           "prov": "Bronnen en kanttekeningen",
           "prov_b": ("Techniek: Rijksmuseum, Delfts aardewerk (collectieteksten). De stappen zijn afgelezen van één bord uit 1921, dus van later, industrieel Delfts;\n"
                      "een 17e-eeuws stuk uit de Rijksmuseumcollectie zou een iets warmer, grijzer blauw geven. De lichtste wassingen zijn bijna kleurloos en\n"
                      "worden door de lezer overgeslagen; het wit is het standaardwit van de bibliotheek.")},
    "en": {"sup": "Delft blue · one colour, every shade",
           "art": "Commemorative plate, Delft 1921", "credit": "Rijksmuseum, NG-2003-85. Wikimedia Commons File:Dat Eyken de roem van Henley wordt, NG-2003-85.jpg, CC0; reduced to 2000 px.",
           "grad": "Colormap `delft` · from tin glaze to cobalt", "grad_c": "Seven stops, OKLab-interpolated through the cobalt washes read off the plate (`gradient_from_image`), like the silk ladders of the Korean embroidery sheet.",
           "heat": "On a heatmap",
           "how": "Why not a palette",
           "how_b": ("Delftware (from about 1620) imitates Chinese porcelain with one colour: cobalt oxide painted on the unfired tin glaze, which turns\n"
                     "blue in the kiln. Everything the plate says, it says with the thickness of that one colour: thin washes for skies and shadow,\n"
                     "thick lines for outlines.\n\n"
                     "A categorical palette needs several hues; Delft blue has one, and all its lightnesses. So Delft is a colormap here, like the\n"
                     "`silk_*` ladders of the Korea collection: light to dark, for densities, grids and heatmaps."),
           "prov": "Sources and caveats",
           "prov_b": ("Technique: Rijksmuseum, Delftware (collection texts). The stops are read off one plate from 1921, so from later, industrial Delftware; a\n"
                      "17th-century piece from the Rijksmuseum collection would give a slightly warmer, greyer blue. The lightest washes are nearly achromatic and\n"
                      "the reader skips them; the white is the library's standard white.")},
}


def sheet(lang):
    t = T[lang]
    panels = [(partial(artwork, filename=SRC, title=t["art"], credit=t["credit"], crop=(0.1, 0.05, 0.9, 0.95)), 1),
              (partial(text_panel, title=t["how"], body=t["how_b"]), 2),
              partial(gradients, cmaps=CMAPS, title=t["grad"], text=t["grad_c"]),
              (partial(heatmaps, cmaps=CMAPS, title=t["heat"]), 2),
              (partial(text_panel, title=t["prov"], body=t["prov_b"]), 3)]
    return panels, t["sup"], {"ncols": 3, "row_heights": [1.3, 0.9, 0.45], "figsize": (19, 14)}


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "delft")
