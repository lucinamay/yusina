colourDict = {
    "discrete": {
        "green": "#B9C311",  # green
        "teal": "#9BC2BA",  # teal
        "purple": "#CFC0D6",  # purple
        "orange": "#FFAD61",  # light orange
        "softred": "#EB6737",  # soft red
        "palegrey": "#D2CEC4",  # pale grey
        "yellow": "#FFEAA0",  # yellow
        "pink": "#FFC4CE",  # pink
        "blue": "#B4CAD8",  # light blue
        "red": "#C21100",  # red
    },
    "continuous": {
        "1": "#081d58",  #'#57BAC0',  # navy,
        "2": "#225ea8",  #'#77BC4D',  # royal blue,
        "3": "#41b6c4",  #'#F3C55F',  # teal,
        "4": "#7fcdbb",  #'#F48861',  # turquoise,
        "10": "#c7e9b4",  #'#797979',  # lemon green,
        "-1": "#c7e9b4",
    },
    "pathways": {
        "purple": "#A783B6",  # purple
        "orange": "#FF8B61",  # orange,
        "green": "#B9C311",  # green,
        "blue": "#6FB5C6",  # blue
        "pink": "#FFC4CE",  # pink
        "yellow": "#FFEAA0",  # yellow
    },
}



def outline(colour, lightness: float = 0.75, saturation: float = 1.3) -> str:
    """Edge colour for a fill: same hue, darker and more saturated. Hex string
    so ``generate`` quotes it in the .mplstyle."""
    import colorsys

    from matplotlib.colors import to_hex, to_rgb

    h, l, s = colorsys.rgb_to_hls(*to_rgb(colour))
    return to_hex(colorsys.hls_to_rgb(h, l * lightness, min(1.0, s * saturation)))
