#cython: language_level=3

from obitools3.apps.progress cimport ProgressBar  # @UnresolvedImport
from obitools3.dms import DMS
from obitools3.dms.view.view cimport View
from obitools3.uri.decode import open_uri
from obitools3.apps.optiongroups import addMinimalInputOption, addTaxonomyOption, addNoProgressBarOption
from obitools3.dms.view import RollbackException
from obitools3.dms.column.column cimport Column
from functools import reduce
from obitools3.apps.config import logger
from obitools3.utils cimport tobytes, str2bytes, tostr
from io import BufferedWriter
from obitools3.dms.capi.obiview cimport TAXID_COLUMN
import time
import math 
import sys

from cpython.exc cimport PyErr_CheckSignals

 
__title__="Compute primer coverage"


 
def addOptions(parser):
    
    addMinimalInputOption(parser)
    addTaxonomyOption(parser)
    addNoProgressBarOption(parser)

    group=parser.add_argument_group('obi primercoverage specific options')

    group.add_argument('-R', '--ref-db',
                     action="store", dest="primercoverage:db",
                     metavar="<URI>",
                     default=None,
                     type=str,
                     help="URI to the entire reference database")

    group.add_argument('-a', '--restricting-ancestor', 
                       action="append",
                       type=int, 
                       dest="primercoverage:restricting_ancestors",
                       metavar="<RESTRICTING_ANCESTOR>",
                       default=[],
                       help="Enables to restrict under ancestors specified by their taxid.")


def run(config):
     
    DMS.obi_atexit()
    
    logger("info", "obi primercoverage")

    # Open the input
    input = open_uri(config['obi']['inputURI'])
    if input is None:
        raise Exception("Could not read input view")
    i_dms = input[0]
    i_view = input[1]
    i_view_name = input[1].name

    # Open the reference db
    input_refdb = open_uri(config['primercoverage']['db'])
    if input_refdb is None:
        raise Exception("Could not read reference db")
    refdb_dms = input_refdb[0]
    refdb_view = input_refdb[1]
    refdb_view_name = input_refdb[1].name

    # Open taxonomy
    taxo_uri = open_uri(config['obi']['taxoURI'])
    if taxo_uri is None or taxo_uri[2] == bytes:
        raise Exception("Couldn't open taxonomy")
    taxo = taxo_uri[1]
        
    try:

        ranks = [tostr(rank) for rank in taxo.ranks]

        taxa_by_rank = {}
        print('oui', file=sys.stderr)
        taxid_col = refdb_view['TAXID']
        print('non', file=sys.stderr)
        
        # Initialize the progress bar
        if config['obi']['noprogressbar'] == False:
            pb = ProgressBar(len(refdb_view), config)
        else:
            pb = None

        for i in range(len(refdb_view)):
            PyErr_CheckSignals()
            if pb is not None:
                pb(i)
 
            taxid = taxid_col[i]
            if taxid is None:
                print('\nWarning: no taxid for:', i, tostr(refdb_view[i].id), '\n')
                continue
            
            if len(config['primercoverage']['restricting_ancestors'])>0 and reduce(lambda x,y: x or y,
                      (taxo.is_ancestor(r, taxid) for r in config['primercoverage']['restricting_ancestors']),
                      False):
                                
                for rank in ranks:
                    if rank != 'no rank':
                        t = taxo.get_taxon_at_rank(taxid, rank)
                        if t is not None:
                            if rank in taxa_by_rank:
                                taxa_by_rank[rank].add(t)
                            else:
                                taxa_by_rank[rank]=set([t])
                        
        stats = dict((x,len(taxa_by_rank[x])) for x in taxa_by_rank)

        if pb is not None:
            pb(i, force=True)
            print("", file=sys.stderr)


        taxa_by_rank = {}
        taxid_col = i_view['TAXID']
                
        # Initialize the progress bar
        if config['obi']['noprogressbar'] == False:
            pb = ProgressBar(len(i_view), config)
        else:
            pb = None

        for i in range(len(i_view)):
            PyErr_CheckSignals()
            if pb is not None:
                pb(i)
 
            taxid = taxid_col[i]
            if taxid is None:
                print('/nWarning: no taxid for:', i, tostr(i_view[i].id), '/n')
                continue
            
            if len(config['primercoverage']['restricting_ancestors'])>0 and reduce(lambda x,y: x or y,
                      (taxo.is_ancestor(r, taxid) for r in config['primercoverage']['restricting_ancestors']),
                      False):
                                
                for rank in ranks:
                    if rank != 'no rank':
                        t = taxo.get_taxon_at_rank(taxid, rank)
                        if t is not None:
                            if rank in taxa_by_rank:
                                taxa_by_rank[rank].add(t)
                            else:
                                taxa_by_rank[rank]=set([t])
        
        if pb is not None:
            pb(i, force=True)
            print("", file=sys.stderr)
               
        dbstats = dict((x,len(taxa_by_rank[x])) for x in taxa_by_rank)
        
        ranks.sort()
        
        print('%-20s\t%10s\t%10s\t%7s' % ('rank','ecopcr','db','percent'))
        
        for r in ranks:
            if r in dbstats and r in stats and dbstats[r]:
                print('%-20s\t%10d\t%10d\t%8.2f' % (r,dbstats[r],stats[r],float(dbstats[r])/stats[r]*100))

    except Exception, e:
        raise Exception("obi primercoverage error")
        
    # Save command config in View and DMS comments
    command_line = " ".join(sys.argv[1:])
    input_dms_name=[input[0].name]
    input_view_name=[i_view_name]
    if 'taxoURI' in config['obi'] and config['obi']['taxoURI'] is not None:
        input_dms_name.append(config['obi']['taxoURI'].split("/")[-3])
        input_view_name.append("taxonomy/"+config['obi']['taxoURI'].split("/")[-1])

    i_dms.close(force=True)

    logger("info", "Done.")
