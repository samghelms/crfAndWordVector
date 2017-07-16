import sys
from enchant import request_pwl_dict
import os
import csv
import itertools

class EnchantSpeller:
    def __init__(self, word_list = None, 
                pwl_loc = "/data/pwl",
                ):
        self.dict = None
        filepath = os.getcwd()+pwl_loc

        print filepath

        # load the dictionary for spell correction
        try: 
            print("loading pwl")
            self.dict = request_pwl_dict(filepath)
            if not self.dict.check("sigmaaldrich"):
                print("going to build")
                raise IOError
            print("loaded pwl")
        except IOError:
            print("building pwl")
            f = open(filepath,"w+")
            f.write("SAMUELHELMSISAWESOME"+ "\n")
            f.close()
            self.load_words(word_list, filepath)
            self.dict = request_pwl_dict(filepath)

    # NOTE: this is implemented on the correct, incorrect pairs dataset in data. Expects the proper spelling to follow a pipe
    # EX: 5 2gether | together
    def load_words(self, word_list, filepath):
        with open(word_list) as f:
            out_file = open(filepath, "w+")
            for i, line in enumerate(f):
                correctly_spelled_word = line.split("|")[0].strip().lower()
                print>>out_file, correctly_spelled_word
                if i % 100000 == 0:
                    print "loaded %d words" % i

    # checks to see if the mispellings get corrected
    # correct input for eval file: csv: line: CORRECT, INCORRECT
    def get_error_rate(self, word_list, verbose = False):
        wf = None
        if verbose == True:
            wf = open("spell_comparison.txt", "w")
        approx_correct = 0.0
        all_correct = 0.0
        total = 0.0
        no_correct_list = []
        approx_correct_list = []
        with open(word_list) as f:
            csvreader = csv.reader(f, delimiter=',', quotechar='"')
            # skip header
            csvreader.next()
            for line in csvreader:
                incorrectly_spelled_words = line[1].strip().lower()
                correctly_spelled_word = line[0].strip().lower()

                suggestions_matrix = []
                for w in incorrectly_spelled_words.split(" "):
                    if not self.dict.check(w):
                        suggestions_matrix.append(self.dict.suggest(w))

                suggestions = list(itertools.product(*suggestions_matrix))

                suggestion_list = [" ".join(el) for el in suggestions]

                # print suggestion_list
       
                if len(list(suggestions)) > 0 and " ".join(suggestions[0]) == correctly_spelled_word:
                    all_correct+=1
                elif len(list(suggestions)) > 0 and correctly_spelled_word in suggestion_list:
                    approx_correct += 1
                    approx_correct_list.append( (incorrectly_spelled_words, correctly_spelled_word, suggestions) )
                else:
                    no_correct_list.append( (incorrectly_spelled_words, correctly_spelled_word, suggestions) )

                total+=1

                if verbose == True:
                    print "term: " +incorrectly_spelled_words," || current suggestion: "+correctly_spelled_word+" || our suggests: "+" ".join(suggestion_list)

                    print>>wf, "term: " +incorrectly_spelled_words," || current suggestion: "+correctly_spelled_word+" || our suggests: "+" ".join(suggestion_list)

                if total % 10 == 0:
                    print("results:")
                    print "wholly correct rate: %f, somewhat correct rate: %f, total rate: %f" % (all_correct/total, approx_correct/total, (all_correct+approx_correct)/total)

                        # print("somewhat correct suggestion terms: ")
                        # print(approx_correct_list)
                        # print("no correct suggestion terms: ")
                        # print(no_correct_list)

    def get_suggestions(self, word):
        suggestions = self.dict.suggest(word)
        return suggestions # come up with a more advanced method for selecting which of the suggestion to return -- edit distance based?

    def check(self, word):
        return self.dict.check(word)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python EnchantSpeller.py word_list_name")
        exit(0)
    es = EnchantSpeller(sys.argv[1])

    print es.get_suggestions("0n")
    print es.check("sigmaaldrich")
    print es.get_suggestions("isooctyltrimethoxysilane")
    print es.get_suggestions("isooctyltrimethoxysilane")
    print es.get_suggestions("isooctyltrimethoxysilane")
    print es.get_suggestions("isooctyltrimethoxysilane")

    
