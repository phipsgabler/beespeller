#!/usr/bin/env python3

from sys import argv, exit
from os import getenv
import requests
import re


MW_API_URL = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/'
TOKEN_FORMAT_NAMES = ['b', 'bc', 'inf', 'it', 'ldquo', 'rdquo', 'sc', 'sup', 'gloss', 'parahw',
                      'phrase', 'qword', 'wi', 'dx', 'dx_def', 'dx_ety', 'ma', 'ds']
FORMATTING_TOKENS = '|'.join(f'(\\{{{t}\\}})|(\\{{/{t}\\}})' for t in TOKEN_FORMAT_NAMES)
FORMATTING_TOKENS_RE = re.compile(FORMATTING_TOKENS)

def lookup(key, query):
    r = requests.get(MW_API_URL + query, params = {'key': key})
    r.raise_for_status()

    return r.json()


def extract_first_definition(answer):
    first_entry = answer[0]

    if isinstance(first_entry, str):
        return '(no definition found)'
    else:
        first_sseq = first_entry['def'][0]['sseq']
        
        if first_sseq[0][0][0] == 'pseq':
            first_sseq = first_sseq[0][0][1][0]

        if first_sseq[0][0][0] != 'bs':
            first_sense = first_sseq[0][0]
        else:
            first_sense = first_sseq[0][1]
        
        try:
            defining_text = first_sense[1]['dt'][0][1]
        except:
            print(first_sseq)
            print(first_sense)
            raise

        try:
            return FORMATTING_TOKENS_RE.sub('', defining_text)
        except:
            print(defining_text)


def get_key():
    key = getenv("MERRIAM_WEBSTER_COLLEGIATE_KEY")
    
    if not key:
        exit("set the MERRIAM_WEBSTER_COLLEGIATE_KEY environmental variables"
             " to your Merriam-Webster API keys in order to perform lookups.")
    else:
        return key


if __name__ == '__main__':
    # print(REMOVED_TOKENS)
    # 1/0
    
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
