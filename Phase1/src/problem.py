"""Classical weighted Max-Cut helpers; no Qiskit dependency required yet."""
from itertools import product


def cut_value(nodes, edges, partition):
    """Return total weight of edges crossing a binary partition.

    Args:
        nodes: iterable of node labels.
        edges: iterable of dictionaries with u, v, weight.
        partition: mapping node -> 0 or 1.
    """
    node_set = set(nodes)
    if set(partition) != node_set:
        raise ValueError("partition must assign every node exactly once")
    if any(bit not in (0, 1) for bit in partition.values()):
        raise ValueError("partition values must be 0 or 1")

    total = 0.0
    for edge in edges:
        u, v, weight = edge["u"], edge["v"], float(edge["weight"])
        if u not in node_set or v not in node_set:
            raise ValueError(f"edge ({u}, {v}) refers to an unknown node")
        if u == v:
            raise ValueError("self-loops are not supported in this starter")
        if weight < 0:
            raise ValueError("this starter expects non-negative edge weights")
        if partition[u] != partition[v]:
            total += weight
    return total


def exact_max_cut(nodes, edges, max_nodes=24):
    """Exhaustively find the exact optimum for a small graph.

    Fixing the first node to 0 avoids checking the equivalent complementary
    partition. This is exponential and is only intended for small instances.
    """
    nodes = list(nodes)
    if not nodes:
        raise ValueError("graph must contain at least one node")
    if len(set(nodes)) != len(nodes):
        raise ValueError("node labels must be unique")
    if len(nodes) > max_nodes:
        raise ValueError(
            f"exact enumeration limited to {max_nodes} nodes; "
            "use an appropriate optimizer for larger instances"
        )

    best_value = float("-inf")
    best_partition = None
    first, rest = nodes[0], nodes[1:]
    for bits in product((0, 1), repeat=len(rest)):
        partition = {first: 0, **dict(zip(rest, bits))}
        value = cut_value(nodes, edges, partition)
        if value > best_value:
            best_value, best_partition = value, partition
    return best_value, best_partition
