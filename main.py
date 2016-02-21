import json

filename = r"C:\Users\manasa\Documents\Caltech\CS144\Pandemaniac\Pandemaniac\test_json_file.txt"
out_file = "C:\Users\manasa\Documents\Caltech\CS144\Pandemaniac\Pandemaniac\output.txt"
data = {}

def get_seed_nodes(num_seeds):
    text_file = open(out_file, "w")
    for rnd in range(50):
        for i in range(num_seeds):
            text_file.write(str(i) + "\n")
    text_file.close()

def main():
    json_data = open(filename).read()
    
    data = json.loads(json_data)
    get_seed_nodes(4)

if __name__ == "__main__":
    main()