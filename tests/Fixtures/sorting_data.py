import random
random.seed(69)

LONGITUD = 4
MAX_NUM = 100
MIN_NUM = -100
MIN_DECIMALES = 3
MAX_DECIMALES = 16
MAX_FLOAT = 0.1415926535897932

class data:
    enteros_unsorted = [random.randint(MIN_NUM, MAX_NUM) for _ in range(LONGITUD)]
    enteros_sorted = sorted(enteros_unsorted)

    flotantes_positivos_unsorted = [random.randint(MIN_NUM, MAX_NUM) + random.randint(0, 10**MIN_DECIMALES) / 10**MIN_DECIMALES for _ in range(LONGITUD//2)]
    flotantes_positivos_sorted = sorted(flotantes_positivos_unsorted)

    flotantes_negativos_unsorted = [-(random.randint(MIN_NUM, MAX_NUM) + random.randint(0, 10**MIN_DECIMALES) / 10**MIN_DECIMALES) for _ in range(LONGITUD//2)]
    flotantes_negativos_sorted = sorted(flotantes_negativos_unsorted)

    flotantes_unsorted = flotantes_positivos_unsorted + flotantes_negativos_unsorted
    flotantes_sorted = sorted(flotantes_unsorted)

    flotantes_de_precision_unsorted = [f + MAX_FLOAT for f in flotantes_unsorted]
    flotantes_de_precision_sorted = sorted(flotantes_de_precision_unsorted)