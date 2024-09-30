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
    значимость: пороговый уровень P-значения для принятия НУЛЕВОЙ гипотезы.
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


if __name__ == '__main__':
    alphabet = '01'
    # random.seed()   # Инициализировать генератор псевдо-случ чисел (использ текущее сист время по умолч)
    # for i in range(1,10):
    #    print(random.choice( alphabet ))

    bs = gen_bitsequence(l=128)  # Вызвать функцию генерации битовой последовательности
    print(bs, len(bs))

    test1 = nist_1_monobit(bs)
    print(f"Test1_monobit: {test1}")
