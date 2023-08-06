#cython: language_level=3

from obitools3.apps.progress cimport ProgressBar  # @UnresolvedImport
from obitools3.uri.decode import open_uri
from obitools3.apps.config import logger
from obitools3.dms import DMS
from obitools3.apps.optiongroups import addMinimalInputOption, addMinimalOutputOption, addNoProgressBarOption, addTaxonomyOption
from obitools3.dms.view.view cimport View, Line_selection
from obitools3.dms.view.typed_view.view_NUC_SEQS cimport View_NUC_SEQS
from obitools3.dms.taxo.taxo cimport Taxonomy
from obitools3.dms.column.column cimport Column
from obitools3.dms.capi.obiview cimport QUALITY_COLUMN, COUNT_COLUMN, NUC_SEQUENCE_COLUMN, ID_COLUMN, TAXID_COLUMN
from obitools3.dms.capi.obitypes cimport OBI_FLOAT, OBI_INT
from obitools3.utils cimport tobytes, tostr, str2bytes
from obitools3.dms.view import RollbackException

import statistics
import sys
from cpython.exc cimport PyErr_CheckSignals
from io import BufferedWriter

import os
 
__title__="Sample for genome size db"


def addOptions(parser):    
    addMinimalInputOption(parser)
    addMinimalOutputOption(parser)
    addTaxonomyOption(parser)
    addNoProgressBarOption(parser)

    group=parser.add_argument_group("obi _sampleforgenomesizedb specific options")
 
    group.add_argument('-D', '--genome-size-ref-db',
                     action="store", dest="_sampleforgenomesizedb:db",
                     metavar="<URI>",
                     default=None,
                     type=str,
                     help="URI to the genome size reference database")
 

def run(config):

    DMS.obi_atexit()
    
    logger("info", "obi _sampleforgenomesizedb")

    # Open the input
    input = open_uri(config["obi"]["inputURI"])
    if input is None:
        raise Exception("Could not read input view")
    i_dms = input[0]
    i_view = input[1]

    # Open the output: only the DMS
    output = open_uri(config['obi']['outputURI'],
                      input=False,
                      dms_only=True)
    if output is None:
        raise Exception("Could not create output view")
    o_dms = output[0]
    output_0 = output[0]
    final_o_view_name = output[1]

    # If stdout output or the input and output DMS are not the same, create a temporary view that will be exported and deleted afterwards.
    if i_dms != o_dms or type(output_0)==BufferedWriter:
        temporary_view_name = b"temp"
        i=0
        while temporary_view_name in i_dms:  # Making sure view name is unique in input DMS
            temporary_view_name = temporary_view_name+b"_"+str2bytes(str(i))
            i+=1
        o_view_name = temporary_view_name
        if type(output_0)==BufferedWriter:
            o_dms = i_dms
    else:
        o_view_name = final_o_view_name

    if 'taxoURI' in config['obi'] and config['obi']['taxoURI'] is not None:
        taxo_uri = open_uri(config["obi"]["taxoURI"])
        if taxo_uri is None or taxo_uri[2] == bytes:
            raise Exception("Couldn't open taxonomy")
        taxo = taxo_uri[1]
    else :
        taxo = None

    # Open the db
    if "db" in config["_sampleforgenomesizedb"]:
        dbi = open_uri(config["_sampleforgenomesizedb"]["db"])
        if dbi is None:
            raise Exception("Could not open genome size reference database")
        db_dms = dbi[0]
        db = dbi[1]
        db_name = db.name
    else:
        raise Exception("No genome size reference database provided")

    # Initialize the progress bar
    if config['obi']['noprogressbar'] == False:
        pb = ProgressBar(len(i_view), config)
    else:
        pb = None
    
    genome_count_col = "GENOME_COUNT"
    genome_size_col = "GENOME_SIZE"
    genome_ungapped_length_col = "GENOME_UNGAPPED_LENGTH"
    density_col = "GENOME_DATA_DENSITY"
    mean_size_col = "MEAN_GENOME_SIZE"
    median_size_col = "MEDIAN_GENOME_SIZE"
    var_col = "VARIANCE_GENOME_SIZE"    
    sd_col = "STANDARD_DEVIATION_GENOME_SIZE"
    infonode_col = "INFO_NODE"
    tax_rank_col = "TAXONOMIC_RANK"
    species_count_col = "SPECIES_COUNT"
    scientific_name_col = "SCIENTIFIC_NAME"
    taxid_col = "TAXID" # TRUE_TAXID

    selection = Line_selection(i_view)
    sample = []
    
    for i in range(len(i_view)):
        PyErr_CheckSignals()
        if pb is not None:
            pb(i)
        taxid = i_view[taxid_col][i]
        #fam = taxo.get_taxon_at_rank(taxid, b'family')
        #s = taxo.get_taxon_at_rank(taxid, b'species')
        #s = taxid
        id = i_view[i].id
        s = id
        #if db[taxid][mean_size_col] is not None: # TODO save col for efficiency
#        if db[taxid][genome_size_col] is not None and s not in sample:
        if db[taxid]['INFO_NODE'] is not None and s not in sample:
            selection.append(i)
            sample.append(s)
            print(tostr(id), taxid)
            #v_name = b'sample_'+id
            #n=0
            #while v_name in o_dms:
            #    n+=1
            #    v_name = b'sample_'+id+tobytes(str(n))
            #v = View_NUC_SEQS.new(o_dms, v_name)
            #v[0] = i_view[i]
            #v.close()
    
    # Create output view with the line selection
    try:
        o_view = selection.materialize(o_view_name)
    except Exception, e:
        raise RollbackException("obi _sampleforgenomesizedb error, rollbacking view: "+str(e), o_view)

    # Save command config in View and DMS comments
    command_line = " ".join(sys.argv[1:])
    input_dms_name=[input[0].name]
    input_view_name=[input[1].name]
    if 'taxoURI' in config['obi'] and config['obi']['taxoURI'] is not None:
        input_dms_name.append(config['obi']['taxoURI'].split("/")[-3])
        input_view_name.append("taxonomy/"+config['obi']['taxoURI'].split("/")[-1])
    o_view.write_config(config, "_sampleforgenomesizedb", command_line, input_dms_name=input_dms_name, input_view_name=input_view_name)
    o_dms.record_command_line(command_line)

    # If input and output DMS are not the same, export the temporary view to the output DMS
    # and delete the temporary view in the input DMS
    if i_dms != o_dms:
        o_view.close()
        View.import_view(i_dms.full_path[:-7], o_dms.full_path[:-7], o_view_name, final_o_view_name)
        o_view = o_dms[final_o_view_name]
    
    # stdout output: write to buffer
    if type(output_0)==BufferedWriter:
        logger("info", "Printing to output...")
        o_view.print_to_output(output_0, noprogressbar=config['obi']['noprogressbar'])
        o_view.close()

    #print("\n\nOutput view:\n````````````", file=sys.stderr)
    #print(repr(o_view), file=sys.stderr)

    # If the input and the output DMS are different or if stdout output, delete the temporary imported view used to create the final view
    if i_dms != o_dms or type(output_0)==BufferedWriter:
        View.delete_view(i_dms, o_view_name)
        o_dms.close(force=True)
    i_dms.close(force=True)

    logger("info", "Done.")
