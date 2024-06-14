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


# WIP

# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors

# # Define the color palette
# discrete_palette = list(colourDict["discrete"].values())

# # Create a color map
# continuous_cmap = mcolors.LinearSegmentedColormap.from_list(
#     "continuous", list(colourDict["continuous"].values())
# )

# # Example usage
# x = [1, 2, 3, 4, 5]
# y = [1, 4, 9, 16, 25]

# # Plot using the color palette and colormap
# fig, ax = plt.subplots()
# ax.scatter(x, y, c=x, cmap=continuous_cmap)
# ax.set_prop_cycle('color', discrete_palette)
# plt.show()
