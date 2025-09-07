class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def _update_height(self, node):
        if not node:
            return 0
        
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        node.height = 1 + max(left_height, right_height)
        return node.height
    
    def get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current
    
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x
    
    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y
    
    def insert(self, key):
        self.root = self._recursive_insert(self.root, key)

    def _recursive_insert(self, current_node, key):
        if not current_node:
            return Node(key)
        

        if key < current_node.key:
            current_node.left = self._recursive_insert(current_node.left, key)
        elif key > current_node.key:
            current_node.right = self._recursive_insert(current_node.right, key)
        else:
            raise ValueError("Chaves duplicadas não são permitidas em árvores AVL")
        
        self._update_height(current_node)

        balance = self.get_balance(current_node)

        if balance > 1 and key < current_node.left.key:
            current_node.left = self._rotate_left(current_node.left)
            return self._rotate_right(current_node)
        
        if balance < -1 and key < current_node.right.key:
            current_node.right = self._rotate_right(current_node.right)
            return self._rotate_left(current_node)
        
        return current_node
    
    def delete(self, key):
        self.root = self._recursive_delete(self.root, key)

    def _recursive_delete(self, current_node, key):
        if not current_node:
            return current_node
        
        if key < current_node.key:
            current_node.left = self._recursive_delete(current_node.left, key)
        elif key > current_node.key:
            current_node.right = self._recursive_delete(current_node.right, key)
        else:
            if not current_node.left:
                return current_node.right
            elif not current_node.right:
                return current_node.left
            else:
                successor = self.get_min_value_node(current_node.right)
                current_node.key = successor.key
                current_node.right = self._recursive_delete(current_node.right, successor.key)

        self._update_height(current_node)

        balance = self.get_balance(current_node)

        if balance > 1 and self.get_balance(current_node.left) >= 0:
            return self._rotate_right(current_node)
        
        if balance > 1 and self.get_balance(current_node.left) < 0:
            current_node.left = self._rotate_left(current_node.left)
            return self._rotate_right(current_node)
        
        if balance < -1 and self._get_balance(current_node.right) <= 0:
            return self._rotate_left(current_node)
        
        if balance < -1 and self.get_balance(current_node.left) > 0:
            current_node.right = self._rotate_right(current_node.right)
            return self._rotate_left(current_node)
        
        return current_node
    
    def find_nodes_in_range(self, key1, key2):
        result = []

        def inorder(node):
            if not node:
                return
            
            if node.key > key1:
                inorder(node.left)
            
            if key1 <= node.key <= key2:
                result.append(node.key)
            
            if node.key < key2:
                inorder(node.right)

        inorder(self.root)
        return result
    
    def get_node_depth(self, key):
        depth = 0
        current = self.root

        while current:
            if key == current.key:
                return depth
            elif key < current.key:
                current = current.left
            else:
                current = current.right
            depth += 1
        
        return -1
    
if __name__ == "__main__":
    avl_tree = AVLTree()

    print("\n--- ATIVIDADE PRÁTICA: ÁRVORE AVL ---")
    
    print("\n--- 1. Inserindo nós ---")
    keys_to_insert = [9, 5, 10, 0, 6, 11, -1, 1, 2]
    try:
        for key in keys_to_insert:
            avl_tree.insert(key)
            print("Inserção concluída (sem erros).")
    except Exception as e:
        print(f"\nERRO DURANTE A INSERÇÃO: {e}")

    print("\n--- 2. Deletando nós ---")
    try:
        keys_to_delete = [10, 11]
        for key in keys_to_delete:
            avl_tree.delete(key)
        print("Deleção concluída (sem erros).")
    except Exception as e:
        print(f"\nERRO DURANTE A DELEÇÃO: {e}")

    print("\n--- 3. Buscando nós no intervalo [1, 9] ---")
    try:
        nodes_in_range = avl_tree.find_nodes_in_range(1, 9)
        if nodes_in_range is not None:
            print(f"Nós encontrados: {sorted(nodes_in_range)}")
        else:
            print("Método `encontrar_nos_intervalo` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE A BUSCA POR INTERVALO: {e}")

    print("\n--- 4. Calculando profundidade do nó 6 ---")
    try:
        depth = avl_tree.get_node_depth(6)
        if depth is not None:
            if depth != -1:
                print(f"O nó 6 está no nível/profundidade: {depth}")
            else:
                print("O nó 6 não foi encontrado.")
        else:
            print("Método `get_node_depth` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE O CÁLCULO DE PROFUNDIDADE: {e}")
