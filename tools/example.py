#!/bin/python3

import time
from modules.utils import progressbar


def test():
    for i in progressbar(list(range(15)), "Computing: "):
        time.sleep(0.1)

test()
