import math
import random

from performanzer import performance_logger

from typing import List

class LinearSearch:
    """
    Implementa el algoritmo de búsqueda lineal.

    Complejidad:
    - Tiempo: O(n), donde n es el número de elementos en la lista.
    - Espacio: O(1), ya que no se necesita espacio adicional.

    Funcionamiento:
    - Recorre cada elemento de la lista y lo compara con el objetivo.
    - Si encuentra un elemento que coincide con el objetivo, devuelve su índice.
    - Si no encuentra el objetivo, devuelve -1.
    """

    @staticmethod
    @performance_logger()
    def search(arr: List[int], target: int) -> int:
        """
        Realiza una búsqueda lineal en una lista para encontrar un elemento objetivo.

        Args:
            arr (List[int]): Lista de enteros en la que buscar.
            target (int): Elemento objetivo a buscar.

        Returns:
            int: El índice del elemento objetivo si se encuentra, de lo contrario -1.
        """
        for i in range(len(arr)):
            if arr[i] == target:
                return i
        return -1

class BinarySearch:
    """
    Implementa el algoritmo de búsqueda binaria.

    Complejidad:
    - Tiempo: O(log n), donde n es el número de elementos en la lista.
    - Espacio: O(1), ya que la búsqueda se realiza in situ sin necesidad de espacio adicional.

    Funcionamiento:
    - Divide repetidamente el rango de búsqueda a la mitad.
    - Compara el elemento medio del rango con el objetivo.
    - Ajusta el rango de búsqueda en función de la comparación hasta encontrar el objetivo o hasta que el rango esté vacío.

    Nota:
    - La lista proporcionada debe estar ordenada para que el algoritmo funcione correctamente.
    """
    @staticmethod
    @performance_logger()
    def search(arr: List[int], target: int) -> int:
        """
        Realiza una búsqueda binaria en una lista ordenada para encontrar un elemento objetivo.

        Args:
            arr (List[int]): Lista ordenada de enteros en la que buscar.
            target (int): Elemento objetivo a buscar.

        Returns:
            int: El índice del elemento objetivo si se encuentra, de lo contrario -1.
        """
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

class JumpSearch:
    """
    Implementa el algoritmo de búsqueda por salto (Jump Search).

    Complejidad:
    - Tiempo: O(√n), donde n es el número de elementos en la lista.
    - Espacio: O(1), ya que la búsqueda se realiza in situ sin necesidad de espacio adicional.

    Funcionamiento:
    - Realiza saltos de tamaño √n a través de la lista.
    - Una vez que se encuentra el bloque donde podría estar el objetivo, realiza una búsqueda lineal en ese bloque.
    - Si encuentra el objetivo, devuelve su índice; si no, devuelve -1.

    Nota:
    - La lista proporcionada debe estar ordenada para que el algoritmo funcione correctamente.
    """
    @staticmethod
    @performance_logger()
    def search(arr: List[int], target: int) -> int:
        """
        Realiza una búsqueda por salto en una lista ordenada para encontrar un elemento objetivo.

        Args:
            arr (List[int]): Lista ordenada de enteros en la que buscar.
            target (int): Elemento objetivo a buscar.

        Returns:
            int: El índice del elemento objetivo si se encuentra, de lo contrario -1.
        """
        n = len(arr)
        step = math.sqrt(n)

        prev = 0
        while arr[int(min(step, n) - 1)] < target:
            prev = step
            step += math.sqrt(n)
            if prev >= n:
                return -1

        while arr[int(prev)] < target:
            prev += 1
            if prev == min(step, n):
                return -1

        if arr[int(prev)] == target:
            return int(prev)

        return -1

