import networkx as nx
import tqdm
from wmutils.collections.safe_dict import SafeDict

with open('./day-23/input.txt', 'r') as input_file:
    edges = [line.strip().split("-") for line in input_file]

G = nx.Graph(edges)

found_cliques = set()
for node in G.nodes:
    nbs = set(G.neighbors(node))

    for nb in nbs:
        nb_nbs = set(G.neighbors(nb))
        cliques = nbs.intersection(nb_nbs)
        cliques = [[node, nb, cl_nb] for cl_nb in cliques]
        cliques = [sorted(clique, key=lambda node: hash(node))
                   for clique in cliques]
        cliques = [tuple(clique) for clique in cliques]
        found_cliques.update(cliques)

found_cliques = sorted(list(found_cliques))

total1 = 0
for clique in found_cliques:
    if any(ele[0] == 't' for ele in clique):
        total1 += 1

# 2478 is too high
# 1476
print(f'{total1=}')


# p2
my_nbs: SafeDict[str, set] = SafeDict(default_value=set)
for clique in found_cliques:
    for node in clique:
        my_nbs[node].update(clique)
my_nbs = dict(my_nbs)

for key in G.nodes:
    if key[0] == 't':
        del my_nbs[key]

visited = set()
to_visit = set()
to_visit.update((node,) for node in my_nbs.keys())
largest_cluster = set()
largest_task_list = 0
tracker = tqdm.tqdm()
while len(to_visit) > 0:

    # progress bar stuff
    largest_task_list = max(len(to_visit), largest_task_list)
    tracker.n += 1
    if tracker.n % 500 == 0:
        msg = f'{len(to_visit)=}, ' + \
            f'{largest_task_list=}, {len(largest_cluster)=}'
        tracker.set_description(msg)
        tracker.refresh()

    cluster: set = to_visit.pop()
    visited.add(cluster)

    if len(cluster) > len(largest_cluster):
        largest_cluster = cluster

    # select candidate for expansion.
    for node, nbs in my_nbs.items():
        if node in cluster:
            continue

        # must be connected to whole cluster.
        whole_cluster_in_nbs = all(cl_node in nbs for cl_node in cluster)
        if not whole_cluster_in_nbs:
            continue

        new_cluster = [*cluster, node]
        new_cluster = sorted(new_cluster)
        new_cluster = tuple(new_cluster)
        if not new_cluster in visited:
            to_visit.add(new_cluster)

tracker.close()


largest_cluster = sorted(largest_cluster)
password = ','.join(largest_cluster)

# eh,ik,jp,ml,oq,qe,rj,te,tl,uw,vy,ze incorrect
# aj,cl,cx,dj,gq,ho,hp,qk,re,tb,tv,zr incorrect
# fc,fg,fp,fz,gn,io,ni,td,ws,xm,yl,zg incorrect
# ca,dw,fo,if,ji,kg,ks,oe,ov,sb,ud,vr,xr
print(f'{len(largest_cluster)=}')
print(f'{password=}')
