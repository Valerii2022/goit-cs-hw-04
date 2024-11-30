import multiprocessing
import time

# Функція для пошуку ключових слів у файлі
def search_in_file(file_path, keywords, queue):
    results = {keyword: [] for keyword in keywords}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            for keyword in keywords:
                if keyword.lower() in content:
                    results[keyword].append(file_path)
        queue.put(results)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Функція для обробки файлів багатопроцесорним методом
def process_search(files, keywords):
    queue = multiprocessing.Queue()
    processes = []
    
    for file_path in files:
        process = multiprocessing.Process(target=search_in_file, args=(file_path, keywords, queue))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()  # Чекаємо завершення всіх процесів
    
    # Збираємо результати з черги
    results = {keyword: [] for keyword in keywords}
    while not queue.empty():
        result = queue.get()
        for keyword, paths in result.items():
            results[keyword].extend(paths)
    
    return results

# Приклад використання
if __name__ == "__main__":
    start_time = time.time()
    
    # Список файлів для обробки
    files = ["file1.txt", "file2.txt", "file3.txt"]
    keywords = ["keyword1", "keyword2", "keyword3"]
    
    # Розподіл файлів між процесами
    results = process_search(files, keywords)
    
    print("Results:", results)
    print(f"Multiprocessing approach took {time.time() - start_time} seconds")
