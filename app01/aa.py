from collections import Iterable


def builder_func(item):
    if isinstance(item,Iterable):
        if not isinstance(item,dict):
            for i in item:
                yield i
        else:
            for j in item.values():
                yield j
    else:
        yield item

# a =[6,4,3,2,1]
a={"a":"a","b":"b","c":"c","d":"d"}
b=builder_func(a)
for x in b:
    print(x)
for x in b:
    print("--",x)