import matplotlib.pyplot as plt
import numpy as np

class Plot:

    def plot_number(self,data):

        labels = list(data.keys())
        python_count = [int(da[0]) for da in list(data.values())]
        pachyderm_count = [int(da[1]) for da in list(data.values())]

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, python_count, width, label='Python')
        rects2 = ax.bar(x + width/2, pachyderm_count, width, label='Pachyderm')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Number of files')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.axes.xaxis.set_visible(False)
        ax.legend()

        fig.tight_layout()

        plt.show()

    def plot_number_lines(self,data1,data2,title):
        plt.clf()
        fig, axs = plt.subplots(2)
        def set(data,xl,yl,ax):
            x1 = range(len(list(data.keys())))
            y1 = [int(da[0]) for da in list(data.values())]
            y1.reverse()
            ax.plot(x1, y1, label = "Python")
            x2 = range(len(list(data.keys())))
            y2 = [int(da[1]) for da in list(data.values())]
            y2.reverse()
            ax.plot(x2, y2, label = "Pachyderm")
            ax.set_xlabel(xl)
            ax.set_ylabel(yl)
            ax.legend()
        set(data1,'','Number of Files',axs[0])
        set(data2,'Commits','Lines of Code',axs[1])
        fig.suptitle(title)
        # Display a figure.
        # plt.show()
        # Save the figure
        plt.savefig(f'/home/lofowl/Desktop/cisc834_group/mining/figures/merge_version/{title}-merge.png')


    def plot(self,data):
        fig, axs = plt.subplots(len(data.keys()))
        index = 0
        for file,count in data.items():
            length = len(count)
            add_count = [int(data[0]) for data in count]
            delete_count = [int(data[1]) for data in count]
            x = np.arange(length)  # the label locations
            width = 0.2  # the width of the bars


            rects1 = axs[index].bar(x - width/2, add_count, width, label='add')
            rects2 = axs[index].bar(x + width/2, delete_count, width, label='delete')

            # Add some text for labels, title and custom x-axis tick labels, etc.
            axs[index].set_title(file)
            axs[index].set_xticks(x)
            axs[index].set_yticks([1,5,10])
            axs[index].axes.yaxis.set_visible(False)
            axs[index].axes.xaxis.set_visible(False)


            def autolabel(rects,ax):
                for rect in rects:
                    height = rect.get_height()
                    ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                            '%d' % int(height),
                            ha='center', va='bottom')

            autolabel(rects1,axs[index])
            autolabel(rects2,axs[index])


            # disable the frame 
            axs[index].spines['top'].set_visible(False)
            axs[index].spines['right'].set_visible(False)
            axs[index].spines['left'].set_visible(False)
            index += 1

        fig.tight_layout()

        plt.show()



if __name__ == "__main__":
    print("Plot")