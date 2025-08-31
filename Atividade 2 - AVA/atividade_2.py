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
    def __init__(self):
        self.root = None

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

    def search(self, value):
        return self._search(self.root, value)

    def _search(self, current, value):
        if current is None or current.value == value:
            return current
        if value < current.value:
            return self._search(current.left, value)
        else:
            return self._search(current.right, value)
        
    def remove(self, value):
        self.root = self._remove(self.root, value)

    def _remove(self, current, value):
        if current is None:
            return None
        if value < current.value:
            current.left = self._remove(current.left, value)
        elif value > current.value:
            current.right = self._remove(current.right, value)
        else:
            if current.left is None and current.right is None:
                return None
            elif current.left is None:
                return current.right
            elif current.right is None:
                return current.left
            else:
                sucessor = self._min_value_node(current.right)
                current.value = sucessor.value
                current.right = self._remove(current.right, sucessor.value)
        return current

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def depth(self, value):
        return self._depth(self.root, value, 0)

    def _depth(self, current, value, d):
        if current is None:
            return -1
        if current.value == value:
            return d
        elif value < current.value:
            return self._depth(current.left, value, d + 1)
        else:
            return self._depth(current.right, value, d + 1)
        
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
        print(f"Árvore salva em '{filename}.png'.")

# --------------------------------------------------------
# 1) Árvore fixa (expressão definida no enunciado)

if __name__ == "__main__":
    valores = [55, 30, 80, 20, 45, 70, 90]
    bt = BinaryTree()
    for v in valores:
        bt.insert(v)

    print("\nÁrvore inicial:")
    bt.show()

    busca_valor = 45
    encontrado = bt.search(busca_valor)
    print(f"\nBusca pelo valor {busca_valor}: {'Encontrado' if encontrado else 'Não encontrado'}")

    remover = 30
    bt.remove(remover)
    print(f"\nÁrvore após remover {remover}:")
    bt.show()

    novo = 50
    bt.insert(novo)
    print(f"\nÁrvore após inserir {novo}:")
    bt.show("arvore_fixa")

    print(f"\nAltura da árvore: {bt.height()}")

    print(f"Profundidade do nó 45: {bt.depth(45)}")

    # --------------------------------------------------------
    # 2) Árvore com valores randômicos

    print("\n===== Árvore Randômica =====")

    random_values = [random.randint(1, 200) for _ in range(15)]
    print("Valores randômicos gerados:", random_values)

    bt_random = BinaryTree()
    for v in random_values:
        bt_random.insert(v)

    print("\nÁrvore randômica gerada:")
    bt_random.show("arvore_randomica")

    print(f"\nAltura da árvore randômica: {bt_random.height()}")