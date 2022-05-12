# creating a new dictionary
my_dict ={"java":[0,100], "python":[0,112], "c":[11,10]}

# list out keys and values separately
key_list = list(my_dict.keys())
val_list = list(my_dict.values())

# print key with val 100
position = val_list.index([0,100])
print(key_list[position])

# print key with val 112


# one-liner