class ExponentialSearch:
    """
    Realiza una búsqueda exponencial en un arreglo ordenado mediante búsqueda binaria.

    Complejidad:
    - Tiempo: O(log n), donde n es el número de elementos en la lista.
    - Espacio: O(1), ya que la búsqueda se realiza in situ sin necesidad de espacio adicional.

    Funcionamiento:
    - Encuentra un rango donde podría estar el elemento objetivo aumentando exponencialmente el índice.
    - Una vez encontrado el rango, realiza una búsqueda binaria en ese rango.
    - Si encuentra el objetivo, devuelve su índice; si no, devuelve -1.

    Nota:
    - La lista proporcionada debe estar ordenada para que el algoritmo funcione correctamente.
    """
    @staticmethod
    @performance_logger()
    def search(arr: List[int], target: int) -> int:
        """
        Realiza una búsqueda exponencial en una lista ordenada para encontrar un elemento objetivo.

        Args:
            arr (List[int]): Lista ordenada de enteros en la que buscar.
            target (int): Elemento objetivo a buscar.

        Returns:
            int: El índice del elemento objetivo si se encuentra, de lo contrario -1.
        """
        if not arr:
            return -1

        if arr[0] == target:
            return 0

        i = 1
        n = len(arr)
        while i < n and arr[i] <= target:
            i *= 2

        left = i // 2
        right = min(i, n - 1)

        return ExponentialSearch._binary_search(arr, target, left, right)

    def _binary_search(arr: List[int], target: int, left: int, right: int) -> int:
        """
        Método auxiliar para realizar una búsqueda binaria en un segmento de la lista.

        Args:
            arr (List[int]): Lista ordenada de enteros.
            target (int): Elemento objetivo a buscar.
            left (int): Índice inferior del segmento.
            right (int): Índice superior del segmento.

        Returns:
            int: Índice del elemento objetivo en el segmento, o -1 si no se encuentra.
        """
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] > target:
                right = mid - 1
            else:
                left = mid + 1

        return -1

class InterpolationSearch:
    """
    Implementa el algoritmo de búsqueda por interpolación.

    Complejidad:
    - Tiempo: O(log log n) en el mejor de los casos para distribuciones uniformes, O(n) en el peor de los casos.
    - Espacio: O(1), ya que la búsqueda se realiza in situ sin necesidad de espacio adicional.

    Funcionamiento:
    - Estima la posición del elemento objetivo utilizando una fórmula de interpolación.
    - Compara el elemento en la posición estimada con el objetivo.
    - Ajusta los índices de búsqueda según sea necesario y repite el proceso.
    
    Nota:
    - La lista proporcionada debe estar ordenada y tener una distribución uniforme de los valores para que el algoritmo sea eficiente.
    """
    @staticmethod
    @performance_logger()
    def search(arr: List[int], target: int) -> int:
        """
        Realiza una búsqueda por interpolación en una lista ordenada para encontrar un elemento objetivo.

        Args:
            arr (List[int]): Lista ordenada de enteros en la que buscar.
            target (int): Elemento objetivo a buscar.

        Returns:
            int: El índice del elemento objetivo si se encuentra, de lo contrario -1.
        """
        low = 0
        high = len(arr) - 1

        while low <= high and target >= arr[low] and target <= arr[high]:
            if low == high:
                if arr[low] == target:
                    return low
                return -1

            pos = low + int(((float(high - low) / (arr[high] - arr[low])) * (target - arr[low])))

            if arr[pos] == target:
                return pos

            if arr[pos] < target:
                low = pos + 1
            else:
                high = pos - 1

        return -1

### Skip list
class Node_SkipList:
    """Clase para representar un nodo en la Skip List
    
    Atributos:
    - key (int): La clave del nodo.
    - forward (List[Node_SkipList]): Lista de punteros a los nodos siguientes en cada nivel.
    """
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)

