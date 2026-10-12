"""Portul din Maramureș: the striped zadie and the beaded zgărdan as the `Maramures` palette.

    python scripts/collections/romania/maramures.py [ro|en|all]   # -> gallery/collections/romania/maramures[_en].png
"""

from _sheet import P, main, standard_sheet

SRC = "maramures_zgardan_ccbysa40.jpg"
PAL = "Maramures"
T = {
    "ro": {"sup": "Portul din Maramureș · zadia și zgărdanul",
           "art": "Zgărdan de mărgele pe ie, Maramureș", "credit": "Foto: CEllen, Wikimedia Commons File:Traditional costumes details Maramures (2).jpg, CC BY-SA 4.0; redusă la 2000 px.",
           "pal": f"Paleta `{PAL}`", "pal_c": "roșu de zadie · mărgele violet · negru · mărgele albastre · verde de zadie · mărgele roz · alb de in · mărgele bleu, galbene, jad. Valori eșantionate din două fotografii ale portului.",
           "extra_t": "Zadia: lână, dungi, sintetic", "extra_c": "Cele două zadii (șorțuri) sunt țesute în dungi: negru cu roșu sau cu galben, după sat și după vârstă. Lâna e vopsită sintetic de la sfârșitul sec. XIX.",
           "plots": "Grafice în paletă",
           "how": "Cât de vechi e 'modernul'",
           "how_b": ("Coloranții sintetici au ajuns în satele românești la vreo douăzeci de ani după sinteza lor: fuxina (1856), alizarina sintetică\n"
                     "(1871), verdele briliant (1879). Spre 1900 roșul și verdele aprins ale zadiei erau deja paleta satului; roibă, indigo și rezedă\n"
                     "rămăseseră în lăzile bunicilor.\n\n"
                     "Zgărdanul, gulerul de mărgele de sticlă cu margini drepte (în Bucovina sunt zimțate), și lătițarul, banda de catifea neagră cu\n"
                     "mărgele, poartă aceleași culori vii. Portul se îmbracă și azi, duminica și la sărbători: paleta aceasta e tradiția vie, nu una\n"
                     "reconstruită. Paleta de dinainte de anilină stă în rândul `Oltenia`."),
           "prov": "Surse și limite",
           "prov_b": ("Trecerea la coloranții sintetici: Petroviciu et al., Heritage 6 (2023) 505–523, pe cămăși din Valea Hârtibaciului. Zadia și zgărdanul: codanec.eu,\n"
                      "Accesorii tradiționale din Maramureș; eliznik.org.uk, Women's jewellery. Valorile sunt eșantionate din fotografii de festival, la lumină de zi;\n"
                      "nu există o analiză a coloranților pentru aceste piese.")},
    "en": {"sup": "The Maramureș costume · the zadie and the zgărdan",
           "art": "Beaded zgărdan over an ie, Maramureș", "credit": "Photo: CEllen, Wikimedia Commons File:Traditional costumes details Maramures (2).jpg, CC BY-SA 4.0; reduced to 2000 px.",
           "pal": f"Palette `{PAL}`", "pal_c": "zadie red · violet beads · black · blue beads · zadie green · pink beads · linen white · periwinkle, yellow and jade beads. Values sampled from two photographs of the costume.",
           "extra_t": "The zadie: wool, stripes, synthetic dye", "extra_c": "The two aprons are woven in stripes, black with red or with yellow, by village and by age. The wool has been dyed synthetically since the late 19th century.",
           "plots": "Plots in the palette",
           "how": "How old 'modern' is",
           "how_b": ("Synthetic dyes reached Romanian villages some twenty years after their synthesis: fuchsine (1856), synthetic alizarin (1871),\n"
                     "brilliant green (1879). By 1900 the bright red and green of the zadie were already the village palette; madder, indigo and\n"
                     "weld had retired to the grandmothers' chests.\n\n"
                     "The zgărdan, a collar of glass beads with straight edges (scalloped in Bucovina), and the lătițar, a black velvet band sewn with\n"
                     "beads, carry the same bright colours. The costume is still worn on Sundays and feast days: this palette is the living tradition,\n"
                     "not a reconstruction. The pre-aniline palette sits in the `Oltenia` row."),
           "prov": "Sources and caveats",
           "prov_b": ("The shift to synthetic dyes: Petroviciu et al., Heritage 6 (2023) 505–523, on shirts from the Hârtibaciu valley. Zadie and zgărdan: codanec.eu,\n"
                      "Traditional accessories from Maramureș; eliznik.org.uk, Women's jewellery. Values are sampled from festival photographs in daylight; no dye\n"
                      "analysis exists for these pieces.")},
}


def sheet(lang):
    zadie = ["#A80D25", "#005D1E", "#211F1E", "#F3EFE6"]  # zadie red and green, black, linen; all in the palette
    assert all(c in P.get(PAL) for c in zadie)
    return standard_sheet(T[lang], SRC, PAL, extra=(zadie, ["roșu", "verde", "negru", "alb"] if lang == "ro" else ["red", "green", "black", "white"]))


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "maramures")
