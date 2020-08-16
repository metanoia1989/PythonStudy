#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
访问树
"""
class Node(object):
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    
def tree_traverse(node):
    if node.left is not None:
        tree_traverse(node.left)

    print(node.data)

    if node.right is not None:
        tree_traverse(node.right)

if __name__ == "__main__":
    root = Node("i am the root")
    root.left = Node("first left child")
    root.right = Node("first right child")

    root.left.right = Node("Right child of first left child of root")

    tree_traverse(root)