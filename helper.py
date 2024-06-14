import matplotlib.pyplot as plt

def setup_plot():
    plt.ion()
    fig, ax = plt.subplots()
    line1, = ax.plot([], [], label='AI 1')
    line2, = ax.plot([], [], label='AI 2')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Score')
    ax.set_title('Scores Over Episodes')
    ax.legend()
    return fig, ax, line1, line2

def update_plot(ax, line1, line2, scores1, scores2):
    line1.set_ydata(scores1)
    line2.set_ydata(scores2)
    line1.set_xdata(range(len(scores1)))
    line2.set_xdata(range(len(scores2)))
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.01)