class SkipList:
    """
    Clase para representar una Skip List.

    Atributos:
    - MAX_LEVEL (int): El número máximo de niveles en la Skip List.
    - p (float): La fracción que determina la probabilidad de incrementar el nivel.
    - header (Node_SkipList): Nodo ficticio que actúa como cabecera de la Skip List.
    - level (int): El nivel actual de la Skip List.

    Métodos:
    - __init__: Constructor de la Skip List.
    - create_node: Crea un nuevo nodo para la Skip List.
    - random_level: Calcula un nivel aleatorio para un nuevo nodo.
    - insert: Inserta un nuevo elemento en la Skip List.
    - search: Busca un elemento en la Skip List.
    """
    def __init__(self, max_level=3, p=0.5):
        """
        Inicializa una Skip List.

        Args:
            max_level (int): El número máximo de niveles en la Skip List.
            p (float): La fracción que determina la probabilidad de incrementar el nivel.
        """
        self.MAX_LEVEL = max_level
        self.p = p
        self.header = self.create_node(self.MAX_LEVEL, -1)
        self.level = 0

    def create_node(self, lvl: int, key: int):
        """
        Crea un nuevo nodo para la Skip List.

        Args:
            lvl (int): El nivel del nodo.
            key (int): La clave del nodo.

        Returns:
            Node_SkipList: Un nuevo nodo de Skip List.
        """
        return Node_SkipList(key, lvl)

    def random_level(self) -> int:
        """
        Genera un nivel aleatorio para un nuevo nodo.

        Returns:
            int: Un nivel aleatorio.
        """
        lvl = 0
        while random.random() < self.p and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, key: int) -> None:
        """
        Inserta un nuevo elemento en la Skip List.

        Args:
            key (int): La clave del elemento a insertar.
        """
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.key != key:
            rlevel = self.random_level()

            if rlevel > self.level:
                for i in range(self.level + 1, rlevel + 1):
                    update[i] = self.header
                self.level = rlevel

            n = self.create_node(rlevel, key)

            for i in range(rlevel + 1):
                n.forward[i] = update[i].forward[i]
                update[i].forward[i] = n

    @performance_logger()
    def search(self, key: int):
        """
        Busca un elemento en la Skip List.

        Args:
            key (int): La clave del elemento a buscar.

        Returns:
            Node_SkipList | int: El nodo que contiene la clave, o -1 si no se encuentra.
        """
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]

        if current and current.key == key:
            return current
        return -1

class Node_BS:
    """
    Nodo de un árbol binario de búsqueda.

    Atributos:
    - val (int): El valor almacenado en el nodo.
    - left (Node_BS): El hijo izquierdo del nodo.
    - right (Node_BS): El hijo derecho del nodo.
    """
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinaryTree:
    """
    Implementa un árbol binario de búsqueda.

    Complejidad:
    - Inicialización (__init__): O(1) en tiempo y espacio.
    - Insertar (insert): O(h) en tiempo, donde h es la altura del árbol.
    - Buscar (search): O(h) en tiempo, donde h es la altura del árbol.

    Atributos:
    - root (Node_BS): La raíz del árbol.

    Métodos:
    - __init__: Constructor del árbol binario de búsqueda.
    - insert: Inserta un nuevo elemento en el árbol.
    - _insert_recursive: Método auxiliar para insertar elementos de manera recursiva.
    - search: Busca un elemento en el árbol.
    - _search_recursive: Método auxiliar para buscar elementos de manera recursiva.
    """
    def __init__(self):
        self.root = None

    def insert(self, key: int) -> None:
        """
        Inserta un nuevo elemento en el árbol.

        Args:
            key (int): La clave del elemento a insertar.
        """
        if self.root is None:
            self.root = Node_BS(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node: Node_BS, key: int) -> None:
        """
        Método auxiliar para insertar un elemento de manera recursiva.

        Args:
            node (Node_BS): El nodo actual en el árbol.
            key (int): La clave del elemento a insertar.
        """
        if key < node.val:
            if node.left is None:
                node.left = Node_BS(key)
            else:
                self._insert_recursive(node.left, key)
        else:
            if node.right is None:
                node.right = Node_BS(key)
            else:
                self._insert_recursive(node.right, key)

    @performance_logger()
    def search(self, key: int) -> Node_BS | int:
        """
        Busca un elemento en el árbol.

        Args:
            key (int): La clave del elemento a buscar.

        Returns:
            Node_BS | int: El nodo que contiene la clave, o -1 si no se encuentra.
        """
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node: Node_BS, key: int) -> Node_BS | int:
        """
        Método auxiliar para buscar un elemento de manera recursiva.

        Args:
            node (Node_BS): El nodo actual en el árbol.
            key (int): La clave del elemento a buscar.

        Returns:
            Node_BS | int: El nodo que contiene la clave, o -1 si no se encuentra.
        """
        if not node:
            return -1
        if node.val == key:
            return node
        if key < node.val:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

