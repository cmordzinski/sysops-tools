#!/bin/python3

import time
import toolkit

tk = toolkit.Toolkit()

def test():
    for i in tk.progressbar(list(range(15)), "Computing: "):
        time.sleep(0.1)

test()
