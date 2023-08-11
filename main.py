import time
import random
from colors import red, green, yellow, magenta, bold, reset
from art import vigenere, cipher

# Polyalphabetic cipher
alphabet = [letter for letter in "abcdefghijklmnopqrstuvwxyz"]


def welcome():
    print(f"{yellow}Welcome to Kylo's {reset}")
    print(vigenere, cipher)
    print(f"{bold}Introduction{reset}\n")
    print(f"{magenta}The Vigenère cipher is a polyalphabetic substitution algorithm that aims to disguise \
the letter distribution in your ciphertext,\nwhich makes it more challenging for third parties to \
decrypt, as it uses multiple substitution alphabets.\nThis encryption algorithm requires a keyword and \
transforms it into a matrix with corresponding positions in the English alphabet of each letter.\nOnce the \
length of the plaintext is calculated, the key is adjusted to match the length of \
plaintext.\nConsequently, each letter is shifted by the corresponding key from the matrix.\nNote \
that, this cipher algorithm does not encrypt spaces, digits and any other special characters.{reset}\n")
    print("Please do not use any special characters.")
    print(f"Now you will be asked to enter the key word. It {bold}must not{reset} contain any digits!\n\
Any uppercase letters will be converted to lowercase and whitespaces will be removed from the key.\n")


def key_as_numbers(usr_key) -> list:
    """Returns a list of indexed letters from the key"""
    # creates a list of numbers derived from the position of each letter
    # from the usr_key in the English alphabet
    # + 1 is required, so that the letter "a" does not result in 0, which will make it unusable for shifting
    indexed_key = [alphabet.index(letter) + 1 for letter in usr_key]
    return indexed_key


def go_again() -> bool:
    """Returns True if the user wants to go again, otherwise,
    it returns False."""
    options = ["Y", "N"]
    restart = input('Do you want to restart the program? (Y/N)\n>').upper()
    # keep asking the user until the received input is either "Y" or "N"
    while restart not in options:
        print("Invalid input.")
        restart = input(input('Do you want to restart the program? (Y/N)\n>').upper())
    if restart == options[0]:
        return True

    time.sleep(.5)
    print("Closing program.")
    time.sleep(1)
    print(f"Terminating {random.randint(0, 100)} processes...")
    time.sleep(2)
    print("Almost there.")
    time.sleep(2)

    # 15% chance of a fake program failure
    decision = random.randint(1, 100)
    if decision <= 15:
        print("Critical Failure!")
        time.sleep(.5)
        print("Please, DO NOT shut down your device!")
        time.sleep(.5)
        print("Resolving dependencies...")
        time.sleep(.5)
        print("Fetching missing data...")
        time.sleep(2)
        print(f"{red}Program has encountered issues with terminating (...) processes{reset}")
    else:
        print(f"\n{green}Success! Process finished with exit code 0{reset}")
    return False


def match(usr_text, usr_key) -> list:
    """Generates a key with a corresponding length to the plaintext"""
    whitespace_indexes = []
    uppercase_indexes = []
    digits_indexes = []
    chars_indexes = []
    digits_dict = {}
    chars_dict = {}

    usr_key_length = len(usr_key)

    text_as_list = [x for x in usr_text]

    # registers the indexes of spaces, digits and capital letters
    current_pos = 0
    for character in text_as_list:
        if character == " ":
            whitespace_indexes.append(current_pos)
        elif character.isnumeric():
            digits_indexes.append(current_pos)
            digits_dict[current_pos] = character
        elif character.isupper():
            uppercase_indexes.append(current_pos)
            text_as_list[current_pos] = character.lower()
        elif not(character.isalnum()):
            chars_indexes.append(current_pos)
            chars_dict[current_pos] = character
        current_pos += 1

    # if len(whitespace_indexes) > 0:
    #     print(f"Space(s) found at indexes: {whitespace_indexes}")
    # if len(uppercase_indexes) > 0:
    #     print(f"Capital letter(s) found at indexes: {uppercase_indexes}")
    # if len(digits_indexes) > 0:
    #     print(f"Digit(s) found at indexes: {digits_indexes}")
    # if len(chars_indexes) > 0:
    #     print(f"Special character(s) found at indexes: {chars_indexes}")

    other_indexes = []
    other_indexes.extend(whitespace_indexes)
    other_indexes.extend(digits_indexes)
    other_indexes.extend(chars_indexes)

    other_indexes.sort(reverse=True)  # sorts other indexes in reverse, so it removes the unwanted
    # characters in the right order without destroying the plaintext
    digits_indexes.sort(reverse=True)
    whitespace_indexes.sort(reverse=True)
    uppercase_indexes.sort(reverse=True)

    ready_for_encryption = text_as_list.copy()
    # takes the copy of text_as_list and removes indexes from the list 'other indexes'
    # this removes digits and spaces, but leaves the indexes of capital letters
    # because they have been temporarily converted to lowercase to allow for encryption/decryption
    for item in other_indexes:
        ready_for_encryption.pop(item)

    ready_length = len(ready_for_encryption)  # length of the list without uppercase, digits and spaces
    # used to check if the key is long enough to begin encryption/decryption

    # repeats the sequence of the key as long as the length of plaintext is longer than the key
    while ready_length > usr_key_length:
        usr_key.extend(usr_key)
        usr_key_length = len(usr_key)

    while ready_length < usr_key_length:
        usr_key.pop()
        usr_key_length = len(usr_key)

    # all_indexes will be used in the insert_chars function
    all_indexes = []
    all_indexes.extend(whitespace_indexes)
    all_indexes.extend(digits_indexes)
    all_indexes.extend(uppercase_indexes)
    all_indexes.extend(chars_indexes)

    return [ready_for_encryption, usr_key, whitespace_indexes, uppercase_indexes, digits_indexes, chars_indexes,
            digits_dict, chars_dict, all_indexes]


