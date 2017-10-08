import math
import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# Grid helper funcions:

def getGridFor(n_items, n_cols = 4):
    return getGrid(math.ceil(n_items / n_cols), n_cols)

def getGrid(n_rows, n_cols):
    plt.figure(random.randrange(0, 1000), figsize=(n_cols * 8, n_rows * 6))

    return gridspec.GridSpec(n_rows, n_cols, hspace=0.75, wspace=0.25)