import os
import string

def clean_token(token):
    lowercase_token_token = token.lower()
    cleaned_token = lowercase_token_token.strip(string.punctuation)
    return cleaned_token

def build_index(folder):
    index = {}
    titles = {}
    files = os.listdir(folder)
    for file in files:
        filepath = os.path.join(folder, file)
        with open(filepath, "r", encoding="utf-8") as file_reader:
            content = file_reader.read()
            if '.' in content:
                sentences = content.split('.')
                first_sentence = sentences[0]
                title = first_sentence.strip()
            else:
                title = content.strip()
            titles[file] = title
            words = content.split()
            for position, word in enumerate(words):
                cleaned = clean_token(word)
                if cleaned:
                    if cleaned not in index:
                        index[cleaned] = {}
                    if file not in index[cleaned]:
                        index[cleaned][file] = []
                    index[cleaned][file].append(position)
    return index, titles

def execute_search(index, query):
    split_words = query.split()
    words = []
    for w in split_words:
        words.append(clean_token(w))
    query_words = []
    for w in words:
        if w != "":  
            query_words.append(w)
    if len(query_words) == 0:
        return []
    first_word = query_words[0]
    if first_word not in index:
        return []
    results = list(index[first_word])
    for word in query_words[1:]:
        if word not in index:
            return []
        new_results = []
        for file in results:
            if file in index[word]:
                new_results.append(file)
        results = new_results
    return results

def get_ordinal(n):
    if 11 <= n % 100 <= 13:
        suffix = "th"
    elif n % 10 == 1:      
        suffix = "st"
    elif n % 10 == 2:
        suffix = "nd"
    elif n % 10 == 3:
        suffix = "rd"
    else:
        suffix = "th"
    return str(n) + suffix

    
def get_snippet(folder, file, pos):
    filepath = os.path.join(folder, file)
    with open(filepath, "r", encoding="utf-8") as file_reader:
        title = file_reader.readline().strip()
        file_reader.seek(0)
        content = file_reader.read()
        words = content.split()
        start = max(0, pos - 10)
        end = min(len(words), pos + 11)
        snippet_words = words[start:end]
        
        target_idx = pos - start
        if 0 <= target_idx < len(snippet_words):
            snippet_words[target_idx] = "[" + snippet_words[target_idx].upper() + "]"
            
        snippet = " ".join(snippet_words)
        
        if start > 0:
            snippet = "... " + snippet
        if end < len(words):
            snippet = snippet + " ..."
            
        return snippet
        

def main():
    folder = input("Enter the folder path you want to index: ")
    index, titles = build_index(folder)
    print("Index built successfully!")
    while True:
        query = input("Search query (or press Enter to exit): ")
        if query == "":
            break
        results = execute_search(index, query)
        if len(results) == 0:
            print("No matching files found.")
        else:
            print("Results:")
            search_terms = []
            for word in query.split():
                cleaned = clean_token(word)
                if cleaned:
                    search_terms.append(cleaned)
            for file in results:
                print("- " + titles[file] + " (" + file + ")")
                print()
            show_snippets = input("Would you like to view snippets? (y/n): ").strip().lower()
            if show_snippets == 'y':
                print("\nSnippets:")
                for file in results:
                    print("- " + titles[file] + " (" + file + ")")
                    for term in search_terms:
                        positions = index[term][file]
                        print("  * '" + term + "' appears " + str(len(positions)) + " time(s):")
                        for idx, pos in enumerate(positions):
                            rank = get_ordinal(idx + 1)
                            snippet = get_snippet(folder, file, pos)
                            print("    - " + rank + " time at word position " + str(pos) + ":")
                            print("      \"" + snippet + "\"")
        print()


if __name__ == '__main__':
    main()