class Node_RB:
    """
    Nodo de un redblack tree.

    Atributos:
    - data (int): El valor almacenado en el nodo.
    - color (str): El color del nodo ('RED' o 'BLACK').
    - parent (Node_RB): El nodo padre.
    - left (Node_RB): El hijo izquierdo del nodo.
    - right (Node_RB): El hijo derecho del nodo.
    """
    def __init__(self, data, color="RED"):
        self.data = data
        self.color = color
        self.parent = None
        self.left = None
        self.right = None

class RedBlackTree:
    """
    Implementa un árbol rojo-negro.

    Atributos:
    - TNULL (Node_RB): Nodo especial que representa el final de un camino en el árbol.
    - root (Node_RB): La raíz del árbol.

    Métodos:
    Complejidad:
    - Inicialización (__init__): O(1) en tiempo y espacio.
    - Insertar (insert): O(log n) en tiempo.
    - Corrección de inserción (fix_insert): O(log n) en tiempo.
    - Rotación izquierda (left_rotate): O(1) en tiempo.
    - Rotación derecha (right_rotate): O(1) en tiempo.
    - Buscar (search): O(log n) en tiempo.
    - Eliminar (delete_node): O(log n) en tiempo.
    - Corrección de eliminación (fix_delete): O(log n) en tiempo.
    """
    def __init__(self):
        self.TNULL = Node_RB(0)
        self.TNULL.color = "BLACK"
        self.root = self.TNULL

    def insert(self, key):
        node = Node_RB(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "RED"

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = "BLACK"
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def fix_insert(self, k):
        while k.parent.color == "RED":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "BLACK"

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    @performance_logger()
    def search(self, key: int) -> Node_RB | int:
        """
        Busca un elemento en el árbol.

        Args:
            key (int): La clave del elemento a buscar.

        Returns:
            Node_RB | int: El nodo que contiene la clave, o -1 si no se encuentra.
        """
        return self._search_helper(self.root, key)

    def _search_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node if node != self.TNULL else -1

        if key < node.data:
            return self._search_helper(node.left, key)
        return self._search_helper(node.right, key)
    
    def delete_node(self, data):
        self._delete_node_helper(self.root, data)

    def _delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("No se puede encontrar la llave en el árbol")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self._rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self._rb_transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "BLACK":
            self._fix_delete(x)

    def _rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def _fix_delete(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.root = RedBlackTree.left_rotate(self.root, x.parent, self.TNULL)
                    s = x.parent.right

                if s.left.color == "BLACK" and s.right.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.right.color == "BLACK":
                        s.left.color = "BLACK"
                        s.color = "RED"
                        self.root = RedBlackTree.right_rotate(self.root, s, self.TNULL)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.right.color = "BLACK"
                    self.root = RedBlackTree.left_rotate(self.root, x.parent, self.TNULL)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.root = RedBlackTree.right_rotate(self.root, x.parent, self.TNULL)
                    s = x.parent.left

                if s.right.color == "BLACK" and s.left.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.left.color == "BLACK":
                        s.right.color = "BLACK"
                        s.color = "RED"
                        self.root = RedBlackTree.left_rotate(self.root, s, self.TNULL)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.left.color = "BLACK"
                    self.root = RedBlackTree.right_rotate(self.root, x.parent, self.TNULL)
                    x = self.root

        x.color = "BLACK"
