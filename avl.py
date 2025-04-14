from node import Node

class AVLTree:
    def __init__(self, compare_function=lambda x, y: x - y):
        self.root = None
        self._compare = compare_function

    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def remove(self, value):
        self.root = self._remove_recursive(self.root, value)

    def search(self, value):
        return self._search_recursive(self.root, value)

    def inorder_traversal(self):
        return self._traverse_inorder(self.root, [])
    def _traverse_inorder(self, node, result):
        if node:
            self._traverse_inorder(node.left, result)
            result.append(node.value)
            self._traverse_inorder(node.right, result)
        return result

    def find_compact_fit(self, size, least_id=True):
        return self._find_compact_fit_recursive(self.root, size, least_id, None)

    def _find_compact_fit_recursive(self, node, size, least_id, current_candidate):
        if not node:
            return current_candidate

        curr_bin = node.value

        # Traverse left subtree first (smaller remaining capacities)
        current_candidate = self._find_compact_fit_recursive(node.left, size, least_id, current_candidate)

        # Check current bin
        if curr_bin.remaining_capacity >= size:
            #Deciding if this bin is a better candidate
            if not current_candidate:
                current_candidate=curr_bin

            elif curr_bin.remaining_capacity<current_candidate.remaining_capacity:
                current_candidate=curr_bin

            elif curr_bin.remaining_capacity == current_candidate.remaining_capacity:
                #checking for least_if condition when same capacity
                if least_id:
                    if curr_bin.bin_id < current_candidate.bin_id:
                        current_candidate = curr_bin
                else:
                    if curr_bin.bin_id > current_candidate.bin_id:
                        current_candidate = curr_bin

        # Traverse right subtree
        current_candidate = self._find_compact_fit_recursive(node.right, size, least_id, current_candidate)

        return current_candidate

    def find_largest_fit(self, size, least_id=True):
        return self._find_largest_fit_recursive(self.root, size, least_id, None)

    def _find_largest_fit_recursive(self, node, size, least_id, current_candidate):
        if not node:
            return current_candidate

        curr_bin = node.value

        # Traverse right subtree first (larger remaining capacities)
        current_candidate = self._find_largest_fit_recursive(node.right, size, least_id, current_candidate)

        # Check current bin
        if curr_bin.remaining_capacity >= size:
            if not current_candidate:
                current_candidate = curr_bin
            elif curr_bin.remaining_capacity > current_candidate.remaining_capacity:
                current_candidate = curr_bin
            elif curr_bin.remaining_capacity ==current_candidate.remaining_capacity:
                if least_id:
                    if curr_bin.bin_id < current_candidate.bin_id:
                        current_candidate = curr_bin
                else:
                    if curr_bin.bin_id > current_candidate.bin_id:
                        current_candidate = curr_bin

        # Traverse left subtree
        current_candidate = self._find_largest_fit_recursive(node.left, size, least_id, current_candidate)

        return current_candidate

    def _insert_recursive(self, node, value):
        if not node:
            return Node(value)

        cmp = self._compare(value, node.value)
        if cmp < 0:
            node.left = self._insert_recursive(node.left, value)
        elif cmp > 0:
            node.right = self._insert_recursive(node.right, value)
        else:
            # Duplicate value, do not insert
            return node

        return self._balance_node(node)

    def _remove_recursive(self, node, value):
        if not node:
            return node

        cmp = self._compare(value, node.value)
        if cmp < 0:
            node.left = self._remove_recursive(node.left, value)
        elif cmp > 0:
            node.right = self._remove_recursive(node.right, value)
        else:
            # Node with one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Node with two children: get the inorder successor
            temp = self._get_min_value_node(node.right)
            node.value = temp.value
            node.right = self._remove_recursive(node.right, temp.value)

        return self._balance_node(node)

    def _search_recursive(self, node, value):
        if not node:
            return None

        cmp = self._compare(value, node.value)
        if cmp == 0:
            return node.value
        elif cmp < 0:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def _balance_node(self, node):
        self._update_height(node)
        balance = self._get_balance(node)

        # Left heavy
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right heavy
        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        self._update_height(z)
        self._update_height(y)

        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        self._update_height(z)
        self._update_height(y)

        return y

    def _get_height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def _get_max_value_node(self, node):
        current = node
        while current.right:
            current = current.right
        return current
