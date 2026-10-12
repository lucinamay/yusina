"""Bisericile pictate din Bucovina: the shared fresco pigments as the `Bucovina` palette,
the ground colour that names each church, and plots in those colours.

    python scripts/collections/romania/frescoes.py [ro|en|all]   # -> gallery/collections/romania/frescoes[_en].png
"""

from _sheet import P, main, standard_sheet

SRC = "voronet_last_judgement_ccbysa20.jpg"
PAL = "Bucovina"
GROUNDS = [("Voroneț", "#55829E"), ("Sucevița", "#597C56"), ("Humor", "#8D4638"), ("Moldovița", "#B69770")]  # church -> its ground colour in the palette
T = {
    "ro": {"sup": "Bisericile pictate din Bucovina · aceiași pigmenți, alt fond",
           "art": "Voroneț, Judecata de Apoi (peretele de vest, 1547)",
           "credit": "Foto: Alastair Rae, Wikimedia Commons File:Last Judgement (1336873129).jpg, CC BY-SA 2.0; redusă la 1600 px.",
           "pal": f"Paleta `{PAL}` · pigmenții frescei moldovenești",
           "pal_c": "azurit · ocru roșu · albastru închis · negru · pământ verde · alb de var · ocru galben. Identitatea pigmenților din analizele pXRF/FTIR; "
                    "valorile eșantionate din fotografiile zidurilor (Voroneț, Sucevița), vopseaua cea mai curată a fiecărei familii de nuanță, `romania_pigments.csv`.",
           "extra_t": "Fondul fiecărei biserici", "extra_c": "Albastrul de Voroneț este azurit; Sucevița, verde (smaltul albastru găsit acolo s-a decolorat afară); Humor, ocru roșu; Moldovița, ocru galben și auriu.",
           "plots": "Grafice în paletă",
           "how": "De ce arată la fel și totuși diferit",
           "how_b": ("Cele opt biserici pictate la exterior (1530–1600, Petru Rareș și urmașii) folosesc aceeași tehnică și același set de pigmenți:\n"
                     "fresca pe var proaspăt, cu pământuri (ocru roșu, ocru galben, pământ verde), minerale scumpe pentru accente (azurit, cinabru,\n"
                     "smalt), var pentru lumini și cărbune pentru contururi.\n\n"
                     "Diferența este fondul: culoarea pe care sunt așezate registrele. La Voroneț peretele de vest este azurit aproape neîntrerupt,\n"
                     "de aceea 'albastru de Voroneț'. Sucevița e verde, Humor roșu-brun, Moldovița galben-auriu. Paleta începe cu azuritul pentru că\n"
                     "acoperă cea mai mare suprafață; cele patru fonduri sunt a doua lectură a aceleiași palete."),
           "prov": "Surse și limite",
           "prov_b": ("Pigmenți: studiu pXRF/FTIR al albastrurilor din pictura murală medievală românească (azurit la Voroneț și Humor, smalt la Sucevița);\n"
                      "pământ verde, ocruri, cinabru, alb de var, negru de cărbune = setul standard al frescei bizantine, confirmat pe alte monumente din Moldova.\n"
                      "Fondurile după descrierile curente (UNESCO, ghiduri); nu există o analiză publicată a verdelui de la Sucevița. Valorile hex sunt\n"
                      "eșantionate din fotografii: zidul de azi, nu pigmentul proaspăt.")},
    "en": {"sup": "Painted churches of Bucovina · the same pigments, a different ground",
           "art": "Voroneț, the Last Judgement (west wall, 1547)",
           "credit": "Photo: Alastair Rae, Wikimedia Commons File:Last Judgement (1336873129).jpg, CC BY-SA 2.0; reduced to 1600 px.",
           "pal": f"Palette `{PAL}` · the Moldavian fresco pigments",
           "pal_c": "azurite · red ochre · dark blue · carbon black · green earth · lime white · yellow ochre. Pigment identities from the pXRF/FTIR analyses; "
                    "values sampled from the photographs of the walls (Voroneț, Sucevița), the cleanest paint of each hue family, `romania_pigments.csv`.",
           "extra_t": "Each church's ground", "extra_c": "Voroneț blue is azurite; Sucevița green (the smalt found there has discoloured outdoors); Humor red ochre; Moldovița yellow ochre and gold.",
           "plots": "Plots in the palette",
           "how": "Why they look alike and yet different",
           "how_b": ("The eight churches painted outside (1530–1600, Petru Rareș and his successors) share one technique and one pigment set:\n"
                     "fresco on fresh lime, with earths (red ochre, yellow ochre, green earth), costly minerals for accents (azurite, cinnabar,\n"
                     "smalt), lime for highlights and charcoal for outlines.\n\n"
                     "The difference is the ground: the colour the registers sit on. At Voroneț the west wall is nearly unbroken azurite, hence\n"
                     "'Voroneț blue'. Sucevița is green, Humor red-brown, Moldovița golden yellow. The palette leads with azurite because it covers\n"
                     "the largest area; the four grounds are a second reading of the same palette."),
           "prov": "Sources and caveats",
           "prov_b": ("Pigments: a pXRF/FTIR study of blues in medieval Romanian murals (azurite at Voroneț and Humor, smalt at Sucevița); green earth,\n"
                      "ochres, cinnabar, lime white and carbon black are the standard Byzantine fresco set, confirmed on other Moldavian monuments.\n"
                      "Grounds follow the usual descriptions (UNESCO, guides); no published analysis of the Sucevița green was found. Hex values are\n"
                      "sampled from the photographs: today's wall, not fresh pigment.")},
}


def sheet(lang):
    assert all(c in P.get(PAL) for _, c in GROUNDS)
    return standard_sheet(T[lang], SRC, PAL, extra=([c for _, c in GROUNDS], [c for c, _ in GROUNDS]))


if __name__ == "__main__":
    main({lang: sheet(lang) for lang in T}, "frescoes")
