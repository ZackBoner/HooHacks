import pickle

def read_file(name):
    file = open(name, 'r', encoding="utf8") 
    lines = file.readlines()

    values = []
    for line in lines:
        values.append(line.strip())
    return values

ticker_symbols = set(read_file("all_symbols.txt"))

pickle.dump(ticker_symbols, open("ticker_symbols.pkl", "wb"))