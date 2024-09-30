import random
import math

# Реализация верхней неполной Гамма-функции заимствовано из
# https://github.com/dj-on-github/sp800_22_tests/blob/master/gamma_functions.py
import gamma_functions


def gen_bitsequence(l: int) -> list:
    '''
    Генерирует псевдослучайную последовательность из {0,1} длины l и возвращает ее в виде списка
    l : int длина последовательности
    '''

    alphabet = '01'
    random.seed()   # Инициализировать генератор псевдо-случ чисел (использ текущее сист время по умолч)
    return [int(random.choice(alphabet)) for i in range(0, l)]  # вернуть список со случайной послед-ю


def nist_1_monobit(bitseq, significance=0.01):
    '''
    Анализирует bitseq (последовательность битов) с помощью теста Monobit NIST.
    bitseq: последовательность битов для анализа
    significance: пороговый уровень P-значения для принятия НУЛЕВОЙ гипотезы.
    '''

    # --- Реализация по формуле из методички:
    # --  HE берется модуль от разности кол-ва единиц и нулей
    # D = bitseq.count(1) - bitseq.count(0)
    # Sn = float(D) / math.sqrt( float( len( bs ) ) )
    # Pval = math.erfc( Sn / math.sqrt(2.0) )
    # print( D, ":", Sn, Pval ) # Отладочная печать

    # --- Реализация по формуле из определяющего документа NIST: "SP800-22r1a", Monobit test
    # --  БЕРЕТСЯ модуль от разницы между кол-вом единиц и нулей
    D = abs(bitseq.count(1) - bitseq.count(0))
    Sn = float(D) / math.sqrt(float(len(bs)))
    Pval = math.erfc(Sn / math.sqrt(2.0))

    # print("Проверка: ", D, ":", Sn, Pval, (Pval > significance))  # Отладочная печать
    print ("Pval = ", Pval)
    return (Pval > significance)


def nist_2_runs(bitseq, significance=0.01):
    '''
    Анализирует bitseq (последовательность битов) с помощью теста Runs.
    bitseq: последовательность битов для анализа
    significance: пороговый уровень P-значения для принятия НУЛЕВОЙ гипотезы.
    '''
    N = len(bitseq)
    # Сначала проверим базовый критерий, нужно ли делать тест
    zeta = bitseq.count(1) / N

    #   Если базовая проверка не выполнена, вернуть False и закончить
    if (abs(zeta - 0.5) >= 2.0 / math.sqrt(N)):
        return False

    # Основной тест
    V_N = 0  # Переменная для расчета общего кол-ва перемен последовательности
    for i in range(N-1):  # 0, 1, 2, ...., 127-1=126
        if (bitseq[i] != bitseq[i+1]):
            V_N += 1
    Pval = math.erfc(abs(V_N - 2 * N * zeta * (1 - zeta)) /
                     (2 * math.sqrt(2.0 * N) * zeta * (1 - zeta)))
    # print(f"Проверка: V_N = {V_N:-3d}, Pval = {Pval:.3f}")
    print("Pval = ", Pval)
    return (Pval > significance)


def nist_3_longest_run_of_ones_in_block(bitseq, significance=0.01, blocklen=8):
    '''
    Анализирует bitseq (последовательность битов) с помощью теста Runs
    bitseq: последовательность битов для анализа
    significance: пороговый уровень P-значения для принятия НУЛЕВОЙ гипотезы.
    blocklen: длина подблоков, в которых анализируется самая длинная серия их распределения.
    '''

    N = len(bitseq)
    M = blocklen

    if (N < 128 or M < 8):
        print(f"Error in function 'nist_3_longest_run_of_ones_in_block' :")
        print(f"    Lengths of the bitsequence N={N:-5d} ", end='')
        print(f"    or the selected sub-block size M={M:-5d} are too short!")

    Nb = math.floor(N / M)
    # print(f"Проверка1: N/M={N/M}, Nb={Nb}")

    # Таблица частот непрерывных послед-тей единиц: не более 1, по 2, по 3, более 4
    v = [0, 0, 0, 0]

    # Цикл по под-блокам и вычисление макс длин непрерывных послед-тей 1ц
    for i in range(Nb):
        block = bitseq[i * M: ((i + 1) * M)]  # Выделить очередной под-блок длины M

        run = 0  # счетчик длины непрерывной послед-ти единиц
        longest = 0  # переменная для хранения максимальной длины непр посл-ти в блоке
        for j in range(M):
            if (block[j] == 1):
                run += 1
                if (run > longest):
                    longest = run  # Обновить хранимую макс длину посл-ти 1ц в блоке
            else:
                run = 0  # Если непрерывная послед-ть 1ц прервалась, обнулить счетчик

        # print(f"Проверка2: in block[{i}] longest run is {longest} ones")

        # Обновить счетчики кол-ва послед-тей длины <=1, =2, =3, >=4
        if longest <= 1:
            v[0] += 1
        elif longest == 2:
            v[1] += 1
        elif longest == 3:
            v[2] += 1
        else:
            v[3] += 1

        # print(f">>Проверка3: v[] = {v}")

    #   Вычислить критерий хи-квадрат
    pi = (0.2148, 0.3672, 0.2305, 0.1875)  # Сохранить таблицу pi_i в кортеж
    chi_sq = 0.0
    for k, vi in enumerate(v):
        # print(f"Проверка4: {k}, {vi}")
        chi_sq += (vi - 16 * pi[k]) ** 2 / (16 * pi[k])

    Pval = gamma_functions.gammaincc(3.0 / 2.0, chi_sq / 2.0)
    # print(f"Проверка5: chi_sq = {chi_sq}, Pval = {Pval}")
    print("Pval = ", Pval)
    return (Pval > significance)


if __name__ == '__main__':
    # alphabet = '01'
    # random.seed()   # Инициализировать генератор псевдо-случ чисел (использ текущее сист время по умолч)
    # for i in range(1,10):
    #    print(random.choice( alphabet ))

    # bs = gen_bitsequence(l=128)  # Вызвать функцию генерации битовой последовательности
    # print(bs, len(bs))
    bs0 = "01001101101111000010110001110111011101000011111110110110000111001111101100010001010001110101001111101011100100001111000010010110"
    bs = [ int(bs0[i]) for i in range(0, len(bs0))]

    test1 = nist_1_monobit(bs)
    print(f"Test1_monobit: {test1}")

    test2 = nist_2_runs(bs)
    print(f"Test2_runs: {test2}")

    test3 = nist_3_longest_run_of_ones_in_block(bs, blocklen=8)
    print(f"Test3_runs: {test3}")
