from avl import AVLTree

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.remaining_capacity = capacity
        self.object_id_to_bin = AVLTree(compare_function=lambda obj1, obj2: obj1.object_id - obj2.object_id)

    def add_object(self, obj):
        if self.remaining_capacity >= obj.size:
            self.object_id_to_bin.insert(obj)
            self.remaining_capacity -= obj.size

    def remove_object(self, obj):
        self.object_id_to_bin.remove(obj)
        self.remaining_capacity += obj.size

    def get_object_ids_in_bin(self):
        return [obj.object_id for obj in self.object_id_to_bin.inorder_traversal()]

