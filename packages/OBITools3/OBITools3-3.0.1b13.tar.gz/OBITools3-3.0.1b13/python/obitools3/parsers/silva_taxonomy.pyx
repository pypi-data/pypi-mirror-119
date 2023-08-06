#cython: language_level=3

'''
Created on may 28th 2021

@author: cmercier
'''

cpdef dict read_silva_tax_ref_file(str path_to_ref):
    
    cdef dict tax_path_to_taxid
    cdef bytes line
    cdef list elts
    cdef bytes silva_tax
    cdef int ncbi_taxid
    cdef bytes ncbi_rank
    
    tax_path_to_taxid = {}
    
    f = uopen(path_to_ref)
    for line in f:
        elts = line.split(b'\t')
        silva_tax = elts[0][:-1]
        ncbi_taxid = int(elts[1])
        ncbi_rank = elts[2][:-1]
        #print(silva_tax, ncbi_taxid, ncbi_rank)
        tax_path_to_taxid[silva_tax] = ncbi_taxid
    return tax_path_to_taxid