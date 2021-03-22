from multiprocessing import Process,Queue

class Processor(Process):

    def __init__(self):
        Process.__init__(self)

    def run(self):
        print("hello")



if __name__ == "__main__":

    p = Processor()
    p.start()