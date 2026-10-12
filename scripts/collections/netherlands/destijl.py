"""De Stijl: Mondrian's Composition II (1930) as the `DeStijl` palette.

    python scripts/collections/netherlands/destijl.py [nl|en|all]   # -> gallery/collections/netherlands/destijl[_en].png
"""

from _sheet import main, standard_sheet

SRC = "mondrian_composition_ii_1930_pd.jpg"
PAL = "DeStijl"
T = {
    "nl": {"sup": "De Stijl · drie kleuren en drie niet-kleuren",
           "art": "Piet Mondriaan, Compositie II in rood, blauw en geel, 1930", "credit": "Kunsthaus Zürich. Wikimedia Commons File:Piet Mondriaan, 1930 - Mondrian Composition II in Red, Blue, and Yellow.jpg, publiek domein; verkleind tot 2000 px.",
           "pal": f"Palet `{PAL}`", "pal_c": "Mondriaan rood · blauw · geel · zwart · wit. Waarden afgelezen van de scan; de vijf vlakken zijn effen, dus de aflezing is ondubbelzinnig.",
           "plots": "Grafieken in het palet",
           "how": "Een palet bij decreet",
           "how_b": ("De Stijl (1917) bracht de schilderkunst terug tot wat Mondriaan het 'universele' noemde: horizontale en verticale lijnen,\n"
                     "rechthoekige vlakken, en alleen de drie primaire kleuren naast de drie 'niet-kleuren' wit, grijs en zwart. Het is het enige\n"
                     "palet in deze collectie dat door een manifest is vastgelegd in plaats van door een materiaal.\n\n"
                     "Voor grafieken is het streng: drie verzadigde tinten, meer niet. Het past bij drie reeksen die elk hun eigen gewicht moeten\n"
                     "houden; bij meer reeksen moet een ander palet het overnemen."),
           "prov": "Bronnen en kanttekeningen",
           "prov_b": ("Het programma: Mondriaan, De Nieuwe Beelding in de schilderkunst, De Stijl 1 (1917–18). Mondriaan stierf in 1944; zijn werk is sinds 2015\n"
                      "publiek domein in de EU. Waarden afgelezen van de scan van het doek in Zürich; het rood van Mondriaan was in de jaren dertig vaak cadmium,\n"
                      "het blauw kobalt of ultramarijn, maar dit doek is hier niet geanalyseerd.")},
    "en": {"sup": "De Stijl · three colours and three non-colours",
           "art": "Piet Mondrian, Composition II in Red, Blue and Yellow, 1930", "credit": "Kunsthaus Zürich. Wikimedia Commons File:Piet Mondriaan, 1930 - Mondrian Composition II in Red, Blue, and Yellow.jpg, public domain; reduced to 2000 px.",
           "pal": f"Palette `{PAL}`", "pal_c": "Mondrian red · blue · yellow · black · white. Values read off the scan; the five planes are flat, so the reading is unambiguous.",
           "plots": "Plots in the palette",
           "how": "A palette by decree",
           "how_b": ("De Stijl (1917) reduced painting to what Mondrian called the 'universal': horizontal and vertical lines, rectangular planes, and\n"
                     "only the three primaries beside the three 'non-colours' white, grey and black. It is the one palette in this collection fixed by\n"
                     "a manifesto rather than by a material.\n\n"
                     "For plots it is strict: three saturated hues and no more. It suits three series that must each hold their own weight; with more\n"
                     "series another palette has to take over."),
           "prov": "Sources and caveats",
           "prov_b": ("The programme: Mondrian, De Nieuwe Beelding in de schilderkunst, De Stijl 1 (1917–18). Mondrian died in 1944; his work has been public domain\n"
                      "in the EU since 2015. Values read off the scan of the Zürich canvas; Mondrian's red in the 1930s was often cadmium, the blue cobalt or\n"
                      "ultramarine, but this canvas is not analysed here.")},
}


def sheet(lang):
    return standard_sheet(T[lang], SRC, PAL)


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "destijl")
