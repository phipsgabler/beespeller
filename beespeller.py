#!/usr/bin/env python3

from sys import argv

if __name__ == '__main__':
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
                print(word)
