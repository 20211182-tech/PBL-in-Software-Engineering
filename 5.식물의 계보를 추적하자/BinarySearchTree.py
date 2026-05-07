def create_node(data):
    return {
        "data": data,
        "left": None,
        "right": None,
    }

def insert(root, data):
    if root is None:
        return create_node(data)

    if data < root["data"]:
        root["left"] = insert(root["left"], data)
        
    elif data > root["data"]:
        root["right"] = insert(root["right"], data)
        
    else:
        print("중복된 값을 삽입할 수 없습니다.")

    return root

def find(root, value):
    if root is None:
        return None

    if value == root["data"]:
        return root
    
    if value < root["data"]:
        return find(root["left"], value)
    return find(root["right"], value)

def find_min(root):
    current = root
    while current is not None and current["left"] is not None:
        current = current["left"]
    return current

def delete(root, data):
    if root is None:
        return None
    
    if data < root["data"]:
        root["left"] = delete(root["left"], data)
        
    elif data > root["data"]:
        root["right"] = delete(root["right"], data)
        
    else:
        if root["left"] is None and root["right"] is None:
            return None
        
        if root["left"] is None:
            return root["right"]
        
        if root["right"] is None:
            return root["left"]
        
        else:
            min_node = find_min(root["right"])
            root["data"] = min_node["data"]
            root["right"] = delete(root["right"], min_node["data"])            

    return root