import numpy as np
import matplotlib.pyplot as plt

with open("7-1_settings.txt", 'r') as settings:
    tmp = [float(i) for i in settings.read().split("\n")]
    print(tmp)

data_array = np.loadtxt("7-1_data.txt", dtype = int)
data_array = data_array * 3.3 / 256

x_graph = [0] * len(data_array)

for i in range(len(data_array)):
    x_graph[i] = i * (1 / tmp[0])


fig, ax = plt.subplots(figsize = (10, 5), dpi = 400)
ax.set_title("Процесс заряда и разряда конденсатора в RC - цепочке")
ax.set_xlabel("Время, с")
ax.set_ylabel("Напряжение, В")
ax.minorticks_on()
ax.grid(which='major', color = 'grey', linewidth = 1)
ax.grid(which='minor', color = 'grey', linestyle = ':')

x_scatter = np.array([])
y_scatter = np.array([])

for i in range(len(data_array)):
    if (i % 100 == 0):
        np.append(x_scatter, x_graph[i])
        np.append(y_scatter, data_array[i])

ax.scatter(x_scatter, y_scatter, marker = '^')
ax.plot(x_graph, data_array, 'o', ls = '-', ms = 4, markevery = 200, label = "V(t)", color = "green", linewidth = 0.5, )
ax.legend()
ax.text(45, 2.55, "Время зарядки: ", color = "red")
ax.text(45, 2.2, "Время разрядки: ", color = "red")
fig.savefig("test.png") 
fig.savefig("test.svg")
#plt.show()