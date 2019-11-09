import datetime

from networkx import connected_components

from User import User
import numpy as np
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


def read_data_from_file(filename):
    users = []
    file = open(filename, "r")
    for i, line in enumerate(file):
        if i % 1000 == 0:
            print("Reading " + str(i) + " line")
        user_data = line.strip().split(';')
        if len(user_data[2]) > 0:
            followers = user_data[2].split(',')
        else:
            followers = []
        users.append(User(user_data[0], user_data[1], followers))
    return users


def print_subgraphs(subgraphs):
    for i, graph in enumerate(subgraphs):
        print(datetime.datetime.now())
        print_message("Drawing graph " + str(i))
        plt.figure(3)
        nx.draw(graph)
        plt.savefig('results' + str(i) + '.png')
        plt.show()


if __name__ == "__main__":
    print_message("Loading data")
    # users = read_data_from_file("processed_users.csv")
    users = read_data_from_file("processed_users2.csv")
    # users = read_data_from_file("data.csv")

    print_message(str(len(users)) + " users created")

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

