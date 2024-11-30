import threading
import time

# Функція для пошуку ключових слів у файлі
def search_in_file(file_path, keywords, results):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            for keyword in keywords:
                if keyword.lower() in content:
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Функція для обробки файлів багатопотоковим методом
def thread_search(files, keywords):
    results = {keyword: [] for keyword in keywords}
    threads = []
    
    for file_path in files:
        thread = threading.Thread(target=search_in_file, args=(file_path, keywords, results))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()  # Чекаємо завершення всіх потоків
    
    return results

# Приклад використання
if __name__ == "__main__":
    start_time = time.time()
    
    # Список файлів для обробки
    files = ["file1.txt", "file2.txt", "file3.txt"]
    keywords = ["keyword1", "keyword2", "keyword3"]
    
    # Розподіл файлів між потоками
    results = thread_search(files, keywords)
    
    print("Results:", results)
    print(f"Threading approach took {time.time() - start_time} seconds")
