#cython: language_level=3

from obitools3.uri.decode import open_uri
from obitools3.apps.config import logger
from obitools3.dms import DMS
from obitools3.apps.optiongroups import addMinimalInputOption, addMinimalOutputOption, addTaxonomyOption
from obitools3.dms.view.view cimport View
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
 
__title__="Build genome size db"


def addOptions(parser):    
    addMinimalInputOption(parser)
    addTaxonomyOption(parser)
    addMinimalOutputOption(parser)

    group=parser.add_argument_group("obi _editgenomesizedb specific options")
 
    group.add_argument('-i', '--ignore',
                     action="store", dest="_editgenomesizedb:ignore",
                     metavar="<URI>",
                     default=None,
                     type=int,
                     help="Taxid to ignore when building the database")
 
    group.add_argument('-D', '--genome-size-ref-db',
                     action="store", dest="_editgenomesizedb:db",
                     metavar="<URI>",
                     default=None,
                     type=str,
                     help="URI to the genome size reference database to edit")


def run(config):

    DMS.obi_atexit()
    
    #logger("info", "obi _editgenomesizedb")

    # Open the input
    input = open_uri(config['obi']['inputURI'])
    if input is None:
        raise Exception("Could not read input view")
    i_dms = input[0]
    i_view = input[1]
    i_view_name = input[1].name

    # Open the output: only the DMS, as the output view is going to be created by cloning the input view
    # (could eventually be done via an open_uri() argument)
    output = open_uri(config['obi']['outputURI'],
                      input=False,
                      dms_only=True)
    if output is None:
        raise Exception("Could not create output view")
    o_dms = output[0]
    output_0 = output[0]
    o_view_name = output[1]

    # stdout output: create temporary view
    if type(output_0)==BufferedWriter:
        o_dms = i_dms
        i=0
        o_view_name = b"temp"
        while o_view_name in i_dms: # Making sure view name is unique in output DMS
            o_view_name = o_view_name+b"_"+str2bytes(str(i))
            i+=1
        imported_view_name = o_view_name

    # Open the db
    if "db" in config["_editgenomesizedb"]:
        dbi = open_uri(config["_editgenomesizedb"]["db"])
        if dbi is None:
            raise Exception("Could not open genome size reference database")
        db_dms = dbi[0]
        db = dbi[1]
        db_name = db.name
    else:
        raise Exception("No genome size reference database provided")

    # If the db and output DMS are not the same, import the db view in the output DMS before cloning it to modify it
    # (could be the other way around: clone and modify in the db DMS then import the new view in the output DMS)
    if db_dms != o_dms:
        imported_view_name = db_name
        i=0
        while imported_view_name in o_dms:  # Making sure view name is unique in output DMS
            imported_view_name = db_name+b"_"+str2bytes(str(i))
            i+=1
        View.import_view(db_dms.full_path[:-7], o_dms.full_path[:-7], db_name, imported_view_name)
        db = o_dms[imported_view_name]

    # Clone output view from db
    o_view = db.clone(o_view_name)
    if o_view is None:
        raise Exception("Couldn't create output view")
    db.close()

