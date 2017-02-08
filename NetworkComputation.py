from __future__ import division
import networkx as nx
import scipy.stats as stat
from sklearn.metrics import jaccard_similarity_score

import csv

def calculate_metrics (filename):
    # 1. read in edge list data
    G = nx.read_edgelist(filename + ".edgelist", nodetype=int)  # preprocessed_facebook_combined
    print('successfully read the nodes:')
    node_degrees = G.degree(G.nodes())


    #print(G.nodes())

    # 2. calculate all shortest paths
    path = nx.all_pairs_shortest_path(G)


    #shortest_paths = []
    node_shortest_path = []
    path_id = []
    id = 0
    for node1 in G.nodes():
        for node2 in G.nodes():
            path_id.append(id)
            id += 1
            if node2 in path[node1]:
                node_shortest_path.append(len(path[node1][node2]))
            else:
                node_shortest_path.append(-1)
        #shortest_paths.append(node_shortest_path)
    print('successfully calculate all shortest paths...')
    #print(node_shortest_path)
    #with open("paths_" + filename +".csv", "wb") as f:
        #writer = csv.writer(f, delimiter=',')
        #writer.writerows(shortest_paths)

    # 3. calculate metrics of nodes
    node_betweenness_centralities = nx.betweenness_centrality(G)
    node_closeness_centrality = nx.closeness_centrality(G)
    node_result = zip(G.nodes(), node_betweenness_centralities.values(), node_closeness_centrality.values())
    print('successfully calculate node metrics...')

    metrics = {}
    metrics['shortest_paths'] = node_shortest_path
    metrics['path_id'] = path_id
    metrics['node_metrics'] = node_result
    metrics['betweenness'] = node_betweenness_centralities.values()
    metrics['closeness'] = node_closeness_centrality.values()
    metrics['node_degrees'] = node_degrees
    return metrics

    #with open("nodes_" + filename + ".csv", "wb") as f:
        #writer = csv.writer(f, delimiter=',')
        #writer.writerows(node_result)


