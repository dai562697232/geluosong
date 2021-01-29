data = [2, 2, 3, 3, 5, 7, 7, 7, 9, 9, 11, 11, 11]


def test_func(arr):
    nums = []
    pair = []
    t = []
    f = []
    for i in arr:
        if nums.count(i) == 0:
            nums.append(i)
        else:
            if pair.count(i) == 0:
                pair.append(i)
            else:
                if t.count(i) == 0:
                    t.append(i)
                else:
                    f.append(i)
    return len(pair), len(t), len(f)


if -1:
    print(test_func(data))


class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age


t_list = [Person("张三",22), Person("李四", 21), Person("王麻子", 25), Person("杨六", 32)]

p1 = t_list[2]
t_list2 =[t_list[2]]
t_list.remove(p1)
print(t_list2)
# for i in range(len(t_list)):
#     if t_list[i].age == 21:
#         obj = t_list[i]
#         print(t_list.index(obj))
def t():
    pass