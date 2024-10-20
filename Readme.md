# Technical Report

## Abstract
This technical report presents a detailed analysis of a local parallel MapReduce implementation for word counting. The project utilizes Python's threading capabilities to create a system that processes multiple text files concurrently, counts word occurrences, and aggregates results efficiently. The implementation demonstrates parallel processing techniques for improved performance in text analysis tasks on a single machine.

## Introduction
The primary objective of this project was to develop a parallel word counting system capable of processing multiple text files simultaneously, distributing the workload across multiple threads, and aggregating the results efficiently. The implementation focuses on leveraging Python's threading module to create a local version of the MapReduce paradigm.

## Methodology
The implementation follows these key steps:
1. Input file distribution
2. Parallel mapping process
3. Intermediate file creation
4. Parallel reducing process
5. Final output generation

## File Structure

The project consists of three main Python files:
- `main.py`: Orchestrates the overall MapReduce process
- `mapper.py`: Contains the mapper function for processing input files
- `reducer.py`: Implements the reducer function for aggregating results

## Mapper Design
The mapper function in mapper.py processes input text files, cleans words, and distributes them into buckets based on their first character3

Key features include:
- Word cleaning using regular expressions
- Bucket assignment based on ASCII value of the first character modulo the number of reducers
- Writing cleaned words to intermediate files


### Word Cleaning
Initially, a list comprehension approach was attempted:

```python
def clean_word(word):
    return ''.join([char for char in word.lower() if char.isalnum()])
```
However, this method had issues with word splitting. The final implementation uses a more robust regex approach:

```python
def clean_word(word):
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', word.lower())
    return cleaned
```
This regex method is preferred for its robustness and scalability, making it more suitable for production environments.

### Word Splitting
The mapper uses regex to split words while keeping contractions intact:

```python
words = re.findall(r"\b[\w']+\b", line.lower())
```
This approach uses word boundaries (\b) to ensure accurate word splitting, including contractions.

### Bucket Assignment
Words are assigned to buckets based on their first character:
```python
bucket = ord(clean[0]) % M
```

This uses the ASCII value of the first character modulo the number of reducers (M) to determine the bucket.


```python
def clean_word(word):
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', word.lower())
    return cleaned

def mapper(input_files, mapper_id, M):
    for file in input_files:
        with open(file, 'r') as f:
            for line in f:
                words = re.findall(r"\b[\w']+\b", line.lower())
                for word in words:
                    clean = clean_word(word)
                    if clean:
                        bucket = ord(clean[0]) % M
                        with open(f'mr-{mapper_id}-{bucket}', 'a') as out:
                            out.write(f'{clean}\n')
```

## Reducer Design
The reducer function in reducer.py aggregates word counts from intermediate files2
1. It performs the following tasks:
2. Reading intermediate files created by mappers
3. Counting word occurrences
4. Writing final word counts to output files

```python
def reducer(reducer_id, N):
    word_counts = {}
    for i in range(N):
        with open(f'mr-{i}-{reducer_id}', 'r') as f:
            for line in f:
                word = line.strip()
                word_counts[word] = word_counts.get(word, 0) + 1
    
    with open(f'out-{reducer_id}', 'w') as f:
        for word, count in word_counts.items():
            f.write(f'{word}: {count}\n')
```
The `reducer_id` is used to identify which reducer instance is processing the intermediate files, ensuring that each reducer processes the correct subset of data.

### File Handling
The implementation uses a specific naming convention for intermediate and output files:
- Intermediate files: `mr-{mapper_id}-{bucket}`
- Output files: `out-{reducer_id}`

This naming convention allows for efficient distribution and processing of data across multiple mappers and reducers.

## Main File



### Thread Management
The main.py file manages thread creation and execution
1. Creates and starts mapper threads
2. Waits for mapper threads to complete
3. Creates and starts reducer threads
4. Waits for reducer threads to complete

```python
def main():
    input_files = get_input_files(input_folder_path)
    files_per_mapper = [input_files[i::N] for i in range(N)]

    mapper_threads = []
    for i in range(N):
        thread = threading.Thread(target=map_files, args=(files_per_mapper[i], i, M))
        mapper_threads.append(thread)
        thread.start()

    for thread in mapper_threads:
        thread.join()

    reducer_threads = []
    for i in range(M):
        thread = threading.Thread(target=reduce_files, args=(i, N))
        reducer_threads.append(thread)
        thread.start()

    for thread in reducer_threads:
        thread.join()
```

### File Handling
The implementation uses a specific naming convention for intermediate and output files:
Intermediate files: `mr-{mapper_id}-{bucket}` Output files: `out-{reducer_id}`

## Results
The implementation successfully processes multiple text files in parallel, distributing the workload across mapper and reducer threads. The system effectively counts word occurrences and aggregates results, demonstrating the principles of parallel processing on a local machine.