def encrypt(usr_plaintext, usr_key) -> str:
    """Encrypts user plaintext given an array with the key."""
    c_text = ""
    # take the length of the usr_key (equal to the length of usr_plaintext) and use it as range
    for i in range(len(usr_key)):
        # find the index of the current letter in the alphabet
        current_letter = alphabet.index(usr_plaintext[i])
        # add the current key to the index of the first letter, which shifts the position to give a new index
        current_letter += usr_key[i]
        # find the mod of current_letter, so it does not give an index error
        current_letter = current_letter % 26
        # append the new shifted letter to ciphertext
        c_text += alphabet[current_letter]
    return c_text


def decrypt(usr_ciphertext, usr_key) -> str:
    """Decrypts user ciphertext given an array with the key."""
    p_text = ""
    # similarly to the encrypt function, create a range between 0 and the length of the ciphertext
    for i in range(len(usr_ciphertext)):
        # find the index of the current letter in the alphabet
        current_letter = alphabet.index(usr_ciphertext[i])
        # subtract the key to get a new shift
        current_letter -= usr_key[i]
        # the mod operator will result in the positive index of the new letter to be used as a substitute
        current_letter = current_letter % 26
        # append decrypted letter to plaintext
        p_text += alphabet[current_letter]
    return p_text


def insert_chars(text, indexes, spaces, uppercase, digits, chars, digits_dict, chars_dict) -> str:
    """Inserts special characters back into plaintext/ciphertext and replace uppercase letters"""
    text_as_list = [letter for letter in text]
    indexes.sort(reverse=False)

    for item in indexes:
        if item in spaces:
            text_as_list.insert(item, " ")
        elif item in uppercase:
            text_as_list[item] = text_as_list[item].upper()
        elif item in digits:
            text_as_list.insert(item, digits_dict[item])
        elif item in chars:
            text_as_list.insert(item, chars_dict[item])

    final_text = "".join(text_as_list)
    return f"{final_text}\n"


running = True
welcome()

while running:
    key = input("Enter the key word: ").replace(" ", "")

    while not key.isalpha():
        print("Key cannot contain numbers!")
        key = input("Re-enter key: ")
    key = key.lower()
    key = key_as_numbers(key)
    user_text = input("Enter plaintext/ciphertext: ")

    choices = ["1", "2"]
    ask = input("Enter 1 for encryption.\nEnter 2 for decryption\n>")
    while ask not in choices:
        print("You MUST enter either 1 or 2!")
        ask = input(">")

    result = match(user_text, key)
    if ask == choices[0]:
        ciphertext = encrypt(result[0], result[1])
        print(insert_chars(ciphertext, result[8], result[2], result[3], result[4], result[5], result[6], result[7]))
    else:
        plaintext = decrypt(result[0], result[1])
        print(insert_chars(plaintext, result[8], result[2], result[3], result[4], result[5], result[6], result[7]))

    running = go_again()
