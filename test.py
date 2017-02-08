import matplotlib.pyplot as plt
import networkx as nx
import operator
import collections

def draw_node_betweenness_plot(file_name,data_name):
    # read in the file

    # create axis
    ax = plt.gca()
    # create legend handles
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)

    styles = ['-ko', '-b^', '-gs', '-r*', '-c+', '-mx']  # line stlyes
    line_labels = ['original', 'k=5', 'k=10', 'k=15', 'k=20', 'k=25']  # line names
    lines = [] # lines
    count_distributions = []


    for index in range(6):
        with open('new_result/' + file_name + '_' + str(index) + '.txt') as f:
            f_lines = f.readlines()
        f_lines = [x.strip() for x in f_lines]
        betweenness_sequence = []
        for idx, line in enumerate(f_lines):
            if idx>0:
                node, betweenness = line.split(' ')
                #print(betweenness)
                betweenness_sequence.append(float(betweenness))
        decimal = 0.001
        betweenness_sequence = [round(b / decimal) * decimal for b in betweenness_sequence]
        betweennessCount = collections.Counter(betweenness_sequence)
        betweennessCount = sorted(betweennessCount.items(), key=operator.itemgetter(0))
        betweennesses, counts = map(list, zip(*betweennessCount))
        print(index)
        line, = ax.plot(betweennesses, counts, styles[index], label=line_labels[index])
        lines.append(line)
        print(lines)
        print('----------------betweenness distribution:' + data_name)
        print(betweennessCount)
        print(betweennesses)
        print(counts)
        count_distributions.append(counts)

    plt.rcParams["figure.figsize"] = [10, 10]

    # linking lines with ledgend
    plt.legend(lines, line_labels,prop={'size': 18})

    # set y-axis to be log-scale
    ax.set_yscale('log')

    # set plot titles, y-label, x-label
    #plt.title("Distribution of Vertex Betweenness:" + data_name +' data')
    plt.ylabel("Num of vertices")
    plt.xlabel("Betweenness")
    plt.gcf().set_facecolor('white')
    plt.rcParams.update({'font.size': 22})
    #plt.margins(0.2, 0.4)
    plt.locator_params(axis='x', nbins=5)
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)


    # save and show plot
    plt.savefig('new_figures/' + data_name + "_betweenness_distribution_new.eps", format='eps', dpi=1000)
    plt.show()



def main():
    draw_node_betweenness_plot('man10000_PagerankRanked_TopK100_betweenness', 'man10000_PagerankRanked_TopK100')

main()