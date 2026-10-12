"""Ceramica de Horezu: the five named colours of the glaze as the `Horezu` palette.

    python scripts/collections/romania/horezu.py [ro|en|all]   # -> gallery/collections/romania/horezu[_en].png
"""

from _sheet import main, standard_sheet

SRC = "horezu_plates_ccbysa30.jpg"
PAL = "Horezu"
T = {
    "ro": {"sup": "Ceramica de Horezu · ivoriu, brun, cobalt, verde",
           "art": "Farfurii de Horezu, cocoșul și spirala", "credit": "Foto: Bogdan29roman, Wikimedia Commons File:Ceramică Horezu doi.jpg, CC BY-SA 3.0; redusă la 2000 px.",
           "pal": f"Paleta `{PAL}`", "pal_c": "ivoriu de Horezu · brun · cobalt · bleu · verde de cupru · negru. Cele cinci culori pe care le numește dosarul UNESCO; valorile eșantionate din fotografie (`romania_pigments.csv`).",
           "plots": "Grafice în paletă",
           "how": "Cum se face",
           "how_b": ("Vasul se trage pe roată, se usucă, se acoperă cu angobă de culoarea ivoriului și se decorează cu cornul (un corn de vită cu o pană\n"
                     "de gâscă, pentru linii) și cu gaița (o pensulă subțire, pentru 'jirăvit', tragerea culorilor una prin alta). Două arderi: una după\n"
                     "decor, una după smalț.\n\n"
                     "Motivele: cocoșul de Horezu, peștele, șarpele, pomul vieții, spirala. Culorile vin din oxizi: brun din mangan și fier, albastru din\n"
                     "cobalt, verde din cupru; 'ivoriul de Horezu' este angoba. Meșteșugul a fost înscris de UNESCO în 2012 (dosar 00610)."),
           "prov": "Surse și limite",
           "prov_b": ("Descrierea tehnicii și a culorilor: UNESCO, Craftsmanship of Horezu ceramics (00610), 2012. Valorile sunt eșantionate dintr-o singură fotografie\n"
                      "de la o tarabă, în umbră: ivoriul iese mai cenușiu decât smalțul la lumină. O fotografie de muzeu, la lumină controlată, ar îndrepta asta.")},
    "en": {"sup": "Horezu ceramics · ivory, brown, cobalt, green",
           "art": "Horezu plates, the rooster and the spiral", "credit": "Photo: Bogdan29roman, Wikimedia Commons File:Ceramică Horezu doi.jpg, CC BY-SA 3.0; reduced to 2000 px.",
           "pal": f"Palette `{PAL}`", "pal_c": "Horezu ivory · brown · cobalt · light blue · copper green · black. The five colours the UNESCO file names; values sampled from the photograph (`romania_pigments.csv`).",
           "plots": "Plots in the palette",
           "how": "How it is made",
           "how_b": ("The pot is thrown, dried, covered with an ivory slip and decorated with the horn (a cow horn fitted with a goose quill, for lines)\n"
                     "and the brush (for 'jirăvit', dragging one colour through another). Two firings: one after decoration, one after glazing.\n\n"
                     "Motifs: the Horezu rooster, the fish, the snake, the tree of life, the spiral. The colours are oxides: brown from manganese and\n"
                     "iron, blue from cobalt, green from copper; 'Horezu ivory' is the slip. UNESCO inscribed the craft in 2012 (file 00610)."),
           "prov": "Sources and caveats",
           "prov_b": ("Technique and colours: UNESCO, Craftsmanship of Horezu ceramics (00610), 2012. Values are sampled from one market-stall photograph\n"
                      "in shade, so the ivory reads greyer than the glaze in daylight. A museum photograph under controlled light would correct that.")},
}


def sheet(lang):
    return standard_sheet(T[lang], SRC, PAL, crop=(0, 0, 1, 0.55))


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "horezu")
