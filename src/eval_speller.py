from spell_corrector.enchant.EnchantSpeller import EnchantSpeller
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python eval_speller.py evaluation.csv")
        exit(0)
    es = EnchantSpeller()

    evals = sys.argv[1]
    es.get_error_rate(evals)


    
