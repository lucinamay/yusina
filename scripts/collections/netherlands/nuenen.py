"""Van Gogh in Nuenen: The Potato Eaters and the Weavers as the `Nuenen` palette.

    python scripts/collections/netherlands/nuenen.py [nl|en|all]   # -> gallery/collections/netherlands/nuenen[_en].png
"""

from _sheet import main, standard_sheet

SRC = "vangogh_potato_eaters_pd.jpg"
PAL = "Nuenen"
T = {
    "nl": {"sup": "Van Gogh, Nuenen 1884–85 · de kleur van een stoffige aardappel",
           "art": "De aardappeleters, april–mei 1885", "credit": "Van Gogh Museum, Amsterdam. Wikimedia Commons File:Vincent van Gogh - The potato eaters - Google Art Project.jpg, publiek domein; verkleind tot 2000 px.",
           "pal": f"Palet `{PAL}`", "pal_c": "lamplicht · aardappeloker · roodbruin · weversgroen · weversbruin · groenzwart · roet. Waarden afgelezen van de museumscans van De aardappeleters en de Wevers.",
           "plots": "Grafieken in het palet",
           "how": "Het donkere palet",
           "how_b": ("Voor hij naar Parijs ging schilderde Van Gogh twee jaar in Nuenen: wevers aan hun getouw, boerenkoppen, en in 1885 De\n"
                     "aardappeleters. Aan Theo schreef hij dat de koppen 'de kleur van een goed stoffige aardappel, ongeschild natuurlijk' moesten\n"
                     "hebben. Het palet is aarde: okers, groene aarde, bruinen, een groenzwarte schaduw en het ene gele lamplicht.\n\n"
                     "Dit is het Brabantse Van Gogh, en het tegendeel van Arles: dezelfde hand, drie jaar eerder, zonder chroomgeel en kobalt. De\n"
                     "twee rijen naast elkaar laten zien wat Parijs en het zuiden met een palet deden."),
           "prov": "Bronnen en kanttekeningen",
           "prov_b": ("Citaat: brief aan Theo, ca. 30 april 1885 (vangoghletters.org, brief 497). Pigmenten van de Nuenense periode: Van Gogh Museum, Van Gogh's Studio\n"
                      "Practice (2013). Waarden afgelezen van kleurbeheerde scans; het schilderij is donker, dus de lezer neemt per tint het schoonste verfvlak, niet de\n"
                      "mediaan van de schaduw.")},
    "en": {"sup": "Van Gogh, Nuenen 1884–85 · the colour of a dusty potato",
           "art": "The Potato Eaters, April–May 1885", "credit": "Van Gogh Museum, Amsterdam. Wikimedia Commons File:Vincent van Gogh - The potato eaters - Google Art Project.jpg, public domain; reduced to 2000 px.",
           "pal": f"Palette `{PAL}`", "pal_c": "lamplight · potato ochre · red-brown · weaver green · weaver brown · green-black · soot. Values read off the museum scans of The Potato Eaters and the Weavers.",
           "plots": "Plots in the palette",
           "how": "The dark palette",
           "how_b": ("Before Paris, Van Gogh painted two years in Nuenen: weavers at their looms, peasant heads, and in 1885 The Potato Eaters. He\n"
                     "wrote to Theo that the heads should have 'the colour of a good dusty potato, unpeeled of course'. The palette is earth: ochres,\n"
                     "green earth, browns, a green-black shadow and the one yellow lamplight.\n\n"
                     "This is the Brabant Van Gogh and the opposite of Arles: the same hand three years earlier, without chrome yellow and cobalt.\n"
                     "The two rows side by side show what Paris and the south did to a palette."),
           "prov": "Sources and caveats",
           "prov_b": ("Quotation: letter to Theo, about 30 April 1885 (vangoghletters.org, letter 497). Pigments of the Nuenen period: Van Gogh Museum, Van Gogh's\n"
                      "Studio Practice (2013). Values read off colour-managed scans; the painting is dark, so the reader takes each hue's cleanest patch of paint,\n"
                      "not the median of the shadow.")},
}


def sheet(lang):
    return standard_sheet(T[lang], SRC, PAL)


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "nuenen")
