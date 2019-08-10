from generator.generate_conditional_sample import generate_sample
from time import sleep
from random import randrange, randint, choice
import names
import string
import threading
import queue

time_a = [
    "Last night, "
]

time_b = [
    " last night"
]

death_primers = [
    """{time_a}{name} was killed{time_b} when""",
    """{time_a}{name} was found dead{time_b}. It is suspected""",
    """{time_a}{name} was murdered{time_b}""",
    """{time_a}{name} suspiciously died{time_b}""",
    """{time_a}{name} suspiciously went missing{time_b}""",
    """{name} was never seen again after{time_b} when""",
    """{time_a}{name} was tragically""",
    """{name}'s death is suspected"""
]

class SampleQueue:
    def __init__(self, buffer_max):
        self.queue = queue.Queue()
        self.buffer_max = buffer_max
        self.length = 150
        self.incoming = [0]
        # futures = [ self.request_new() for i in range(buffer_max) ]
        # self.loop.run_in_executor(asyncio.gather(*futures))
        thread = threading.Thread(target=self.run_gen, args=(buffer_max, self.queue, self.incoming))
        thread.daemon = True
        self.incoming[0] += buffer_max
        thread.start()

    def resize(self, size):
        self.buffer_max = size
        thread = threading.Thread(target=self.run_gen, 
            args=(self.buffer_max - (self.queue.qsize() + self.incoming[0]), self.queue, self.incoming))
        thread.daemon = True
        self.incoming[0] += self.buffer_max - (self.queue.qsize() + self.incoming[0])
        thread.start()


    def pop(self):
        while self.queue.empty() and self.incoming[0] == 0:
            thread = threading.Thread(target=self.run_gen, args=(1, self.queue, self.incoming))
            thread.daemon = True
            self.incoming[0] += 1
            thread.start()

        top = self.queue.get()

        if self.queue.qsize() < self.buffer_max:
            thread = threading.Thread(target=self.run_gen, args=(1, self.queue, self.incoming))
            thread.daemon = True
            self.incoming[0] += 1
            thread.start()

        return top

    def run_gen(self, num, queue, incoming):
        for i in range(num):
            print(i)
            fake_name, primer = get_primer()
            sentence = generate_sample(text=primer, length=self.length)
            queue.put((fake_name, primer, sentence[0].split("<|endoftext|>")[0]))
            incoming[0] -= 1
            

def get_primer():
    sentence = choice(death_primers)
    name = names.get_first_name()
    full_sentence = None

    formats = [tup[1] for tup in string.Formatter().parse(sentence) if tup[1] is not None]
    time_a_insert = ""
    time_b_insert = ""
    if set(["time_a", "time_b"]).issubset(formats):
        flip = randint(0,1)
        if flip == 0:
            time_a_insert = choice(time_a)
        else:
            time_b_insert = choice(time_b)
    elif "time_a" in formats:
            time_a_insert = choice(time_a)
    elif "time_b" in formats:
            time_b_insert = choice(time_b)

    full_sentence = sentence.format(name=name, time_a=time_a_insert, time_b=time_b_insert)

    return name, full_sentence

