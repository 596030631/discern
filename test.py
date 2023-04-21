labels = []
category = []

with open('labels/categroy.txt', 'r', encoding='utf-8') as f:
    l = f.readlines()
    for i in l:
        print(i)
        category.append(i.split(',')[1].replace('\n', ''))
print(category)

with open('labels/labels.txt', 'r', encoding='utf-8') as f:
    l = f.readlines()
    for i in l:
        print(i)
        ls = i.split(',')
        labels.append(
            {'id': int(ls[0]), 'en': ls[1], 'cn': ls[2], 'category_id': int(ls[3]), 'category': category[int(ls[3])]})

print(labels)