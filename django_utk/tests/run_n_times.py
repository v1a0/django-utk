from functools import wraps

__all__ = [
    "run_n_times",
    "run_10_times",
    "run_100_times",
    "run_1k_times",
    "run_10k_times",
    "run_100k_times",
    "run_1m_times",
]


def run_n_times(n: int):
    def repeat_wrapper(method: callable):
        @wraps(method)
        def many_running_method(*args, **kwargs):
            for _ in range(n):
                method(*args, **kwargs)

        return many_running_method

    return repeat_wrapper


run_10_times = run_n_times(10)
run_100_times = run_n_times(100)
run_1k_times = run_n_times(1_000)
run_10k_times = run_n_times(10_000)
run_100k_times = run_n_times(100_000)
run_1m_times = run_n_times(1_000_000)
