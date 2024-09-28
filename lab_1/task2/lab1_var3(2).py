import collections
import key_2


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
    result = [(char, count / total) for char, count in sorted_frequency if char != "\n"]
    return result


def create_key(text: str) -> dict:
    freq_cipher = frequency_analysis(text)
    freq_ru = {}
    with open("frequencies.txt", "r", encoding='utf-8') as f2:
        for line in f2:
            char, freq = line.split('=')
            freq_ru[char] = float(freq)

    # Сортировка по убыванию частоты
    sorted_freq_cipher = sorted(freq_cipher, key=lambda x: x[1], reverse=True)
    new_key = {fc[0]: fr[0] for fc, fr in zip(sorted_freq_cipher, freq_ru)}
    return new_key


def decrypt(text: str, key: dict) -> str:
    """
    Расшифровывает текст с помощью ключа.

    Args:
        text (str): Зашифрованный текст.
        key (str): Ключ для расшифровки.

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

    with open("cod3.txt", "r", encoding='utf-8') as f1:
        cipher_text = f1.read()

    if len(key_2.key) == 0:
        # если ключ еще не был создан
        key = create_key(cipher_text)
        print(f'Ключ шифрования: (для дальнейшей работы с ним вставьте его в файл key_2.py)')
        print(key)

    else:
        # если ключ был создан
        key = key_2.key
        print(f'Ключ шифрования загружен из key_2.py')

    #deciphered_text = decrypt(cipher_text, ''.join([k for k, _ in key.items()]))
    deciphered_text = decrypt(cipher_text, key)
    with open('cod3_decrypted.txt', 'w', encoding='utf-8') as f:
        f.write(deciphered_text)
    print(f'Расшифрованный текст записан в cod3_decrypted.txt')
    print(deciphered_text)
