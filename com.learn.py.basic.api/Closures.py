def counter():
    count = 0
    def add_one():
        nonlocal count
        count += 1
        return count
    return add_one

c = counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3
