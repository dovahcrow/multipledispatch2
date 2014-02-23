from multipledispatch import dispatch
from multipledispatch.compatibility import raises
from pytest import xfail


def test_singledispatch():
    @dispatch(int)
    def f(x):
        return x + 1

    @dispatch(int)
    def g(x):
        return x + 2

    @dispatch(float)
    def f(x):
        return x - 1

    assert f(1) == 2
    assert g(1) == 3
    assert f(1.0) == 0

    assert raises(NotImplementedError, lambda: f('hello'))


def test_multipledispatch():
    @dispatch(int, int)
    def f(x, y):
        return x + y

    @dispatch(float, float)
    def f(x, y):
        return x - y

    assert f(1, 2) == 3
    assert f(1.0, 2.0) == -1.0


class A(object): pass
class B(object): pass
class C(A): pass
class D(C): pass
class E(C): pass


def test_inheritance():
    @dispatch(A)
    def f(x):
        return 'a'

    @dispatch(B)
    def f(x):
        return 'b'

    assert f(A()) == 'a'
    assert f(B()) == 'b'
    assert f(C()) == 'a'


def test_inheritance_and_multiple_dispatch():
    @dispatch(A, A)
    def f(x, y):
        return type(x), type(y)

    @dispatch(A, B)
    def f(x, y):
        return 0

    assert f(A(), A()) == (A, A)
    assert f(A(), C()) == (A, C)
    assert f(A(), B()) == 0
    assert f(C(), B()) == 0
    assert raises(NotImplementedError, lambda: f(B(), B()))


def test_competing_solutions():
    @dispatch(A)
    def h(x):
        return 1

    @dispatch(C)
    def h(x):
        return 2

    assert h(D()) == 2


def test_competing_multiple():
    @dispatch(A, B)
    def h(x, y):
        return 1

    @dispatch(C, B)
    def h(x, y):
        return 2

    assert h(D(), B()) == 2


def test_competing_ambiguous():
    @dispatch(A, C)
    def f(x, y):
        return 2

    @dispatch(C, A)
    def f(x, y):
        return 2

    assert f(A(), C()) == f(C(), A()) == 2
    # assert raises(Warning, lambda : f(C(), C()))


def test_caching_correct_behavior():
    @dispatch(A)
    def f(x):
        return 1

    assert f(C()) == 1

    @dispatch(C)
    def f(x):
        return 2

    assert f(C()) == 2


"""
Fails
def test_methods():
    class Foo(object):
        @dispatch(int)
        def f(self, x):
            return x + 1

        @dispatch(float)
        def f(self, x):
            return x - 1

    F = Foo()
    assert F.f(1) == 2
    assert F.f(1.0) == 0.0
"""
