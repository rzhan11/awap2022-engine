import multiprocessing
import time

# Your foo function
def foo(n):
    time.sleep(n)

if __name__ == '__main__':
    # Start foo as a process
    n = 3
    p = multiprocessing.Process(target=foo, name="Foo", args=(n,))
    p.start()

    # Wait 10 seconds for foo
    p.join(4.5)
    # Terminate foo
    if p.is_alive():
        print("foo is running... let's kill it...")
        p.terminate()
        # Cleanup
        p.join()
    else:
        print("all good!")
