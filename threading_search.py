import threading
import time

def search_keywords_thread(files, keywords, results, buffer_size=1024):
    for file_path in files:
        try:
            file_results = {keyword: False for keyword in keywords}  
            with open(file_path, 'r', encoding='utf-8') as file:
                while True:
                    buffer = file.read(buffer_size).lower()
                    if not buffer:
                        break
                    for keyword in keywords:
                        if keyword in buffer and not file_results[keyword]:  
                            results[keyword].append(file_path)
                            file_results[keyword] = True  
                            break  
        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")



def keyword_search_threading(files, keywords, max_threads=3, buffer_size=1024):
    start_time = time.time()
    threads = []
    results = {keyword: [] for keyword in keywords}
    files_per_thread = len(files) // max_threads + (len(files) % max_threads > 0)

    for i in range(max_threads):
        thread_files = files[i * files_per_thread:(i + 1) * files_per_thread]
        thread = threading.Thread(target=search_keywords_thread, args=(thread_files, keywords, results, buffer_size))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    elapsed_time = time.time() - start_time
    print(f"Threading виконано за {elapsed_time:.6f} секунд.")
    return results, elapsed_time


