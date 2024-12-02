from threading_search import keyword_search_threading
from multiprocessing_search import keyword_search_multiprocessing

if __name__ == "__main__":
    files = ["file1.txt", "file2.txt", "file3.txt"]
    keywords = ["first", "second", "third"] 

    print("=== Порівняння продуктивності ===")
    
    print("\n=== Багатопотоковий підхід ===")
    threading_results, threading_time = keyword_search_threading(files, keywords, max_threads=3)
    print("Результати:", threading_results)

    print("\n=== Багатопроцесорний підхід ===")
    multiprocessing_results, multiprocessing_time = keyword_search_multiprocessing(files, keywords, max_processes=3)
    print("Результати:", multiprocessing_results)

    print("\n=== Порівняння часу виконання ===")
    print(f"Threading: {threading_time:.6f} секунд")
    print(f"Multiprocessing: {multiprocessing_time:.6f} секунд")

