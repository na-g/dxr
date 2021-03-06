from textwrap import dedent

from dxr.plugins.python.tests import PythonSingleFileTestCase


class CallersTests(PythonSingleFileTestCase):
    source = dedent("""
    def call_once():
        called_once()

    def call_multiple():
        called_multiple()
        called_multiple()

    def call_in_separate_functions_1():
        called_in_separate_functions()

    def call_in_separate_functions_2():
        called_in_separate_functions()

    def outer_call_bar():
        def inner_call_foo():
            foo()
        bar()

    outer_call_bar()
    """)

    def test_called_once(self):
        self.found_line_eq('callers:called_once', '<b>called_once()</b>', 3)

    def test_called_multiple_times(self):
        self.found_lines_eq('callers:called_multiple', [
            ('<b>called_multiple()</b>', 6),
            ('<b>called_multiple()</b>', 7),
        ])

    def test_called_in_several_functions(self):
        self.found_lines_eq('callers:called_in_separate_functions', [
            ('<b>called_in_separate_functions()</b>', 10),
            ('<b>called_in_separate_functions()</b>', 13),
        ])

    def test_called_in_inner_function(self):
        """Make sure a call within an inner function matches the inner
        function only.

        """
        self.found_line_eq('callers:foo', '<b>foo()</b>', 17)

    def test_called_in_outer_function(self):
        """Make sure inner function definitions do not affect other
        calls in the outer function.

        """
        self.found_line_eq('callers:bar', '<b>bar()</b>', 18)

    def test_called_outside_of_function(self):
        """Make sure calls that take place at the top level in a module are
        still recorded.

        """
        self.found_line_eq('callers:outer_call_bar', '<b>outer_call_bar()</b>', 20)


class CallersMethodTests(PythonSingleFileTestCase):
    source = dedent("""
    class Foo(object):
        @classmethod
        def class_method(cls):
            pass

        def method(self):
            pass

    Foo.class_method()

    foo = Foo()
    foo.method()
    """)

    def test_class_method_called(self):
        self.found_nothing('callers:class_method')

    def test_method_called(self):
        self.found_nothing('callers:method')
