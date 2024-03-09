from matplotlib import pyplot as plt
import matplotlib.patches as mpatches


def compare(record):
    tasks = 2
    colour = ["orange", "red", "green", "blue", "purple", "brown", "pink", "gray", "olive", "cyan"]
    height = len(record)
    height = height if height > 1 else 2

    try:
        fig, axs = plt.subplots(tasks, height, sharex=True, sharey="row")  # (x,y)
    except ValueError:
        return True
    fig.suptitle('Comparison')

    for y in range(len(record)):  # y refers to the index of each task
        for x in range(tasks):  # x refers to the index of each data set within the task
            axs[x, y].plot(record[y][2], record[y][x])  # iterates through each subplot and plots data in each
            left_colour = (record[y][3][0]/255, record[y][3][1]/255, record[y][3][2]/255)  # colours according to the
            # colour of the original trace
            axs[x, y].spines['left'].set_color(left_colour)
            axs[x, y].spines['bottom'].set_color(colour[x])  # colours according to whether it is x vs time or y vs time
    labels = ["x", "y"]
    patches = []
    for i in range(tasks):  # creates a legend
        patches.append(mpatches.Patch(color=colour[i], label=labels[i]))
    fig.legend(loc=7, handles=[i for i in patches])
    fig.tight_layout()
    fig.subplots_adjust(right=0.9)
    plt.show()
