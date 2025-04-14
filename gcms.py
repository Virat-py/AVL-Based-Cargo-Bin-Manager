from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

# custom comparator function
def compare_bins(bin1, bin2):
    if bin1.remaining_capacity < bin2.remaining_capacity:
        return -1
    elif bin1.remaining_capacity > bin2.remaining_capacity:
        return 1
    else:
        return bin1.bin_id - bin2.bin_id

class GCMS:
    def __init__(self):
        # to find bin info from a bin_id
        self.bins_by_bin_id = AVLTree(compare_function=lambda bin1, bin2: bin1.bin_id - bin2.bin_id)
        # to find objects from object_id
        self.objects_by_id = AVLTree(compare_function=lambda obj1,obj2: obj1.object_id-obj2.object_id)
        # AVL tree sorted by remaining_capacity ascending and bin_id ascending
        self.bins = AVLTree(compare_bins)

    def add_bin(self, bin_id, capacity):
        bin = Bin(bin_id, capacity)
        self.bins_by_bin_id.insert(bin)
        self.bins.insert(bin)

    def add_object(self, object_id, size, color):
        obj = Object(object_id, size, color)
        found_bin = None

        if color == Color.BLUE:
            # Compact Fit, Least ID
            found_bin = self.bins.find_compact_fit(size, least_id=True)
        if color == Color.YELLOW:
            # Compact Fit, Greatest ID
            found_bin = self.bins.find_compact_fit(size, least_id=False)
        if color == Color.RED:
            # Largest Fit, Least ID
            found_bin = self.bins.find_largest_fit(size, least_id=True)
        if color == Color.GREEN:
            # Largest Fit, Greatest ID
            found_bin = self.bins.find_largest_fit(size, least_id=False)

        if found_bin==None:
            raise NoBinFoundException
        # Remove bin from AVL tree before updating
        self.bins.remove(found_bin)
        # Add object to the bin
        found_bin.add_object(obj)
        obj.bin = found_bin
        # Insert the object into objects_by_id AVL tree
        self.objects_by_id.insert(obj)
        # Reinsert the bin into the AVL tree with updated remaining_capacity
        self.bins.insert(found_bin)

    def delete_object(self, object_id):
        # Create a dummy object for searching
        dummy_object = Object(object_id, 0, None)
        del_object = self.objects_by_id.search(dummy_object)
        if del_object is None:
            return None
        del_bin = del_object.bin

        # Remove bin from AVL tree before updating
        self.bins.remove(del_bin)

        # Remove the object from the bin
        del_bin.remove_object(del_object)
        del_object.bin = None

        # Remove the object from objects_by_id AVL tree
        self.objects_by_id.remove(del_object)

        # Reinsert the bin into the AVL tree with updated remaining_capacity
        self.bins.insert(del_bin)

    def bin_info(self, bin_id):
        # Create a dummy bin for searching
        dummy_bin = Bin(bin_id, 0)
        bin = self.bins_by_bin_id.search(dummy_bin)
        if bin:
            return (bin.remaining_capacity, bin.get_object_ids_in_bin())
        else:
            return None

    def object_info(self, object_id):
        # Create a dummy object for searching
        dummy_object = Object(object_id, 0, None)
        obj = self.objects_by_id.search(dummy_object)
        if obj and obj.bin:
            return obj.bin.bin_id
        else:
            return None
