import matplotlib.pyplot as plt

plot_colors = ['#000000', '#bc2122', '#55679e', '#69b628', '#dacf2f', '#ff6600']


def set_latex_mpl_format(font_size = 15):
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = font_size
    # To have math like LaTeX
    plt.rcParams['mathtext.fontset'] = 'cm'
    plt.rcParams['mathtext.rm'] = 'serif'
