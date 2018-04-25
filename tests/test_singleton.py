# coding=utf8

from borax.patterns.singleton import MetaSingleton


class SingletonM(metaclass=MetaSingleton):
    pass


def test_singleton():
    a = SingletonM()
    b = SingletonM()
    assert id(a) == id(b)
