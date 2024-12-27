import random
import threading
import time
from datetime import datetime


class Request:
    """
    Represents a request with an ID, priority, and timestamp.
    """

    def __init__(self, id, priority):
        self.id = id
        self.priority = priority
        self.timestamp_received = datetime.now()

    def add_request(self, queue):
        """
        Adds this request to the provided queue.
        """
        queue.add_request(self)

    def __repr__(self):
        return (
            f"Request(id={self.id}, priority={self.priority}, "
            f"received={self.timestamp_received.strftime('%Y-%m-%d %H:%M:%S')})"
        )


class RequestQueue:
    """
    Thread-safe priority queue for managing requests.
    Higher priority requests are processed first. If priorities are equal,
    the request that was received earlier is processed first.
    Implemented using a manually sorted list.
    """

    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()

    def add_request(self, request):
        with self.lock:
            index = self._find_insertion_index(request)
            self.queue.insert(index, request)

    def _find_insertion_index(self, request):
        """
        Finds the index at which the request should be inserted to keep the queue sorted.
        Higher priority first. If priority is equal, earlier timestamp first.
        """
        low = 0
        high = len(self.queue)
        while low < high:
            mid = (low + high) // 2
            current = self.queue[mid]
            if request.priority > current.priority:
                high = mid
            elif request.priority < current.priority:
                low = mid + 1
            else:
                if request.timestamp_received < current.timestamp_received:
                    high = mid
                else:
                    low = mid + 1
        return low

    def pop_request(self):
        with self.lock:
            if self.queue:
                request = self.queue.pop(0)
                return request
            else:
                return None

    def is_empty(self):
        with self.lock:
            return len(self.queue) == 0


class Provider(threading.Thread):
    """
    Represents a provider that processes requests at a specified rate limit.
    """

    def __init__(self, name, rate_limit, queue):
        super().__init__()
        self.name = name
        self.rate_limit = rate_limit  # Requests per second
        self.time_between_requests = 1 / rate_limit if rate_limit > 0 else 0
        self.queue = queue
        self.daemon = True  # Daemonize thread to exit when main program exits

    def run(self):
        while True:
            request = self.queue.pop_request()
            if request:
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {self.name} processing "
                    f"Request(id={request.id}, priority={request.priority})"
                )
                # Simulate processing time based on rate limit
                time.sleep(self.time_between_requests)
            else:
                # If queue is empty, wait before trying again
                time.sleep(1)


def main():
    """
    Main function to simulate the outgoing request rate limiter.
    """
    # Initialize the request queue
    request_queue = RequestQueue()

    # Explain to the user how the program works
    print("Welcome to the Request Rate Limiter Simulation!")
    print("You will specify the number of providers and their respective rate limits.")
    print("Rate limit is the number of requests a provider can process per second.")
    print("For example:")
    print(
        "  - A rate limit of 0.2 means the provider processes 1 request every 5 seconds."
    )
    print("  - A rate limit of 1 means the provider processes 1 request per second.")

    # Get the number of providers from the user
    num_providers = int(input("Enter the number of providers: "))

    # Initialize providers with their respective rate limits
    providers = []
    for i in range(num_providers):
        name = f"P{i+1}"
        rate_limit = float(
            input(f"Enter rate limit (requests per second) for {name}: ")
        )
        if rate_limit <= 0:
            print(
                "Rate limit must be greater than 0. Setting default rate limit to 0.1 (1 request every 10 seconds)."
            )
            rate_limit = 0.1

        providers.append(
            Provider(name=name, rate_limit=rate_limit, queue=request_queue)
        )

    # Get the number of requests from the user
    max_requests = int(input("Enter the number of requests to generate: "))

    # Start provider threads
    for provider in providers:
        provider.start()

    # Generate all requests
    request_id = 1
    try:
        while request_id <= max_requests:
            # Generate a request
            priority = random.randint(1, 3)  # Priority between 1 and 3
            request = Request(id=request_id, priority=priority)
            request.add_request(request_queue)
            request_id += 1

        # Wait based on the number of requests
        time.sleep(max_requests * 0.1)  # Adjust sleep time as needed

    except KeyboardInterrupt:
        print("\nSimulation stopped.")


if __name__ == "__main__":
    main()
