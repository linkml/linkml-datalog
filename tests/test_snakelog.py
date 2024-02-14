from typing import Iterable, Tuple

import pytest
from snakelog.common import *
from snakelog.litelog import Solver, TEXT

@pytest.fixture
def solver():
    return Solver()


def tree_edges(node: str, depth: int, num_children: int = 3) -> Iterable[Tuple[str, str]]:
    if depth == 0:
        return
    for i in range(num_children):
        child = f"{node}.{i}"
        yield node, child
        yield from tree_edges(child, depth-1, num_children)


@pytest.mark.parametrize("depth", [1, 2, 5, 10])
@pytest.mark.parametrize("num_children", [2, 3])
def test_snakelog(solver, depth, num_children):
    """
    TODO: change from benchmark to test

    :param solver:
    :param depth:
    :param num_children:
    :return:
    """
    s = solver
    x, y, z = Vars("x y z")
    edge = s.Relation("edge", TEXT, TEXT)
    path = s.Relation("path", TEXT, TEXT)
    indirect_path = s.Relation("indirect_path", TEXT, TEXT)

    for e in tree_edges("a", depth, num_children):
        s.add(Atom("edge", e))
    s.add(path(x, y) <= edge(x, y))
    s.add(path(x, z) <= path(x, y) & path(y, z))
    s.add(indirect_path(x, y) <= path(x, y) & Not(edge(x, y)))
    s.run()

    s.cur.execute("SELECT * FROM indirect_path")
    paths = list(s.cur.fetchall())
    print(f"\nDepth: {depth}, NChildren: {num_children} Num paths: {len(paths)}")


def test_unbound(solver):
    """
    Tests unbounded

    :param solver:
    :param depth:
    :param num_children:
    :return:
    """
    s = solver
    x, y, z = Vars("x y z")
    (u,) = Vars("u")
    edge = s.Relation("edge", TEXT, TEXT, TEXT)
    path = s.Relation("path", TEXT, TEXT)

    for e in tree_edges("a", 2, 2):
        s.add(Atom("edge", [e[0], "parent", e[1]]))
    s.add(path(x, y) <= edge(x, Var("u"), y))
    s.add(path(x, z) <= edge(x, u, y) & path(y, z))
    s.run()

    s.cur.execute("SELECT * FROM path")
    paths = list(s.cur.fetchall())
    print(len(paths))
    for p in paths:
        print(p)
    assert len(paths) == 10


def test_bound(solver):
    """
    Tests bounded in args

    :param solver:
    :param depth:
    :param num_children:
    :return:
    """
    s = solver
    x, y, z, u = Vars("x y z u")
    edge = s.Relation("edge", TEXT, TEXT, TEXT)
    path = s.Relation("path", TEXT, TEXT)

    for e in tree_edges("a", 2, 2):
        s.add(Atom("edge", [e[0], "parent", e[1]]))
    s.add(path(x, y) <= edge(x, "parent", y))
    s.add(path(x, z) <= edge(x, "parent", y) & path(y, z))
    s.run()

    s.cur.execute("SELECT * FROM path")
    paths = list(s.cur.fetchall())
    print(len(paths))
    for p in paths:
        print(p)
    assert len(paths) == 10
