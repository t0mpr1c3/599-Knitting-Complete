"""Tests that generate simple knit graph visualizations"""
from debugging_tools.knit_graph_viz import visualize_knitGraph
from debugging_tools.simple_knitgraphs import *


def test_stockinette():
    visualize_knitGraph(stockinette(4, 4))


def test_rib():
    visualize_knitGraph(rib(5, 4, 1))


def test_seed():
    visualize_knitGraph(seed(4, 4))


def test_twisted_stripes():
    visualize_knitGraph(twisted_stripes(4, 5))


def test_lace():
    visualize_knitGraph(lace(4, 4))


def test_standard():
    visualize_knitGraph(standard(6, 4))


def test_jacquard():
    visualize_knitGraph(jacquard(6, 4))


def test_birdseye():
    visualize_knitGraph(birdseye(8, 4))


def test_birdseye_3():
    visualize_knitGraph(birdseye_3(6, 4))


if __name__ == "__main__":
    # test_stockinette()
    # test_rib()
    # test_seed()
    # test_twisted_stripes()
    # test_lace()
    # test_standard()
    # test_jacquard()
    # test_birdseye()
    test_birdseye_3()


def test_short_rows():
    knit_graph = short_rows(6, buffer_height=1)
    _, __ = knit_graph.get_courses()
    visualize_knitGraph(knit_graph)
