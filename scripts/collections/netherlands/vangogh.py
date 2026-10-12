"""Van Gogh in Arles: The Bedroom and the Sunflowers as the `VanGogh` palette.

    python scripts/collections/netherlands/vangogh.py [nl|en|all]   # -> gallery/collections/netherlands/vangogh[_en].png
"""

from _sheet import main, standard_sheet

SRC = "vangogh_bedroom_pd.jpg"
PAL = "VanGogh"
T = {
    "nl": {"sup": "Van Gogh, Arles 1888 · chroomgeel tegen kobalt",
           "art": "De slaapkamer, oktober 1888", "credit": "Van Gogh Museum, Amsterdam. Wikimedia Commons File:Vincent van Gogh - De slaapkamer - Google Art Project.jpg, publiek domein; verkleind tot 2000 px.",
           "pal": f"Palet `{PAL}`", "pal_c": "kobaltblauw · smaragdgroen · oranje · ultramarijn · oker · vermiljoen · olijf · chroomgeel. Waarden afgelezen van de museumscans van De slaapkamer en de Zonnebloemen (`netherlands_pigments.csv`).",
           "plots": "Grafieken in het palet",
           "how": "Kleur als rust",
           "how_b": ("Over De slaapkamer schreef Van Gogh aan Theo (oktober 1888) dat de kleur hier alles moest doen en 'rust of slaap in het\n"
                     "algemeen' moest suggereren: muren bleek violet, vloer rood, bed en stoelen botergeel, deken scharlaken, raam groen. De\n"
                     "muren zijn door het verbleken van de rode lak nu blauw; het palet neemt het schilderij zoals het vandaag hangt.\n\n"
                     "De pigmenten van het Arles-jaar zijn goed gedocumenteerd: chroomgeel, kobaltblauw, Frans ultramarijn, smaragdgroen,\n"
                     "vermiljoen, zinkwit, geraniumlak. Het palet begint met kobalt; het chroomgeel staat achteraan, omdat het op wit te licht is om een\n"
                     "reeks te dragen (contrast onder 3:1)."),
           "prov": "Bronnen en kanttekeningen",
           "prov_b": ("Pigmenten: Van Gogh Museum, Van Gogh's Studio Practice (2013) en de brieven, vangoghletters.org (brief 705, oktober 1888). Waarden zijn\n"
                      "afgelezen van kleurbeheerde museumscans; chroomgeel is sinds 1888 donkerder geworden en de rode lak op de muren verbleekt, dus dit is het\n"
                      "schilderij van nu, niet van 1888.")},
    "en": {"sup": "Van Gogh, Arles 1888 · chrome yellow against cobalt",
           "art": "The Bedroom, October 1888", "credit": "Van Gogh Museum, Amsterdam. Wikimedia Commons File:Vincent van Gogh - De slaapkamer - Google Art Project.jpg, public domain; reduced to 2000 px.",
           "pal": f"Palette `{PAL}`", "pal_c": "cobalt blue · emerald green · orange · ultramarine · ochre · vermilion · olive · chrome yellow. Values read off the museum scans of The Bedroom and the Sunflowers (`netherlands_pigments.csv`).",
           "plots": "Plots in the palette",
           "how": "Colour as rest",
           "how_b": ("Of The Bedroom Van Gogh wrote to Theo (October 1888) that colour had to do everything here and suggest 'rest or sleep in\n"
                     "general': walls pale violet, floor red, bed and chairs butter yellow, blanket scarlet, window green. The walls are now blue\n"
                     "because the red lake has faded; the palette takes the painting as it hangs today.\n\n"
                     "The pigments of the Arles year are well documented: chrome yellow, cobalt blue, French ultramarine, emerald green, vermilion,\n"
                     "zinc white, geranium lake. The palette opens with cobalt; the chrome yellow comes last, because on white it is too\n"
                     "pale to carry a series (contrast under 3:1)."),
           "prov": "Sources and caveats",
           "prov_b": ("Pigments: Van Gogh Museum, Van Gogh's Studio Practice (2013) and the letters, vangoghletters.org (letter 705, October 1888). Values are read\n"
                      "off colour-managed museum scans; chrome yellow has darkened since 1888 and the red lake on the walls has faded, so this is the painting of\n"
                      "today, not of 1888.")},
}


def sheet(lang):
    return standard_sheet(T[lang], SRC, PAL)


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "vangogh")
