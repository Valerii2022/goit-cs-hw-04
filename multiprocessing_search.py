from multiprocessing import Process, Queue, Manager
import time

def search_keywords_process(file_queue, keywords, results, buffer_size=1024):
    while not file_queue.empty():
        try:
            file_path = file_queue.get_nowait()
            file_results = {keyword: False for keyword in keywords}  
            with open(file_path, 'r', encoding='utf-8') as f:
                while True:
                    buffer = f.read(buffer_size).lower()  
                    if not buffer:
                        break
                    for keyword in keywords:
                        if keyword in buffer and not file_results[keyword]: 
                            results[keyword].append(file_path)
                            file_results[keyword] = True  
                            break  
        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")


def keyword_search_multiprocessing(files, keywords, max_processes=3, buffer_size=1024):
    start_time = time.time()
    file_queue = Queue()
    for file in files:
        file_queue.put(file)

    with Manager() as manager:
        results = manager.dict({keyword: manager.list() for keyword in keywords})
        processes = []

        for _ in range(max_processes):
            process = Process(target=search_keywords_process, args=(file_queue, keywords, results, buffer_size))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        results_dict = {key: list(results[key]) for key in results}
    
    elapsed_time = time.time() - start_time
    print(f"Multiprocessing виконано за {elapsed_time:.6f} секунд.")
    return results_dict, elapsed_time
