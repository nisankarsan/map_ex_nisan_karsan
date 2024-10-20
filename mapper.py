# mapper.py

import re  #provides support for regular expressions
#it processes iput text files,
#cleans the words and distributes them into buckets based on the the first character of each word
# the cleaned words are then written to intermediate files that will be used by reducers
# mr - mapper id - bucket 


def clean_word(word):
    # remove non-alphanumeric characters and convert to lowercase
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', word.lower()) #cleans a word by converting lowercase
    return cleaned


def mapper(input_files, mapper_id, M):  
    #this function processes a list of input files, cleans the words,
    #and writes them to intermediate files(reducer use this then)
#mapper_id is a identifier for the mapper used to intermediate files
#M the number of reducers for useinf to determine the bucket for each word

    for file in input_files: 
        try:
            with open(file, 'r') as f: 
                for line in f: #iterates over each file in the file
                    # Use regex to split words, keeping contractions intact
                    words = re.findall(r"\b[\w']+\b", line.lower()) 
                    #line.lower converts line to lowercase 
                    # re.findall finds all words (incl contractions)

                    for word in words:
                        clean = clean_word(word)
                        if clean:
                            #Intermediate Files: Named mr-{mapper_id}-{bucket}, 
                            #where bucket is determined by the first character of the cleaned word, 
                            #modulo the number of reducers (M).
                            bucket = ord(clean[0]) % M  # M=4 (reducer)
                            #uses the ASCII value for first character of cleaned word, modulo M, to determine the bucket
                            with open(f'mr-{mapper_id}-{bucket}', 'a') as out:
                                out.write(f'{clean}\n')
        except IOError as e:
            print(f"Error reading file {file}: {e}")


def map_files(input_files, mapper_id, M): #for calling from main.py
    mapper(input_files, mapper_id, M)
# it provides a simple target for creting mapper threads. this makes the threading code clener and more readable
