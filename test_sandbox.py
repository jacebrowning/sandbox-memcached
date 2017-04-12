import pytest
from expecter import expect

from sandbox import main


def describe_main():

    def as_placeholder():
        expect(main()) == None

