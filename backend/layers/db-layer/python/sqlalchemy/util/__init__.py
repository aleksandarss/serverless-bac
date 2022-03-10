# util/__init__.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


from collections import defaultdict  # noqa
from contextlib import contextmanager  # noqa
from functools import partial  # noqa
from functools import update_wrapper  # noqa

from ._collections import coerce_generator_arg  # noqa
from ._collections import collections_abc  # noqa
from ._collections import column_dict  # noqa
from ._collections import column_set  # noqa
from ._collections import EMPTY_SET  # noqa
from ._collections import flatten_iterator  # noqa
from ._collections import has_dupes  # noqa
from ._collections import has_intersection  # noqa
from ._collections import IdentitySet  # noqa
from ._collections import ImmutableContainer  # noqa
from ._collections import immutabledict  # noqa
from ._collections import ImmutableProperties  # noqa
from ._collections import KeyedTuple  # noqa
from ._collections import lightweight_named_tuple  # noqa
from ._collections import LRUCache  # noqa
from ._collections import ordered_column_set  # noqa
from ._collections import OrderedDict  # noqa
from ._collections import OrderedIdentitySet  # noqa
from ._collections import OrderedProperties  # noqa
from ._collections import OrderedSet  # noqa
from ._collections import PopulateDict  # noqa
from ._collections import Properties  # noqa
from ._collections import ScopedRegistry  # noqa
from ._collections import ThreadLocalRegistry  # noqa
from ._collections import to_column_set  # noqa
from ._collections import to_list  # noqa
from ._collections import to_set  # noqa
from ._collections import unique_list  # noqa
from ._collections import UniqueAppender  # noqa
from ._collections import update_copy  # noqa
from ._collections import WeakPopulateDict  # noqa
from ._collections import WeakSequence  # noqa
from .compat import b  # noqa
from .compat import b64decode  # noqa
from .compat import b64encode  # noqa
from .compat import binary_type  # noqa
from .compat import byte_buffer  # noqa
from .compat import callable  # noqa
from .compat import cmp  # noqa
from .compat import cpython  # noqa
from .compat import decode_backslashreplace  # noqa
from .compat import dottedgetter  # noqa
from .compat import inspect_getfullargspec  # noqa
from .compat import int_types  # noqa
from .compat import iterbytes  # noqa
from .compat import itertools_filter  # noqa
from .compat import itertools_filterfalse  # noqa
from .compat import jython  # noqa
from .compat import namedtuple  # noqa
from .compat import nested  # noqa
from .compat import next  # noqa
from .compat import parse_qsl  # noqa
from .compat import pickle  # noqa
from .compat import print_  # noqa
from .compat import py2k  # noqa
from .compat import py33  # noqa
from .compat import py36  # noqa
from .compat import py3k  # noqa
from .compat import pypy  # noqa
from .compat import quote_plus  # noqa
from .compat import raise_from_cause  # noqa
from .compat import reduce  # noqa
from .compat import reraise  # noqa
from .compat import safe_kwarg  # noqa
from .compat import string_types  # noqa
from .compat import StringIO  # noqa
from .compat import text_type  # noqa
from .compat import threading  # noqa
from .compat import timezone  # noqa
from .compat import u  # noqa
from .compat import ue  # noqa
from .compat import unquote  # noqa
from .compat import unquote_plus  # noqa
from .compat import win32  # noqa
from .compat import with_metaclass  # noqa
from .compat import zip_longest  # noqa
from .deprecations import deprecated  # noqa
from .deprecations import deprecated_cls  # noqa
from .deprecations import deprecated_params  # noqa
from .deprecations import inject_docstring_text  # noqa
from .deprecations import pending_deprecation  # noqa
from .deprecations import warn_deprecated  # noqa
from .deprecations import warn_pending_deprecation  # noqa
from .langhelpers import add_parameter_text  # noqa
from .langhelpers import as_interface  # noqa
from .langhelpers import asbool  # noqa
from .langhelpers import asint  # noqa
from .langhelpers import assert_arg_type  # noqa
from .langhelpers import attrsetter  # noqa
from .langhelpers import bool_or_str  # noqa
from .langhelpers import chop_traceback  # noqa
from .langhelpers import class_hierarchy  # noqa
from .langhelpers import classproperty  # noqa
from .langhelpers import clsname_as_plain_name  # noqa
from .langhelpers import coerce_kw_type  # noqa
from .langhelpers import constructor_copy  # noqa
from .langhelpers import counter  # noqa
from .langhelpers import decode_slice  # noqa
from .langhelpers import decorator  # noqa
from .langhelpers import dependencies  # noqa
from .langhelpers import dictlike_iteritems  # noqa
from .langhelpers import duck_type_collection  # noqa
from .langhelpers import ellipses_string  # noqa
from .langhelpers import EnsureKWArgType  # noqa
from .langhelpers import format_argspec_init  # noqa
from .langhelpers import format_argspec_plus  # noqa
from .langhelpers import generic_repr  # noqa
from .langhelpers import get_callable_argspec  # noqa
from .langhelpers import get_cls_kwargs  # noqa
from .langhelpers import get_func_kwargs  # noqa
from .langhelpers import getargspec_init  # noqa
from .langhelpers import group_expirable_memoized_property  # noqa
from .langhelpers import hybridmethod  # noqa
from .langhelpers import hybridproperty  # noqa
from .langhelpers import iterate_attributes  # noqa
from .langhelpers import map_bits  # noqa
from .langhelpers import md5_hex  # noqa
from .langhelpers import memoized_instancemethod  # noqa
from .langhelpers import memoized_property  # noqa
from .langhelpers import MemoizedSlots  # noqa
from .langhelpers import methods_equivalent  # noqa
from .langhelpers import monkeypatch_proxied_specials  # noqa
from .langhelpers import NoneType  # noqa
from .langhelpers import only_once  # noqa
from .langhelpers import PluginLoader  # noqa
from .langhelpers import portable_instancemethod  # noqa
from .langhelpers import quoted_token_parser  # noqa
from .langhelpers import safe_reraise  # noqa
from .langhelpers import set_creation_order  # noqa
from .langhelpers import symbol  # noqa
from .langhelpers import unbound_method_to_callable  # noqa
from .langhelpers import warn  # noqa
from .langhelpers import warn_exception  # noqa
from .langhelpers import warn_limited  # noqa
from .langhelpers import wrap_callable  # noqa


# things that used to be not always available,
# but are now as of current support Python versions
