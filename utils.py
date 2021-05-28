


def findkeys(node, kv):
    """
         Find all occurrences of a key in nested dictionaries and lists
        :param node: dictionary or list
        :param kv: key value
        :return: array of key values
        """
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys(j, kv):
                yield x