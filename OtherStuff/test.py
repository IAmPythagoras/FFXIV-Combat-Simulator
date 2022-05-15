import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1,1,100)
y = np.linspace(-1,1,100)

fig, axs = plt.subplots(1,2)

axs[0].plot(x,y)
axs[1].plot(x,y)
plt.show()
