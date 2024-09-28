import collections
import my_key_2 as my_key_2


def frequency_analysis(text: str) -> list:
    """
    Проводит частотный анализ текста.

    Args:
        text (str): Текст для анализа.

    Returns:
        list: Список пар (буква, частота).
    """
    frequency = collections.Counter(text)
    total = sum(frequency.values())
    sorted_frequency = sorted(frequency.items(), key=lambda x: x[1])
    result = [(char, count / total)
              for char, count in sorted_frequency if char != "n"]
    return result


def create_key(text: str) -> dict:
    """
    Создает ключ сопоставляя результаты частотного анализа текста
    и частоту букв в русском алфавите

    Args:
        text (str): Зашифрованный текст.

    Returns:
        dict: Словарь с ключами для декодирования (буква1: буква2)
    """
    freq_cipher = frequency_analysis(text)
    freq_ru = {}
    try:
        with open("frequencies.txt", "r", encoding='utf-8') as f2:
            for line in f2:
                char, freq = line.split('=')
                freq_ru[char] = float(freq)
    except FileNotFoundError:
        print("Файл frequencies.txt не найден. Ключ не может быть создан.")
        return {}
    except Exception as e:
        print(f"Ошибка при чтении файла frequencies.txt: {e}")
        return {}

    # Сортировка по убыванию частоты
    sorted_freq_cipher = sorted(
        freq_cipher, key=lambda x: x[1], reverse=True)
    new_key = {
        fc[0]: fr[0]
        for fc, fr in zip(sorted_freq_cipher, freq_ru)
    }
    return new_key


def decrypt(text: str, key: dict) -> str:
    """
    Расшифровывает текст с помощью ключа.

    Args:
        text (str): Зашифрованный текст.
        key (dict): Ключ для расшифровки.

    Returns:
        str: Расшифрованный текст.
    """
    translated = ''
    chars_a = key.keys()
    for symbol in text:
        if symbol in chars_a:
            translated += key.get(symbol)
        else:
            translated += symbol
    return translated


if __name__ == "__main__":

    try:
        with open("cod3.txt", "r", encoding='utf-8') as f1:
            cipher_text = f1.read()
    except FileNotFoundError:
        print("Файл cod3.txt не найден. Дешифровка невозможна.")
        exit()
    except Exception as e:
        print(f"Ошибка при чтении файла cod3.txt: {e}")
        exit()

    if len(my_key_2.key) == 0:
        # если ключ еще не был создан
        key = create_key(cipher_text)
        if key:  # Проверяем, что ключ был создан успешно
            print(
                f'Ключ шифрования: (для дальнейшей работы с ним вставьте его в файл my_key_2.py)')
            print(key)
        else:
            exit()  # Выход из программы, если ключ не создан
    else:
        # если ключ был создан
        key = my_key_2.key
        print(f'Ключ шифрования загружен из my_key_2.py')

    deciphered_text = decrypt(cipher_text, key)
    try:
        with open('cod3_decrypted.txt', 'w', encoding='utf-8') as f:
            f.write(deciphered_text)
        print(f'Расшифрованный текст записан в cod3_decrypted.txt')
        print()
        print(deciphered_text)
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")
