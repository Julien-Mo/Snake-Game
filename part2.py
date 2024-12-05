# Group #: 24
# Student names: Julien Mo, Grayson Vanderzalm, Tyler Lissel

import threading
import queue
import time, random

# Constants
NUM_PRODUCERS = 4  # Number of producer threads
NUM_CONSUMERS = 5  # Number of consumer threads
NUM_ITEMS_TO_PRODUCE = 10  # Total items to be produced
DELAY = 0.1

def producerWorker(queue: queue.Queue):
    """
    Worker function for producer threads.
    Produces items and adds them to the queue.
    """
    for _ in range(NUM_ITEMS_TO_PRODUCE):
        item = random.randint(1, 100)  # Produce a random item
        queue.put(item)  # Add the item to the queue
        print(f"{threading.current_thread().name} produced: {item}")
        time.sleep(DELAY)

def consumerWorker(queue: queue.Queue):
    """
    Worker function for consumer threads.
    Consumes items from the queue.
    """
    while True:
        try:
            item = queue.get()
            print(f"{threading.current_thread().name} consumed: {item}")
            time.sleep(DELAY) 
            queue.task_done()
        except queue.Empty:
            # Exit if queue is empty and all producers are done
            break

if __name__ == "__main__":
    buffer = queue.Queue()  # Shared buffer for producers and consumers

    # Create and start producer threads
    producer_threads = [threading.Thread(target=producerWorker, args=(buffer,), name=f"Producer-{i+1}") for i in range(NUM_PRODUCERS)]
    for producer in producer_threads:
        producer.start()

    # Create and start consumer threads
    consumer_threads = [threading.Thread(target=consumerWorker, args=(buffer,), name=f"Consumer-{i+1}", daemon=True) for i in range(NUM_CONSUMERS)]
    for consumer in consumer_threads:
        consumer.start()

    # Wait for all producers to finish
    for producer in producer_threads:
        producer.join()

    # Wait for all items in the buffer to be consumed
    buffer.join()

    print("All items have been produced and consumed.")
