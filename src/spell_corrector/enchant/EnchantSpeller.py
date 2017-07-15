import sys
from enchant.pypwl import PyPWL
import os

class EnchantSpeller:
    def __init__(self, word_list = None, 
                pwl_loc = "/src/spell_corrector/enchant/pwl",
                ):
        self.dict = None
        filepath = os.getcwd()+pwl_loc

        # load the dictionary for spell correction
        try: 
            self.dict = PyPWL(filepath)
            print("loading pwl")
        except IOError:
            print("building pwl")
            f = open(filepath,"w+")
            f.write("SAMUELHELMSISAWESOME"+ "\n")
            f.close()
            self.dict = PyPWL(filepath)
            self.load_words(self.dict, word_list)
            # self.get_error_rate(self.dict, word_list)

    # NOTE: this is implemented on the correct, incorrect pairs dataset in data. Expects the proper spelling to follow a pipe
    # EX: 5 2gether | together
    def load_words(self, d, word_list):
        with open(word_list) as f:
            for line in f:
                correctly_spelled_word = line.split("|")[1].strip().lower()
                d.add(correctly_spelled_word)
                
    # checks to see if the mispellings get corrected
    def get_error_rate(self, d, word_list, verbose = False):
        approx_correct = 0.0
        all_correct = 0.0
        total = 0.0
        no_correct_list = []
        approx_correct_list = []
        with open(word_list) as f:
            for line in f:
                incorrectly_spelled_word = line.split("|")[0].split("\t")[1].strip().lower()
                correctly_spelled_word = line.split("|")[1].strip().lower()
                suggestions = d.suggest(incorrectly_spelled_word)
       
                if len(suggestions) > 0 and suggestions[0] == correctly_spelled_word:
                    all_correct+=1
                elif len(suggestions) > 0 and correctly_spelled_word in suggestions:
                    approx_correct += 1
                    approx_correct_list.append( (incorrectly_spelled_word, correctly_spelled_word, suggestions) )
                else:
                    no_correct_list.append( (incorrectly_spelled_word, correctly_spelled_word, suggestions) )

                total+=1

                if total % 10 == 0:
                    print("results:")
                    print "wholly correct rate: %f, somewhat correct rate: %f, total rate: %f" % (all_correct/total, approx_correct/total, (all_correct+approx_correct)/total)
                    if verbose == True:
                        print("somewhat correct suggestion terms: ")
                        print(approx_correct_list)
                        print("no correct suggestion terms: ")
                        print(no_correct_list)

    def get_suggestions(self, word):
        suggestions = self.dict.suggest(word)
        return suggestions[0:3] # come up with a more advanced method for selecting which of the suggestion to return -- edit distance based?

    def check(self, word):
        return self.dict.check(word)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python EnchantSpeller.py word_list_name")
        exit(0)
    es = EnchantSpeller(sys.argv[1])

    print es.get_suggestions("0n")

    # es2 = EnchantSpeller()

    
