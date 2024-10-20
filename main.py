# main.py
import threading #support for creating and managing threads
import os #files and directory opreations
from mapper import map_files #imported from mapper.py
from reducer import reduce_files 

#creatinf and managing mapper and reducer threads
#it reads input files from the directory, 
#distributes among mapper threads
#and then processees the intermediate files using reducer threads

#       Configuration
N = 3  # Number of mapper threads should be bigger than 2 
M = 4  # Number of reducer threads should bugger than 2

#         Specify the path to the folder containing input files
input_folder_path = "/Users/nisankarsan/Desktop/map_ex/texts"  

def get_input_files(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]
    #filters the list to include only .txt files and constructs their full paths.


#main Function

def main():
    # get the list of input files from the specified folder
    input_files = get_input_files(input_folder_path)
    
    if not input_files:
        print(f"No .txt files found in {input_folder_path}")
        return

    # distribute input files among mappers
    files_per_mapper = [input_files[i::N] for i in range(N)] #each mapper thread gets a subset of the input files

    # create and start mapper threads
    mapper_threads = [] #initialize empty list to store mapper threads
    for i in range(N): #N is number of mapper
        thread = threading.Thread(target=map_files, args=(files_per_mapper[i], i, M))
        #creates a new thread for each mapper with map_files as the target function
        mapper_threads.append(thread) #adds the thread to the list of mapper threads
        thread.start()

    # wait for all mapper threads to complete
    for thread in mapper_threads:
        thread.join() #waits for each thread to complete

    print("Mapping phase completed.")

    # create and start reducer threads
    reducer_threads = [] #initialize empty list to store the reducer threads
    for i in range(M): 
        thread = threading.Thread(target=reduce_files, args=(i, N))
        reducer_threads.append(thread)
        thread.start()

    # Wait for all reducer threads to complete
    for thread in reducer_threads:
        thread.join()

    print("Reducing phase completed.")
    print("MapReduce job finished.")

if __name__ == "__main__":
    main()