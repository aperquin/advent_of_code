from run import Network1, Network2, Node

instruction_1 = "RL"
network_1_text = """AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

instruction_2 = "LLR"
network_2_text = """AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

instruction_3 = "LR"
network_3_text = """11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

def test_node_constructor_01():
    assert Node("BBB", "AAA", "ZZZ") == Node.from_string("BBB = (AAA, ZZZ)")

def test_node_next_node_id_01():
    assert Node.from_string("BBB = (AAA, ZZZ)").next_node_id("L") == "AAA"

def test_node_next_node_id_02():
    assert Node.from_string("BBB = (AAA, ZZZ)").next_node_id("R") == "ZZZ"

def test_network_constructor_01():
    assert Network1.from_string(network_1_text)._nodes["CCC"] == Node.from_string("CCC = (ZZZ, GGG)")

def test_network_constructor_02():
    assert Network1.from_string(network_2_text)._nodes["ZZZ"] == Node.from_string("ZZZ = (ZZZ, ZZZ)")

def test_network_solve_01():
    network = Network1.from_string(network_1_text)
    assert network.nb_steps_solve(network.compute_starting_nodes(), network.compute_ending_nodes(), instruction_1) == (2, ['ZZZ'])

def test_network_solve_02():
    network = Network1.from_string(network_2_text)
    assert network.nb_steps_solve(network.compute_starting_nodes(), network.compute_ending_nodes(), instruction_2) == (6, ['ZZZ'])




def test_network2_starting_nodes_01():
    assert Network2.from_string(network_3_text).compute_starting_nodes() == ["11A", "22A"]

def test_network2_ending_nodes_01():
    assert Network2.from_string(network_3_text).compute_ending_nodes() == ["11Z", "22Z"]

def test_network2_solve_01():
    network = Network2.from_string(network_3_text)
    assert network.nb_steps_solve(network.compute_starting_nodes(), network.compute_ending_nodes(), instruction_3) == (6, ['11Z', '22Z'])