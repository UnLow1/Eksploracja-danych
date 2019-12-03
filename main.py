import csv
import datetime
import os

from networkx import connected_components

from User import User
import networkx as nx
import matplotlib.pyplot as plt


def print_message(message):
    print("====================================")
    print("\t\t\t" + message)
    print("====================================")


# connect only existing followers
def create_graph(users):
    G = nx.Graph()
    for i, user in enumerate(users):
        if i % 1000 == 0:
            print("Connecting " + str(i) + " user")
        for follower in user.followers:
            G.add_edge(user.id, follower)
    return G

# each follower is a node
# def create_graph(users):
#     fig_size = 50
#     G = nx.Graph()
#     for i, user in enumerate(users):
#         if i % 1000 == 0:
#             print("Connecting " + str(i) + " user")
#         for inner_user in users:
#             if user.id in inner_user.followers:
#                 G.add_edge(user, inner_user)
#     print_message("Drawing graph")
#     plt.figure(3, figsize=(fig_size, fig_size))
#     nx.draw(G, node_size=60)
#     return G


# def create_graph(users, labels):
#     G = nx.Graph()
#     # G.add_node(users[0].id, label=)
#     for i, user in enumerate(users):
#         if i % 1000 == 0:
#             print("Connecting " + str(i) + " user")
#         for follower in user.followers:
#             G.add_edge(user.id, follower)
#     print_message("Drawing graph")
#     nx.draw(G, labels=labels, with_labels=True)
#     return G


def create_labels(users):
    labels = {}
    for user in users:
        labels[user.id] = user.username
    return labels


def read_data_from_file(filename, is_test, only_these_users):
    users = []
    path = 'data'
    if is_test:
        path += '\\test'
    file = open(os.path.join(path, filename), "r")
    for i, line in enumerate(file):
        if i % 1000 == 0:
            print("Reading " + str(i) + " line")
        user_data = line.strip().split(';')
        user_id = user_data[0]
        if only_these_users:
            if user_id in only_these_users:
                if len(user_data[2]) > 0:
                    followers = user_data[2].split(',')
                else:
                    followers = []
                users.append(User(user_id, user_data[1], followers))
                print("1) users = " + str(len(users)))
            elif len(user_data[2]) > 0:
                followers = user_data[2].split(',')
                for user in only_these_users:
                    if user in followers:
                        users.append(User(user_id, user_data[1], followers))
                        print("2) users = " + str(len(users)))
        else:
            if len(user_data[2]) > 0:
                followers = user_data[2].split(',')
            else:
                followers = []
            users.append(User(user_id, user_data[1], followers))
    return users


def print_subgraphs(subgraphs):
    for i, graph in enumerate(subgraphs):
        print(datetime.datetime.now())
        print_message("Drawing graph " + str(i))
        plt.figure(3)
        nx.draw(graph)
        plt.savefig('results' + str(i) + '.png')
        plt.show()


def print_graph_using_networkx(users):
    # print_message("Creating labels for graph")
    # labels = create_labels(users)
    print_message("Creating graph")
    G = create_graph(users)

    subgraphs = (G.subgraph(c) for c in connected_components(G))
    print_subgraphs(subgraphs)

    print_message("Drawing whole graph")
    fig_size = 50
    plt.figure(3, figsize=(fig_size, fig_size))
    nx.draw(G, node_size=60)
    plt.savefig('results.png')
    plt.show()


def create_file_with_nodes(users, filename):
    with open(os.path.join('results', filename + '.csv'), 'w') as nodesFile:
        writer = csv.writer(nodesFile, lineterminator='\n', delimiter=';', skipinitialspace=True)
        writer.writerow(['Id', 'Label'])
        for user in users:
            writer.writerow([user.id, user.username])
    nodesFile.close()


def create_file_with_edges(users, filename):
    with open(os.path.join('results', filename + '.csv'), 'w') as edgesFile:
        writer = csv.writer(edgesFile, lineterminator='\n', delimiter=';', skipinitialspace=True)
        writer.writerow(['Source', 'Target'])
        for user in users:
            for follower in user.followers:
                writer.writerow([user.id, follower])
    edgesFile.close()


def remove_not_imported_followers(users):
    user_ids = []
    for user in users:
        user_ids.append(user.id)
    for i, user in enumerate(users):
        if i % 1000 == 0:
            print("Parsing " + str(i) + " user")
        new_followers = []
        for follower in user.followers:
            if follower in user_ids:
                new_followers.append(follower)
                # user.followers.remove(follower)
        user.followers = new_followers


def crete_whole_graph():
    print_message("Loading data")
    # users = read_data_from_file("processed_users.csv", False, None)
    # users = read_data_from_file("processed_users2.csv", True, None)
    users = read_data_from_file("data.csv", True, None)

    print_message(str(len(users)) + " users created")

    # print_graph_using_networkx(users)

    print_message("Removing not imported followers")
    remove_not_imported_followers(users)

    print_message("Creating file with nodes")
    create_file_with_nodes(users, 'nodes')

    print_message("Creating file with edges")
    create_file_with_edges(users, 'edges')


def read_group(group_id, is_test):
    path = 'data'
    if is_test:
        path += '\\test'
    with open(os.path.join(path, 'clusters_label_propagation' + '.csv'), 'r') as file:
        for line in file:
            id = line.strip().split(';')[0]
            if int(id) == group_id:
                return line.strip().split(';')[1].split(',')


if __name__ == "__main__":
    group_id = 108

    user_ids = read_group(group_id, False)
    users = read_data_from_file("data3.csv", False, user_ids)

    print_message("Creating file with nodes")
    create_file_with_nodes(users, 'nodes')

    print_message("Creating file with edges")
    create_file_with_edges(users, 'edges')

    # crete_whole_graph()
