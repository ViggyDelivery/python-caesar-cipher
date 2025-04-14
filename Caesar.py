from google import genai
from google.genai import types
import time


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def read_txt(file_name):
    with open(file_name, 'r') as file:
        return file.readline()


def ai_check(result):
    client = genai.Client(api_key=read_txt("API_KEY.txt")) # Read in the API key from a text file
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a coherence classifier that determines whether sentences contain meaningful words or random gibberish. For each input sentence, evaluate if it consists of actual words forming a potentially meaningful sentence (even if unusual or grammatically imperfect). Respond with EXACTLY ONE WORD: - \"yes\" if the sentence contains real words that could potentially form a coherent thought - \"no\" if the sentence contains random characters, made-up words, or complete gibberish. Do not explain your reasoning or provide any additional text beyond your one-word answer."
        ),
        contents=result
    )
    if response.text == 'yes' or response.text == 'yes\n':
        return True
    else:
        return False


def find_shift(one_letter):
    cur_char_pos = alphabet.index(one_letter)
    i_pos = alphabet.index('I')
    return cur_char_pos - i_pos


def shift_char_back(cur_char, shift):
    if alphabet.index(cur_char) - shift >= 0:
        return alphabet[(alphabet.index(cur_char) - shift)]
    else:
        shift = 26 - shift
        return alphabet[(alphabet.index(cur_char) + shift)]


def shift_char_forward(cur_char, shift):
    return alphabet[(alphabet.index(cur_char) + shift) % 26]


def decrypt():
    user_input = input('Enter an encrypted message to decrypt: ').upper()
    input_list = user_input.split()
    shift = 0
    res = ""
    while shift < 26:
        if shift == 13:
            print("Going to sleep for a minute to reset RPM...")
            time.sleep(60)
        res = ""
        for i in range(len(input_list)):
            cur_str = input_list[i]
            new_str = ""
            for cur_char in cur_str:
                if cur_char.isalpha():
                    new_str += shift_char_back(cur_char, shift)
                else:
                    new_str += cur_char
            res += new_str + " "
        if ai_check(res):
            print(f'Shift is {shift}. Decrypted message is: {res}')
            break
        else:
            shift = shift + 1


def encrypt():
    user_input = input('Enter a message to encrypt: ').upper()
    input_list = user_input.split()
    shift_input = int(input('Enter your intended shift: '))
    res = ""
    for i in range(len(input_list)):
        cur_str = input_list[i]
        new_str = ""
        for cur_char in cur_str:
            if cur_char.isalpha():
                new_str += shift_char_forward(cur_char, shift_input)
            else:
                new_str += cur_char
        res += new_str + " "
    print(f'Encrypted message is {res}')


choice = int(input('Would you like to encrypt (press 1) or decrypt (press 2)? '))
if choice == 1:
    encrypt()
else:
    decrypt()
