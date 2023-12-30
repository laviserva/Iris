import os

def handle_exception():
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                if os.path.exists("logs/algorithm_performance.txt"):
                    os.remove("logs/algorithm_performance.txt")
                return 
            except Exception as e:
                if os.path.exists("logs/algorithm_performance.txt"):
                    os.remove("logs/algorithm_performance.txt")
                raise e
        return wrapper
    return decorator