
# 1 варіант - імпорт цілого модуля (5)

# Вбудовані
import math
import random

# Інстальовані
import numpy
import pytest

# Власний
import imported_modules

print(math.pi)
print(random.randint(1, 10))
print(imported_modules.add(2, 3))


# 2 варіант – імпорт конкретного (5)

# Вбудовані
from math import sqrt
from datetime import date

# Інстальовані
from numpy import array

# Власні
from imported_modules import add
from imported_modules import subtract

print(sqrt(16))
print(date.today())
print(array([1,2,3]))
print(add(5,5))
print(subtract(10,3))


# 3 варіант – імпорт всього (5)

# Вбудовані
from math import *
from random import *

# Інстальовані
from numpy import *

# Власні
from imported_modules import *

# Ще один вбудований
from datetime import *

print(pi)
print(randint(1,10))
print(array([4,5,6]))
print(add(1,1))
print(date.today())


# 4 варіант – імпорт з псевдонімом (5)

# Вбудовані
import math as m
import random as rnd

# Інстальовані
import numpy as np

# Власні
import imported_modules as mod
from imported_modules import multiply as mult

print(m.pi)
print(rnd.randint(1,5))
print(np.array([7,8,9]))
print(mod.add(3,3))
print(mult(2,4))
