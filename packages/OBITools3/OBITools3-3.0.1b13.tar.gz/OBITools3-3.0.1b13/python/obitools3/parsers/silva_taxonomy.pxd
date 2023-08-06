#cython: language_level=3

from ..files.universalopener cimport uopen


cpdef dict read_silva_tax_ref_file(str path_to_ref)