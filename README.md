# Python Mini Search Engine

A lightweight, local search engine built in Python that indexes and searches through a directory of text (`.txt`) files. 

This project was developed as my final project for **Stanford University's Code in Place** program.

## Features
- **Inverted Indexing**: Scans and indexes documents upfront using nested dictionaries for blazing-fast lookups.
- **Multi-Word Search**: Filters results to only include files containing *all* search terms.
- **Contextual Snippets**: Highlights the matched search terms inside a text snippet with surrounding context.
- **Clean UI**: Extracts the first sentence of files to use as clean, readable titles in the search results.

## How it Works
1. Run the script and provide a folder path containing `.txt` files.
2. The engine normalizes the text (lowercasing, removing punctuation) and builds an index mapping words to their exact file and position.
3. Enter a query, and the engine will instantly return matching documents along with formatted text snippets showing exactly where your words appear!

## Usage
Run the script using Python:
```bash
python "CIP mini search engine.py"
```
