literate-dataclasses
====================

This is a work-in-progress library to add documentation functionality to ``dataclasses`` introduced in Python 3.7.
The library can be used as a drop-in replacement for the standard ``dataclasses`` and can be installed from PyPI_.

.. code:: bash

    $ pip install literate_dataclasses


Literate dataclasses modify their own class docstrings and add attribute docs in [Google code style](https://google.github.io/styleguide/pyguide.html)
with the goal of removing redundant code. The docs can be written as follows:

.. code:: python 

    from literate_dataclasses import dataclass, field

    @dataclass(test_arg = "hello")
    class Test:
        """My dataclass
        
        Some comment.
        
        Args:
            See dataclass signature.
        """
        
        x: int = field(default = 42, doc = \
        """Some value x."""
        )
        
        y: int = field(default = 72, doc = \
        """Some value x."""
        )
            
        name: int = field(default = 'foo', doc = \
        """The object name.""",
        )
            
    test = Test(x = 5, y = 3)
    help(Test)

which will generate the output

.. code:: 

    Help on class Test in module __main__:

    class Test(builtins.object)
    |  Test(x: int = 42, y: int = 72, name: int = 'foo') -> None
    |  
    |  My dataclass
    |  
    |  Some comment.
    |  
    |  Args:
    |      x: Some value x.
    |      y: Some value x.
    |      name: The object name.

.. _PyPI: https://pypi.org/stes/literate_dataclasses/
