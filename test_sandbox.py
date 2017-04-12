# -*- coding: utf-8 -*-

import pytest
from expecter import expect

from sandbox import get_key


def describe_get_key():

    def with_nominal_filename():
        expect(get_key("foobar.dat", 42)) == "96527871-42"

    def with_non_ascii_filename():
        expect(get_key("values_of_π.dat", 42)) == "2336675477-42"

