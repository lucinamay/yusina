"""Cimitirul Vesel din Săpânța: the painted oak crosses as the `Sapanta` palette.

    python scripts/collections/romania/sapanta.py [ro|en|all]   # -> gallery/collections/romania/sapanta[_en].png
"""

from _sheet import main, standard_sheet

SRC = "sapanta_crosses_ccbysa30.jpg"
PAL = "Sapanta"
T = {
    "ro": {"sup": "Cimitirul Vesel, Săpânța · albastrul de Săpânța",
           "art": "Cruci de stejar pictate, Săpânța, Maramureș", "credit": "Foto: Andrei Stroe, Wikimedia Commons File:RO MM Sapanta merry cemetery 3.jpg, CC BY-SA 3.0; redusă la 2000 px.",
           "pal": f"Paleta `{PAL}`", "pal_c": "albastru de Săpânța · galben · turcoaz · roșu · verde · negru · ocru · alb. Valori eșantionate din fotografia a două cruci, la lumină de zi.",
           "plots": "Grafice în paletă",
           "how": "Un cimitir cu culori",
           "how_b": ("Din 1935 Stan Ioan Pătraș a cioplit și pictat crucile de stejar ale satului: un acoperiș, un relief naiv cu meseria sau sfârșitul\n"
                     "celui îngropat, și o epitafie în versuri, la persoana întâi, adesea cu haz. După moartea lui (1977) ucenicul Dumitru Pop a dus\n"
                     "mai departe atelierul.\n\n"
                     "Fondul e același peste tot, 'albastrul de Săpânța', albastrul cerului și al speranței în povestirea obișnuită a locului; pe el,\n"
                     "verdele vieții, galbenul rodului, roșul patimii, negrul morții. Vopseaua e de ulei, pe lemn; paleta e, deci, un amestec de atelier,\n"
                     "nu un pigment istoric."),
           "prov": "Surse și limite",
           "prov_b": ("Istoria atelierului și semnificațiile culorilor: descrierile curente ale Cimitirului Vesel (Muzeul Țăranului Român, ghiduri); nu există o analiză\n"
                      "a vopselelor. Valorile sunt eșantionate dintr-o fotografie, pe două cruci: fața însorită și cea în umbră dau două albastruri, aici e cel mediu.")},
    "en": {"sup": "The Merry Cemetery, Săpânța · the Săpânța blue",
           "art": "Painted oak crosses, Săpânța, Maramureș", "credit": "Photo: Andrei Stroe, Wikimedia Commons File:RO MM Sapanta merry cemetery 3.jpg, CC BY-SA 3.0; reduced to 2000 px.",
           "pal": f"Palette `{PAL}`", "pal_c": "Săpânța blue · yellow · turquoise · red · green · black · ochre · white. Values sampled from the photograph of two crosses in daylight.",
           "plots": "Plots in the palette",
           "how": "A cemetery in colour",
           "how_b": ("From 1935 Stan Ioan Pătraș carved and painted the village's oak crosses: a little roof, a naive relief of the trade or the end of\n"
                     "the person buried, and a rhymed epitaph in the first person, often funny. After his death (1977) his apprentice Dumitru Pop\n"
                     "carried the workshop on.\n\n"
                     "The ground is the same everywhere, the 'Săpânța blue', the blue of the sky and of hope in the usual telling; on it, the green of\n"
                     "life, the yellow of fertility, the red of passion, the black of death. The paint is oil on wood, so the palette is a workshop\n"
                     "mix, not a historical pigment."),
           "prov": "Sources and caveats",
           "prov_b": ("Workshop history and colour meanings: the usual accounts of the Merry Cemetery (Romanian Peasant Museum, guides); no paint analysis exists.\n"
                      "Values are sampled from one photograph, two crosses: the sunlit and the shaded faces give two blues, the middle one is used here.")},
}


def sheet(lang):
    return standard_sheet(T[lang], SRC, PAL, crop=(0.1, 0.3, 0.9, 0.95))


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "sapanta")
