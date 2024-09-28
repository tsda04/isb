import os
import collections

def frequency_analysis(text : str) -> list:
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
    result = [(char, count / total) for char, count in sorted_frequency]
    return result
def decrypt(text : str, key : str) -> str:
    """
    Расшифровывает текст с помощью ключа.

    Args:
        text (str): Зашифрованный текст.
        key (str): Ключ для расшифровки.

    Returns:
        str: Расшифрованный текст.
    """
    translated = ''
    chars_a = key
    chars_b = ' ОИЕАНТСРВМЛДЯКПЗЫЬУЧЖГХФЙЮБЦШЩЭЪ'
    for symbol in text:
        if symbol in chars_a:
            sym_index = chars_a.find(symbol)
            translated += chars_b[sym_index]
        else:
            translated += symbol
    return translated

if __name__ == "__main__":

    with open("cod3.txt", "r", encoding='utf-8') as f:
        cipher_text = f.read()

    freq_cipher = frequency_analysis(cipher_text)
    freq_ru = {}
    with open("frequencies.txt", "r", encoding='utf-8') as f:
        for line in f:
            char, freq = line.split('=')
            freq_ru[char] = float(freq)

    # Сортировка по убыванию частоты
    sorted_freq_cipher = sorted(freq_cipher, key=lambda x: x[1], reverse=True)
    key = {fc[0]: fr[0] for fc, fr in zip(sorted_freq_cipher, freq_ru)}
    print(f'Ключ шифрования: (для дальнейшей работы с ним вставьте его в файл key2.py)')
    print(key)

    deciphered_text = decrypt(cipher_text, ''.join([k for k, _ in key.items()]))
    with open('cod3_decrypted.txt', 'w', encoding='utf-8') as f:
        f.write(deciphered_text)

    print(f'Расшифрованный текст записан в cod3_decrypted.txt')
