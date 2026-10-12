"""Vermeer: The Milkmaid as the `Vermeer` palette.

    python scripts/collections/netherlands/vermeer.py [nl|en|all]   # -> gallery/collections/netherlands/vermeer[_en].png
"""

from _sheet import main, standard_sheet

SRC = "vermeer_milkmaid_pd.jpg"
PAL = "Vermeer"
T = {
    "nl": {"sup": "Vermeer · ultramarijn en loodtingeel",
           "art": "Het melkmeisje, ca. 1660", "credit": "Rijksmuseum, SK-A-2344. Wikimedia Commons File:Johannes Vermeer - Het melkmeisje - Google Art Project.jpg, publiek domein; verkleind tot 2000 px.",
           "pal": f"Palet `{PAL}`", "pal_c": "ultramarijn · loodtingeel · meekraprood · broodoker · kalkwit · roet. Identiteit van de pigmenten naar het Rijksmuseum-onderzoek, waarden afgelezen van de scan, uitsnede op de figuur.",
           "plots": "Grafieken in het palet",
           "how": "Het duurste blauw naast het goedkoopste geel",
           "how_b": ("Vermeer gebruikte natuurlijk ultramarijn, gemalen lapis lazuli, zo royaal als geen tijdgenoot: niet alleen voor de rok van het\n"
                     "melkmeisje, maar ook in de schaduwen van de witte muur. Daarnaast loodtingeel voor het lijfje, meekraplak voor de rode\n"
                     "bovenrok, okers voor het brood en de mand, loodwit voor de muur en het licht.\n\n"
                     "Het palet neemt die zes: een diep blauw, een warm geel, een gedempt rood, twee aardtinten en zwart. Blauw en geel voorop,\n"
                     "omdat het schilderij daarmee staat of valt."),
           "prov": "Bronnen en kanttekeningen",
           "prov_b": ("Pigmenten: Rijksmuseum, onderzoek naar Het melkmeisje (2022–23, onderliggende tekening en pigmentanalyse) en de collectietekst; ultramarijn, loodtingeel\n"
                      "en meekrap zijn er vastgesteld. Waarden afgelezen van de Google Art Project-scan, uitgesneden op de figuur; het 'kalkwit' is de muur in het\n"
                      "licht, dus loodwit met een gele zweem, niet het standaardwit.")},
    "en": {"sup": "Vermeer · ultramarine and lead-tin yellow",
           "art": "The Milkmaid, c. 1660", "credit": "Rijksmuseum, SK-A-2344. Wikimedia Commons File:Johannes Vermeer - Het melkmeisje - Google Art Project.jpg, public domain; reduced to 2000 px.",
           "pal": f"Palette `{PAL}`", "pal_c": "ultramarine · lead-tin yellow · madder red · bread ochre · lime white · soot. Pigment identities from the Rijksmuseum research, values read off the scan, cropped to the figure.",
           "plots": "Plots in the palette",
           "how": "The dearest blue beside the cheapest yellow",
           "how_b": ("Vermeer used natural ultramarine, ground lapis lazuli, more freely than any contemporary: not only for the milkmaid's skirt but in\n"
                     "the shadows of the white wall. Beside it lead-tin yellow for the bodice, madder lake for the red overskirt, ochres for the bread\n"
                     "and the basket, lead white for the wall and the light.\n\n"
                     "The palette takes those six: a deep blue, a warm yellow, a muted red, two earths and black. Blue and yellow lead, because the\n"
                     "painting stands or falls with them."),
           "prov": "Sources and caveats",
           "prov_b": ("Pigments: Rijksmuseum, research on The Milkmaid (2022–23, underdrawing and pigment analysis) and the collection text; ultramarine, lead-tin\n"
                      "yellow and madder are established there. Values read off the Google Art Project scan, cropped to the figure; the 'lime white' is the wall in\n"
                      "light, so lead white with a yellow cast, not the standard white.")},
}


def sheet(lang):
    return standard_sheet(T[lang], SRC, PAL, crop=(0.25, 0.2, 0.9, 0.9))


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "vermeer")