def test_difference(file1, file2):
    metrics1 =  calculate_metrics(file1)
    metrics2 =  calculate_metrics(file2)
    shortest_path1 = metrics1['shortest_paths']
    shortest_path2 = metrics2['shortest_paths']

   # print(shortest_path1)
   # print(shortest_path2)

    # 1. wicoxon-test
    print('======Wicoxon tests======')

    # node degree wicoxon-test
    node_degrees1 = metrics1['node_degrees']
    node_degrees2 = metrics2['node_degrees']
    diffs = []
    for key, value in node_degrees1.iteritems():

        # if shortest_path1[index] == -1 or shortest_path2[index] == -1:
        # continue
        # else:
        diffs.append(node_degrees1[key] - node_degrees2[key])
    # print(diffs)
    w_value = stat.wilcoxon(diffs)
    print ("When comparing node  degrees, the wilcoxon value:" + str(w_value))

    # shortest path wicoxon-test
    diffs =[]
    for index, value in enumerate(shortest_path1):
        #if shortest_path1[index] == -1 or shortest_path2[index] == -1:
            #continue
        #else:
        diffs.append(shortest_path1[index] - shortest_path2[index] )
    #print(diffs)
    w_value = stat.wilcoxon(diffs)
    print ("When comparing shortest paths, the wilcoxon value:" + str(w_value))


    # node betweenness wicoxon-test
    diffs = []
    for index, value in enumerate( metrics1['betweenness']):
        diffs.append( metrics1['betweenness'][index]-metrics2['betweenness'][index])
    w_value = stat.wilcoxon(diffs)
    print ("When comparing betweenness, the wilcoxon value:" + str(w_value))


    # node closeness wicoxon-test
    diffs = []
    for index, value in enumerate(metrics1['closeness']):
        diffs.append(metrics1['closeness'][index] - metrics2['closeness'][index])
    w_value = stat.wilcoxon(diffs)
    print ("When comparing closeness, the wilcoxon value:" + str(w_value))

    # 2. intersection
    print('======intersection tests======')
    top_N_percentage = 0.01
    # path intersection
    shortest_paths1 = zip( metrics1['path_id'], metrics1['shortest_paths'])
    shortest_paths2 = zip( metrics2['path_id'], metrics2['shortest_paths'])
    shortest_paths1 = sorted(shortest_paths1, key=lambda x: x[1],reverse=True)
    shortest_paths2 = sorted(shortest_paths2, key=lambda x: x[1], reverse=True)

    #print(shortest_paths1)
    #print(shortest_paths2)

    # node degree intersection


    import operator
    node_degrees1 = sorted(node_degrees1.items(), key=operator.itemgetter(1), reverse=True)
    node_degrees2 = sorted(node_degrees2.items(), key=operator.itemgetter(1), reverse=True)


    count = 0
    id_1 = []

    for key, value in enumerate(node_degrees1):
        id_1.append(value[0])
        count += 1
        if count >= len(node_degrees1) * top_N_percentage:
            break
    id_1 = set(id_1)
    # print(id_1)
    count = 0
    id_2 = []
    for key, value in enumerate(node_degrees2):
        id_2.append(value[0])
        count += 1
        if count >= len(node_degrees1) * top_N_percentage:
            break
    id_2 = set(id_2)
    # print(id_2)
    intersection_set = id_1.intersection(id_2)
    union_set = id_1.union(id_2)

    # print(intersection_set)
    print('the percentage of intersection of node degrees = ' + str(
        len(intersection_set) / (len(id_1))) + ', jaccard similarity = ' + str(len(intersection_set) / len(union_set)))



    #print(len(shortest_paths1))
    count = 0
    id_1 = []
    for id, path in shortest_paths1:
        id_1.append(id)
        count += 1
        if count >= len(shortest_paths1) * top_N_percentage:
            break
    id_1 = set(id_1)
    #print(id_1)
    count = 0
    id_2 = []
    for id, path in shortest_paths2:
        id_2.append(id)
        count += 1
        if count >= len(shortest_paths2) * top_N_percentage:
            break
    id_2 = set(id_2)
    #print(id_2)
    intersection_set = id_1.intersection(id_2)
    union_set = id_1.union(id_2)

    #print(intersection_set)
    print('the percentage of intersection of paths= ' + str(len(intersection_set)/(len(id_1))) + ', jaccard similarity = ' +  str(len(intersection_set)/len(union_set)))


    # node betweenness intersection
    nodes1 = metrics1['node_metrics']
    nodes1 = sorted(nodes1, key=lambda x: x[1], reverse=True)
    nodes2 = metrics2['node_metrics']
    nodes2 = sorted(nodes2, key=lambda x: x[1], reverse=True)
    #print(nodes1)
    #print(nodes2)
    count = 0
    id_1 = []
    for id, betweenness, closeness in nodes1:
        id_1.append(id)
        count += 1
        if count >= len(nodes1) * top_N_percentage:
            break
    id_1 = set(id_1)
    # print(id_1)
    count = 0
    id_2 = []
    for id, betweenness, closeness in nodes2:
        id_2.append(id)
        count += 1
        if count >= len(nodes1) * top_N_percentage:
            break
    id_2 = set(id_2)
    # print(id_2)
    intersection_set = id_1.intersection(id_2)
    union_set = id_1.union(id_2)
    # print(intersection_set)
    print('the percentage of intersection of node betweenness= ' + str(len(intersection_set) / len(id_1))+ ', jaccard similarity = ' +  str(len(intersection_set)/len(union_set)))


    # node closeness intersection
    nodes1 = metrics1['node_metrics']
    nodes1 = sorted(nodes1, key=lambda x: x[2], reverse=True)
    nodes2 = metrics2['node_metrics']
    nodes2 = sorted(nodes2, key=lambda x: x[2], reverse=True)
    count = 0
    id_1 = []
    for id, betweenness, closeness in nodes1:
        id_1.append(id)
        count += 1
        if count >= len(nodes1) * top_N_percentage:
            break
    id_1 = set(id_1)
    # print(id_1)
    count = 0
    id_2 = []
    for id, betweenness, closeness in nodes2:
        id_2.append(id)
        count += 1
        if count >= len(nodes1) * top_N_percentage:
            break
    id_2 = set(id_2)
    # print(id_2)
    intersection_set = id_1.intersection(id_2)
    union_set = id_1.union(id_2)
    # print(intersection_set)
    print('the percentage of intersection of node closeness= ' + str(len(intersection_set) / len(id_1))+ ', jaccard similarity = ' +  str(len(intersection_set)/len(union_set)))

    # 3. average repositioning
    print('======repositioning tests======')
    # node degree
    node_degree_dict1 = {}
    count = 0
    for key, value in enumerate(node_degrees1):
        node_degree_dict1[value[0]] = count
        count += 1

    diffs = []
    count = 0
    for key, value in enumerate(node_degrees2):
        diff = abs(node_degree_dict1[value[0]] - count)
        count += 1
        diffs.append(diff)
        # if count >= len(shortest_paths1) * top_N_percentage:
        # break

    avg_value = (sum(diffs) / len(diffs)) / (len(node_degrees1))
    print('the average repositioning of node degrees = ' + str(avg_value))

    # path
    path_dict1 = {}
    count = 0
    for id, path in shortest_paths1:
        path_dict1[id] = count
        count += 1

    diffs = []
    count = 0
    for id, path in shortest_paths2:
        diff = abs(path_dict1[id] - count)
        count += 1
        diffs.append(diff)
        #if count >= len(shortest_paths1) * top_N_percentage:
            #break

    avg_value = (sum(diffs) / len(diffs)) / (len(shortest_paths1) )
    print('the average repositioning of paths = ' + str(avg_value))

    # betweenness
    nodes1 = sorted(nodes1, key=lambda x: x[1], reverse=True)
    nodes2 = sorted(nodes2, key=lambda x: x[1], reverse=True)
    node_dict1 = {}
    count = 0
    for id, betweenness, closeness in nodes1:
        node_dict1[id] = count
        count += 1

    diffs = []
    count = 0
    for  id, betweenness, closeness in nodes2:
        diff = abs(node_dict1[id] - count)
        count += 1
        diffs.append(diff)
        #if count >= len(nodes1) * top_N_percentage:
            #break
    avg_value = (sum(diffs) / len(diffs)) / (len(nodes1))
    print('the average repositioning of betweenness = ' + str(avg_value))

    # closeness
    nodes1 = sorted(nodes1, key=lambda x: x[2], reverse=True)
    nodes2 = sorted(nodes2, key=lambda x: x[2], reverse=True)
    node_dict1 = {}
    count = 0
    for id, betweenness, closeness in nodes1:
        node_dict1[id] = count
        count += 1

    diffs = []
    count = 0
    for  id, betweenness, closeness in nodes2:
        diff = abs(node_dict1[id] - count)
        count += 1
        diffs.append(diff)
        #if count >= len(nodes1) * top_N_percentage:
            #break
    avg_value = (sum(diffs) / len(diffs) )/(len(nodes1) )
    print('the average repositioning of closeness = ' + str(avg_value))



def main():
    file1 = 'preprocessed_facebook_combined' # preprocessed_facebook_combined
    file2 = 'facebook-100percent-noise' # facebook-100percent-noise
    test_difference(file1, file2)

main()
