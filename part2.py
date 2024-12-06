# Group #: 24
# Student Names: Julien Mo, Tyler Lissel, Grayson Vanderzalm

import threading
import queue
import time, random

# Constants
BUFFER_SIZE = 10  # Max size of the queue
NUM_PRODUCERS = 4
NUM_CONSUMERS = 5
ITEMS_TO_PRODUCE = 20  # Total items to be produced by each producer
PRODUCTION_DELAY = (0.1, 0.5)  # Delay range for producing items (seconds)
CONSUMPTION_DELAY = (0.1, 0.5)  # Delay range for consuming items (seconds)



def consumerWorker(id: int, shared_queue: queue):
    """target worker for a consumer thread"""
    while True:
        try:
            item = shared_queue.get(timeout=2)  # Timeout to avoid infinite blocking
            time.sleep(random.uniform(*CONSUMPTION_DELAY))  # Simulate consumption time
            print(f"Consumer {id} consumed: {item}")
            shared_queue.task_done()
        except queue.Empty:
            # Exit when there are no more items to consume and the queue is empty
            break

def producerWorker(id: int, shared_queue: queue):
    """target worker for a producer thread"""
    for i in range(ITEMS_TO_PRODUCE):
        item = f"Item-{id}-{i}"  # Create an identifiable item
        time.sleep(random.uniform(*PRODUCTION_DELAY))  # Simulate production time
        shared_queue.put(item)
        print(f"Producer produced: {item}")


if __name__ == "__main__":
    # Create and start producer threads

    # Shared queue
    buffer = queue.Queue(maxsize=BUFFER_SIZE) 

    producer_threads = []
    for i in range(NUM_PRODUCERS):
        thread = threading.Thread(target=producerWorker, args=(i,buffer,))
        producer_threads.append(thread)
        thread.start()

    # Create and start consumer threads
    consumer_threads = []
    for i in range(NUM_CONSUMERS):
        thread = threading.Thread(target=consumerWorker, args=(i,buffer,))
        consumer_threads.append(thread)
        thread.start()

    # Wait for all producer threads to finish
    for thread in producer_threads:
        thread.join()

    # Wait for all items in the queue to be processed
    buffer.join()

    # Wait for all consumer threads to finish
    for thread in consumer_threads:
        thread.join()

    print("All tasks are completed.")