#    for col in o_view.keys():
#        print(col)
    
    taxo_uri = open_uri(config['obi']['taxoURI'])
    if taxo_uri is None or taxo_uri[2] == bytes:
        raise RollbackException("Couldn't open taxonomy, rollbacking view", o_view)
    taxo = taxo_uri[1]

    # to ignore
    ignore = config["_editgenomesizedb"]["ignore"]

    # Build db with columns:
    # At index=taxid, GENOME_COUNT (int), GENOME_SIZE (float tuple)
    
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
    taxid_col = "TAXID"

    # Create columns
    Column.new_column(o_view,
                      genome_size_col,
                      OBI_FLOAT,
                      tuples=True)

    # Renitialize columns
    for taxon in taxo:
        taxid = taxon.taxid
        o_view[taxid][infonode_col] = False
        o_view[taxid][genome_count_col] = 0
        #o_view[taxid][tax_rank_col] = taxo.get_rank(taxid)
        #o_view[taxid][scientific_name_col] = taxo.get_scientific_name(taxid)
        o_view[taxid][density_col] = 0.0
        #o_view[taxid][taxid_col] = taxid
        o_view[taxid][genome_size_col] = None
        o_view[taxid][mean_size_col] = None
        o_view[taxid][median_size_col] = None
        o_view[taxid][var_col] = None
        o_view[taxid][sd_col]= None

    #logger("info", "Initialized columns")

    # Compute and store info about the nodes with assembly info
    
    genome_dict = {}
    for genome in i_view:
        # Get taxid
        taxid = genome[TAXID_COLUMN]
        if taxid != ignore and not taxo.is_ancestor(ignore, taxid):
            genome_size = genome[genome_ungapped_length_col]
            # Store the info for that taxid
            if taxid not in genome_dict:
                genome_dict[taxid] = [genome_size]
            else:
                genome_dict[taxid].append(genome_size)
        
    for taxid in genome_dict:
        o_view[taxid][infonode_col] = True
        if taxo.get_rank(taxid) != b"species": # computed later if species
            o_view[taxid][genome_size_col] = tuple(genome_dict[taxid])
            o_view[taxid][genome_count_col] = len(genome_dict[taxid])
            o_view[taxid][mean_size_col] = statistics.mean(genome_dict[taxid])
            o_view[taxid][median_size_col] = statistics.median(genome_dict[taxid])
            if len(genome_dict[taxid]) >= 2 :
                o_view[taxid][var_col] = statistics.variance(genome_dict[taxid])
                o_view[taxid][sd_col] = statistics.stdev(genome_dict[taxid])
    
    #logger("info", "Computed assembly statistics at nodes with assemblies")
    
    # Then compute for each node:
    # from the leaves of each node, mean median CI var sd emptiness(%of children leaves with a GSR)
    
    # Propagate infos up the taxonomic tree
    # propagate info to species level and store in dict
    sp_genome_dict = {}
    # for each info node :
    for taxid in genome_dict :
        # propagate to species level:
        # for ancestor:
        for ancestor in taxo.parental_tree_iterator(taxid):
            # if ancestor rank is species:
            if taxo.get_rank(ancestor.taxid) == b"species":
                # store (add) genome size in sp_genome_dict at ancestor
                sp_taxid = ancestor.taxid
                if sp_taxid not in sp_genome_dict:
                    sp_genome_dict[sp_taxid] = genome_dict[taxid]
                else:
                    sp_genome_dict[sp_taxid].extend(genome_dict[taxid])
    
    # propagate to all ancestor nodes, and compute/store info at species and all ancestor nodes
    anc_genome_dict = {}
    # for species in sp_genome_dict :
    for species in sp_genome_dict:
        # compute and store tuple, mean, genome_count, median, var, sd
        o_view[species][genome_size_col] = tuple(sp_genome_dict[species])
        o_view[species][genome_count_col] = len(sp_genome_dict[species])
        o_view[species][mean_size_col] = statistics.mean(sp_genome_dict[species])
        o_view[species][median_size_col] = statistics.median(sp_genome_dict[species])
        if len(sp_genome_dict[species]) >= 2 :
            o_view[species][var_col] = statistics.variance(sp_genome_dict[species])
            o_view[species][sd_col] = statistics.stdev(sp_genome_dict[species])
        # Propagate up to the top
        # for ancestor:
        itself = True
        for ancestor in taxo.parental_tree_iterator(species):
            if not itself: # first parent yielded is itself
                # store (add) genome size in anc_genome_dict at ancestor
                ataxid = ancestor.taxid
                if ataxid not in anc_genome_dict:
                    anc_genome_dict[ataxid] = [o_view[species][mean_size_col]]
                else:
                    anc_genome_dict[ataxid].append(o_view[species][mean_size_col])
            else:
                itself = False

    #logger("info", "Propagated assembly metadata up to all nodes")

    # for ancestor in anc_genome_dict:
    for ancestor in anc_genome_dict:
        # compute and store tuple, mean, genome_count_at_species_level, median, var, sd
        o_view[ancestor][genome_size_col] = tuple(anc_genome_dict[ancestor]) # boom if exists?
        o_view[ancestor][genome_count_col] = len(anc_genome_dict[ancestor])
        o_view[ancestor][mean_size_col] = statistics.mean(anc_genome_dict[ancestor])
        o_view[ancestor][median_size_col] = statistics.median(anc_genome_dict[ancestor])
        if len(anc_genome_dict[ancestor]) >= 2 :
            o_view[ancestor][var_col] = statistics.variance(anc_genome_dict[ancestor])
            o_view[ancestor][sd_col] = statistics.stdev(anc_genome_dict[ancestor])

    #logger("info", "Computed assembly statistics for all nodes")

    # Compute density
    for taxon in taxo:
        taxid = taxon.taxid
        if o_view[taxid][species_count_col] > 0:
            o_view[taxid][density_col] = o_view[taxid][genome_count_col] / o_view[taxid][species_count_col]

    #logger("info", "Computed density for all nodes")   
    
    # Save command config in View and DMS comments
    command_line = " ".join(sys.argv[1:])
    input_dms_name=[input[0].name]
    input_view_name=[input[1].name]
    if 'taxoURI' in config['obi'] and config['obi']['taxoURI'] is not None:
        input_dms_name.append(config['obi']['taxoURI'].split("/")[-3])
        input_view_name.append("taxonomy/"+config['obi']['taxoURI'].split("/")[-1])
    o_view.write_config(config, "_editgenomesizedb", command_line, input_dms_name=input_dms_name, input_view_name=input_view_name)
    o_dms.record_command_line(command_line)

    # stdout output: write to buffer
    if type(output_0)==BufferedWriter:
        logger("info", "Printing to output...")
        o_view.print_to_output(output_0, noprogressbar=config['obi']['noprogressbar'])
        o_view.close()

    #print("\n\nOutput view:\n````````````", file=sys.stderr)
    #print(repr(o_view), file=sys.stderr)

    # If stdout output, delete the temporary result view in the input DMS
    if type(output_0)==BufferedWriter:
        View.delete_view(i_dms, o_view_name)

    i_dms.close(force=True)
    o_dms.close(force=True)

    #logger("info", "Done.")
