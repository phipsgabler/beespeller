#!/usr/bin/env python3

from sys import argv

if __name__ == '__main__':
    mandatory_letter = argv[1].lower()
    allowed_letters = set(argv[2].lower()) | set(mandatory_letter)

    with open('words_alpha.txt', 'r') as words:
        for line in words:
            word = line.rstrip('\n')
            
            if len(word) >= 4:
                candidate_letters = set(word.lower())
                if (mandatory_letter in candidate_letters and
                    candidate_letters.issubset(allowed_letters)):
                    print(word)
