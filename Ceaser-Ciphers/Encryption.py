def encrypt_caesar(text, shift):
    result = ""

    for char in text:
        if char.isupper():
            base = ord('A')
            new_char = chr((ord(char) - base + shift) % 26 + base)
            result += new_char

        elif char.islower():
            base = ord('a')
            new_char = chr((ord(char) - base + shift) % 26 + base)
            result += new_char

        else:
            result += char  # leave symbols unchanged

    return result
