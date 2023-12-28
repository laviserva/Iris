import random
random.seed(6)

LONGITUD = 4
MAX_NUM = 100
MIN_NUM = -100
MIN_DECIMALES = 3
MAX_DECIMALES = 16
MAX_FLOAT = 0.1415926535897932

class data:
    no_chosed = MAX_NUM + 1
    
    __enteros_unsorted = [random.randint(MIN_NUM, MAX_NUM) for _ in range(LONGITUD)]
    enteros_sorted = sorted(__enteros_unsorted)
    enteros_chosed = random.choice(enteros_sorted)

    __flotantes_positivos_unsorted = [random.randint(MIN_NUM, MAX_NUM) + random.randint(0, 10**MIN_DECIMALES) / 10**MIN_DECIMALES for _ in range(LONGITUD//2)]
    flotantes_positivos_sorted = sorted(__flotantes_positivos_unsorted)

    __flotantes_negativos_unsorted = [-(random.randint(MIN_NUM, MAX_NUM) + random.randint(0, 10**MIN_DECIMALES) / 10**MIN_DECIMALES) for _ in range(LONGITUD//2)]
    flotantes_negativos_sorted = sorted(__flotantes_negativos_unsorted)

    __flotantes_unsorted = __flotantes_positivos_unsorted + __flotantes_negativos_unsorted
    flotantes_sorted = sorted(__flotantes_unsorted)
    flotantes_chosed = random.choice(flotantes_sorted)

    __flotantes_de_precision_unsorted = [f + MAX_FLOAT for f in __flotantes_unsorted]
    flotantes_de_precision_sorted = sorted(__flotantes_de_precision_unsorted)
    flotantes_de_precision_chosed = random.choice(flotantes_de_precision_sorted)