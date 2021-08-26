import numpy as np
import matplotlib.pyplot as plt
import sys

data_dir = sys.argv[1]

categories = ['If', 'Vbd', 'Vpt', 'dV', 'Id', 'Mmax', 'R', 'V10', 'Vm', 'I0', 'Im']
datamap = {}
values = {}
for category in categories:
    values[category] = []

with open(data_dir, 'r') as f:
    lines = f.readlines()
    i = 0
    xy = {}
    xy[i] = []
    index_list = []
    len_y = []
    for line in lines:
        line = line.strip('\n')
        line = line.split()
        if len(line) == 22:
            index_list.append(int(line[2]))
            if int(line[2]) not in xy[i]:
                xy[i].append(int(line[2]))
            else:
                i = i + 1
                xy[i] = []
                xy[i].append(int(line[2]))
            k = 0
            for l in line[3:]:
                if l not in ['Pass', 'Fail']:
                    values[categories[k]].append(float(l))
                    k = k + 1
    for k in range(i+1):
        len_y.append(len(xy[k]))

    index_min = min(index_list)
    index_max = max(index_list)
    index_diff = index_max - index_min + 1
    for category in categories:
        datamap[category] = min(values[category]) * np.ones((index_diff, i + 1))

    i = 0
    xy = {}
    xy[i] = []
    for line in lines:
        line = line.strip('\n')
        line = line.split()
        if len(line) == 22:
            if int(line[2]) not in xy[i]:
                xy[i].append(int(line[2]))
            else:
                i = i + 1
                xy[i] = []
                xy[i].append(int(line[2]))
            x = int(line[2]) - index_min

            k = 0
            for l in line[3:]:
                if l not in ['Pass', 'Fail']:
                    datamap[categories[k]][x][i] = float(l)
                    k = k + 1

rows = 2
cols = 6

axes=[]
fig=plt.figure()
plt.rcParams.update({'font.size': 7})

for i, category in enumerate(categories):
    max = np.max(datamap[category])
    min = np.min(datamap[category])
    showmap = datamap[category]
    #showmap = np.clip((datamap[category] - min) / (max - min), 0, 1)
    axes.append(fig.add_subplot(rows, cols, i + 1))
    axes[-1].set_title((str(category)))
    plt.imshow(showmap)
    plt.colorbar(ticks=np.arange(min, max + 0.01, (max-min)/5))
    plt.axis('off')

fig.tight_layout()
img_name = data_dir.split('.')
plt.savefig(img_name[0] + '.png')

