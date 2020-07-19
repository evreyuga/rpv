from multiprocessing import Pool, current_process, Process
from time import sleep


def sleeper(time):
    print(current_process().name, f"wait for {time} seconds")
    sleep(time)
    print(current_process().name, f"has done")
    return str(f"Wait for {time} seconds")


def finish_callback(arg):
    print("Finish subprocess in", current_process().name, "with", arg)


if __name__ == "__main__":
    print("This process name is", current_process().name)
    pool = Pool(1)
    result = pool.apply_async(sleeper, (1,), callback=finish_callback)
    sleep(0.5)
    pool.terminate()
    print(result.ready())
    pool = Pool(1)
    result = pool.apply_async(sleeper, (1,), callback=finish_callback)
    result.wait()
    pool = Pool(1)
    pool.terminate()
