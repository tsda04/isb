# -*- coding: utf-8 -*-
def run_cipher():
    try:
        with open('text1.txt', 'r', encoding='utf8') as f_text:
            text = f_text.read()

        with open('key.txt', 'r', encoding='utf8') as f_key:
            key = int(f_key.read())

        lines = text.splitlines()
        new_text = ''
        for char in text:
            if char.isalpha():
                is_upper = char.isupper()
                char_code = ord(char)

                if is_upper:
                    new_char_code = (char_code - ord('А') + key) % 32 + ord('А')
                else:
                    new_char_code = (char_code - ord('а') + key) % 32 + ord('а')
                new_char = chr(new_char_code)
            else:
                new_char = char
            new_text += new_char

        print(new_text)

        with open('new_file.txt', 'w', encoding='utf8') as f:
            f.write(new_text)
    except Exception as e:
        print('An error occurred: ', e)


if __name__ == '__main__':
    run_cipher()