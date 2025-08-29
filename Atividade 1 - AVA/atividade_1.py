import random
from anytree import Node as AnyNode, RenderTree
from anytree.exporter import DotExporter
from graphviz import Source

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self, root_value):
        self.root = Node(root_value)

    def to_anytree(self, node=None, parent=None):
        if node is None:
            node = self.root
        any_node = AnyNode(f"{node.value}_{id(node)}", parent=parent, label=node.value)
        if node.left:
            self.to_anytree(node.left, any_node)
        if node.right:
            self.to_anytree(node.right, any_node)
        return any_node

def render_tree(anytree_root, filename):
    dot_data = "\n".join(DotExporter(
        anytree_root,
        nodenamefunc=lambda n: n.name,
        nodeattrfunc=lambda n: f'label="{n.label}"'
    ))
    graph = Source(dot_data)
    graph.render(filename, format="png", cleanup=True)

# --------------------------------------------------------
# 1) Árvore fixa (expressão definida no enunciado)

tree = BinaryTree("/")
tree.root.left = Node("*")
tree.root.right = Node("*")

tree.root.left.left = Node("+")
tree.root.left.right = Node("-")

tree.root.left.left.left = Node("7")
tree.root.left.left.right = Node("3")
tree.root.left.right.left = Node("5")
tree.root.left.right.right = Node("2")

tree.root.right.left = Node("10")
tree.root.right.right = Node("20")

anytree_root = tree.to_anytree()
render_tree(anytree_root, "arvore_fixa")

print("Árvore fixa gerada: arvore_fixa.png")

# --------------------------------------------------------
# 2) Árvore com valores randômicos

OPERATORS = ["+", "-", "*", "/"]

def generate_random_expression():
    operands = [str(random.randint(1, 20)) for _ in range(3)]

    operators = [random.choice(OPERATORS) for _ in range(2)]

    expression = f"(({operands[0]} {operators[0]} {operands[1]}) {operators[1]} {operands[2]})"
    return expression

def build_tree_from_expression(expr):
    tokens = expr.replace("(", " ( ").replace(")", " ) ").split()
    
    def parse(tokens):
        token = tokens.pop(0)
        if token == "(":
            left = parse(tokens)
            op = tokens.pop(0)
            right = parse(tokens)
            tokens.pop(0)
            node = Node(op)
            node.left = left
            node.right = right
            return node
        else:
            return Node(token)
    
    return parse(tokens)

random_expr = generate_random_expression()
print("Expressão aleatória gerada:", random_expr)

random_tree = BinaryTree(None)
random_tree.root = build_tree_from_expression(random_expr)

anytree_random = random_tree.to_anytree()
render_tree(anytree_random, "arvore_randomica")

print("Árvore randômica gerada: arvore_randomica.png")