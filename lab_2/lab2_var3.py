import random
import math


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

    print("Проверка: ", D, ":", Sn, Pval, (Pval > significance))  # Отладочная печать

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
    if(abs(zeta - 0.5) >= 2.0 / math.sqrt(N)):
        return False;

    # Основной тест
    V_N = 0 # Переменная для расчета общего кол-ва перемен последовательности
    for i in range(N-1):  # 0, 1, 2, ...., 127-1=126
        if(bitseq[i] != bitseq[i+1]):
            V_N += 1;
    Pval = math.erfc(abs(V_N - 2 * N * zeta * (1 - zeta)) /
                      (2 * math.sqrt(2.0 * N) * zeta * (1 - zeta))
                    )
    print(f"Проверка: V_N = {V_N:-3d}, Pval = {Pval:.3f}")
    return (Pval > significance)


if __name__ == '__main__':
    alphabet = '01'
    # random.seed()   # Инициализировать генератор псевдо-случ чисел (использ текущее сист время по умолч)
    # for i in range(1,10):
    #    print(random.choice( alphabet ))

    bs = gen_bitsequence(l=128)  # Вызвать функцию генерации битовой последовательности
    print(bs, len(bs))

    test1 = nist_1_monobit(bs)
    print(f"Test1_monobit: {test1}")

    test2 = nist_2_runs( bs )
    print( f"Test2_runs: {test2}" )

