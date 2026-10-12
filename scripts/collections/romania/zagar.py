"""Mobilierul pictat săsesc: a painted dresser from the Zagăr museum as the `Zagar` palette.

    python scripts/collections/romania/zagar.py [ro|en|all]   # -> gallery/collections/romania/zagar[_en].png
"""

from _sheet import main, standard_sheet

SRC = "zagar_saxon_dresser_ccbysa30ro.jpg"
PAL = "Zagar"
T = {
    "ro": {"sup": "Mobilier pictat săsesc · fondul albastru",
           "art": "Dulap pictat, Muzeul etnografic săsesc din Zagăr", "credit": "Foto: Țetcu Mircea Rareș, Wikimedia Commons File:Biserica evanghelica din Zagar (21).JPG, CC BY-SA 3.0 ro; redusă la 2000 px.",
           "pal": f"Paleta `{PAL}`", "pal_c": "albastru săsesc · roșu · albastru închis · verde-albastru · cărămiziu. Valori eșantionate din fotografia dulapului, în lumina camerei.",
           "plots": "Grafice în paletă",
           "how": "Lăzi, dulapuri, paturi",
           "how_b": ("Sașii transilvăneni și-au pictat mobila de zestre din sec. XVIII până la începutul sec. XX: lăzi, dulapuri, paturi și bănci, cu\n"
                     "fond albastru sau verde-albastru, peste care vin lalele, garoafe și trandafiri în roșu, alb și ocru, uneori cu anul și\n"
                     "inițialele miresei. Fiecare sat avea atelierul și tipul lui de floare.\n\n"
                     "Muzeul din Zagăr (Mureș), așezat în biserica evanghelică fortificată, păstrează interioare întregi. Paleta ia dulapul din fotografie:\n"
                     "fondul albastru domină, roșul și cărămiziul sunt florile și chenarele, verdele-albastru și albastrul închis sunt umbrele\n"
                     "aceluiași fond."),
           "prov": "Surse și limite",
           "prov_b": ("Descrierea mobilierului pictat săsesc: literatura etnografică curentă (Muzeul ASTRA, Sibiu; muzeele sătești săsești). Vopselele nu sunt analizate;\n"
                      "valorile vin dintr-o fotografie de interior, la lumină mixtă, deci nuanțele albastre sunt aproximative. Un pigment plauzibil pentru fond e\n"
                      "albastrul de Prusia sau smaltul, dar nu e verificat aici.")},
    "en": {"sup": "Saxon painted furniture · the blue ground",
           "art": "Painted dresser, Transylvanian Saxon ethnographic museum, Zagăr", "credit": "Photo: Țetcu Mircea Rareș, Wikimedia Commons File:Biserica evanghelica din Zagar (21).JPG, CC BY-SA 3.0 ro; reduced to 2000 px.",
           "pal": f"Palette `{PAL}`", "pal_c": "Saxon blue · red · dark blue · teal · brick. Values sampled from the photograph of the dresser in room light.",
           "plots": "Plots in the palette",
           "how": "Chests, dressers, beds",
           "how_b": ("Transylvanian Saxons painted their dowry furniture from the 18th to the early 20th century: chests, dressers, beds and benches,\n"
                     "on a blue or blue-green ground, with tulips, carnations and roses in red, white and ochre, often with the year and the bride's\n"
                     "initials. Each village had its workshop and its own flower.\n\n"
                     "The Zagăr museum (Mureș county), housed in the fortified Lutheran church, keeps whole interiors. The palette takes the dresser in\n"
                     "the photograph: the blue ground dominates, red and brick are the flowers and borders, teal and dark blue are the shadows of the\n"
                     "same ground."),
           "prov": "Sources and caveats",
           "prov_b": ("Saxon painted furniture: the usual ethnographic literature (ASTRA Museum, Sibiu; Saxon village museums). The paints are not analysed; the values\n"
                      "come from one interior photograph in mixed light, so the blues are approximate. Prussian blue or smalt is a plausible pigment for the ground,\n"
                      "but not verified here.")},
}


def sheet(lang):
    return standard_sheet(T[lang], SRC, PAL, crop=(0.3, 0.1, 0.85, 0.95))


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "zagar")
