from time import sleep
from tqdm import tqdm

p_bar = tqdm(range(10))
p_bar.update(3)
p_bar.refresh()
sleep(1)
p_bar.update(2)
p_bar.refresh()
sleep(1)
p_bar.update(5)
p_bar.refresh()
input("hey")