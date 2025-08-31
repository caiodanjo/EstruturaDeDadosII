import random
from anytree import Node as AnyNode, RenderTree
from anytree.exporter import DotExporter
from graphviz import Source

# ------------------------------
# Nó da árvore
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# ------------------------------
# Classe da árvore binária
class BinaryTree:
    def __init__(self):
        self.root = None

    # Inserção
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, current, value):
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
            else:
                self._insert(current.left, value)
        else:
            if current.right is None:
                current.right = Node(value)
            else:
                self._insert(current.right, value)

    # ------------------------------
    # Métodos de travessia

    def inorder(self):
        return self._inorder(self.root, [])

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)
        return result

    def preorder(self):
        return self._preorder(self.root, [])

    def _preorder(self, node, result):
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)
        return result

    def postorder(self):
        return self._postorder(self.root, [])

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)
        return result

    # ------------------------------
    # Visualização com anytree + graphviz
    def to_anytree(self):
        def build_anytree(node):
            if node is None:
                return None
            any_node = AnyNode(str(node.value))
            if node.left:
                any_node.left = build_anytree(node.left)
                any_node.left.parent = any_node
            if node.right:
                any_node.right = build_anytree(node.right)
                any_node.right.parent = any_node
            return any_node
        return build_anytree(self.root)

    def show(self, filename="arvore"):
        anytree_root = self.to_anytree()
        for pre, _, node in RenderTree(anytree_root):
            print("%s%s" % (pre, node.name))
        DotExporter(anytree_root).to_dotfile(f"{filename}.dot")
        Source.from_file(f"{filename}.dot").render(filename, format="png", cleanup=True)
        print(f"Árvore salva em '{filename}.png'.\n")


# ==========================================================
# Programa Principal
if __name__ == "__main__":

    # ------------------------------
    # Árvore com valores fixos
    print("===== ÁRVORE FIXA =====")
    valores_fixos = [55, 30, 80, 20, 45, 70, 90]
    bt_fixa = BinaryTree()
    for v in valores_fixos:
        bt_fixa.insert(v)

    print("\nEstrutura da árvore fixa:")
    bt_fixa.show("arvore_fixa")

    print("Travessias da árvore fixa:")
    print("In-Order (Esq-Raiz-Dir):", bt_fixa.inorder())
    print("Pre-Order (Raiz-Esq-Dir):", bt_fixa.preorder())
    print("Post-Order (Esq-Dir-Raiz):", bt_fixa.postorder())

    # ------------------------------
    # Árvore com valores randômicos
    print("\n===== ÁRVORE RANDÔMICA =====")
    valores_random = [random.randint(1, 200) for _ in range(10)]
    print("Valores randômicos gerados:", valores_random)

    bt_random = BinaryTree()
    for v in valores_random:
        bt_random.insert(v)

    print("\nEstrutura da árvore randômica:")
    bt_random.show("arvore_randomica")

    print("Travessias da árvore randômica:")
    print("In-Order (Esq-Raiz-Dir):", bt_random.inorder())
    print("Pre-Order (Raiz-Esq-Dir):", bt_random.preorder())
    print("Post-Order (Esq-Dir-Raiz):", bt_random.postorder())
