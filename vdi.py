import requests
import threading
import queue

# إعداد عدد الخيوط
thread_count = 10

# إعداد قائمة الانتظار لتخزين الدلائل (wordlist)
q = queue.Queue()

# إعداد User-Agent
headers = {'User-Agent': 'Mozilla/5.0'}

# الدالة التي تقوم بالبحث عن الدلائل
def dir_fuzzer(target_url):
    while not q.empty():
        directory = q.get()
        url = f"{target_url}/{directory}"

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(f"[+] Found: {url}")
            elif response.status_code == 403:
                print(f"[-] Forbidden: {url}")
            else:
                pass  # تجاهل النتائج غير المفيدة
        except requests.exceptions.RequestException as e:
            print(f"[-] Error accessing {url}: {str(e)}")
        finally:
            q.task_done()

# تحميل قائمة الكلمات إلى قائمة الانتظار
def load_wordlist(wordlist_file):
    with open(wordlist_file, 'r') as f:
        for line in f:
            word = line.strip()
            if word:
                q.put(word)

# وظيفة رئيسية لتشغيل الأداة
def main():
    target_url = input("Enter the target URL (e.g., http://example.com): ")
    wordlist_file = input("Enter the path to the wordlist file: ")

    # تحميل قائمة الكلمات
    load_wordlist(wordlist_file)

    # إنشاء وإطلاق الخيوط
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=dir_fuzzer, args=(target_url,))
        threads.append(t)
        t.start()

    # انتظار اكتمال جميع الخيوط
    for t in threads:
        t.join()

    print("[+] Directory fuzzing completed!")

if __name__ == "__main__":
    main()
