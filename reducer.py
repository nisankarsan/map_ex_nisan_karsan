# reducer.py

 #this reducer function process intermediate files created by mappers, aggregated word counts, 
 #and write the result on output file


def reducer(reducer_id, N): 
    #reducer_id is identifer which reducer instance is proceesing the intermediate files
    

    word_counts = {} #empty dictionary to store word counts

    #read intermediate files created by the mapper function
    for i in range(N):
        try:
            with open(f'mr-{i}-{reducer_id}', 'r') as f:
                for line in f:
                    word = line.strip() #Strips any leading or trailing whitespace from the line to get the word.
                    word_counts[word] = word_counts.get(word, 0) + 1 #updates the word count in the word_counts dictionary
        except IOError as e:
            print(f"Error reading intermediate file mr-{i}-{reducer_id}: {e}")
    
    try:
        with open(f'out-{reducer_id}', 'w') as f:
            for word, count in word_counts.items(): #iterates over the items in the word_counts dictionary
                f.write(f'{word}: {count}\n') #writes each word ans its count to output file writing the file
    except IOError as e:
        print(f"Error writing output file out-{reducer_id}: {e}")

def reduce_files(reducer_id, N):
    reducer(reducer_id, N)

