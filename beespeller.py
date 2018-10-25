#!/usr/bin/env python3

from sys import argv, exit
from os import getenv
import requests
import re


MW_API_URL = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/'
FORMATTING_TOKENS = re.compile('\{([\w/| ])+\}')

def lookup(key, query):
    r = requests.get(MW_API_URL + query, params = {'key': key})
    r.raise_for_status()

    return r.json()


def extract_first_definition(answer):
    first_entry = answer[0]

    if isinstance(first_entry, str):
        return '(no definition found)'
    else:
        first_def = first_entry['def'][0]
        first_sense = first_def['sseq'][0][0]
        if first_sense[0] == 'pseq': first_sense = first_sense[1][0]
        
        try:
            defining_text = first_sense[1]['dt'][0][1]
        except:
            print(first_entry)
            raise

        return re.sub(FORMATTING_TOKENS, '', defining_text)


def get_key():
    key = getenv("MERRIAM_WEBSTER_COLLEGIATE_KEY")
    
    if not key:
        exit("set the MERRIAM_WEBSTER_COLLEGIATE_KEY environmental variables"
             " to your Merriam-Webster API keys in order to perform lookups.")
    else:
        return key


if __name__ == '__main__':
    api_key = get_key()
    
    mandatory_letter = argv[1].lower()
    allowed_letters = frozenset(argv[2].lower()) | frozenset(mandatory_letter)
    
    def is_valid(word: str):
        if len(word) >= 4:
            candidate_letters = frozenset(word.lower())
            return (mandatory_letter in candidate_letters and
                    candidate_letters.issubset(allowed_letters))
        else:
            return False
    
    with open('words_alpha.txt', 'r') as wordfile:
        for word in (line.rstrip('\n') for line in wordfile):
            if is_valid(word):
                definition = extract_first_definition(lookup(api_key, word))
                print(f'{word} - {definition}')
