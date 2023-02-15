from functools import partial
from typing import Callable


class MyPartial:

    def __init__(self, func, /, *args, **keywords):
        self.func = func
        self.args = args
        self.keywords = keywords

    def __call__(self, /, *args, **keywords):
        keywords = {**self.keywords, **keywords}
        return self.func(*args, *self.args, **keywords)


def _pseudo_decor(fun, argument):
    def ret_fun(*args, **kwargs):
        #do stuff here, for eg.
        print ("decorator arg is %s" % str(argument))
        return fun(*args, **kwargs)
    return ret_fun


ARG = "안녕하세요"
real_decorator = partial(_pseudo_decor, argument=ARG)


@real_decorator
def foo(*args, **kwargs):
    print(*args)
    print({**kwargs})

foo("1", "2", 이름="James", 나이="15")



