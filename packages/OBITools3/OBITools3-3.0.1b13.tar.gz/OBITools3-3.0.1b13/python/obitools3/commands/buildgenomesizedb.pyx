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
import math
import sys
from cpython.exc cimport PyErr_CheckSignals
from io import BufferedWriter

import os
 
__title__="Build genome size db"


def addOptions(parser):    
    addMinimalInputOption(parser)
    addTaxonomyOption(parser)
    addMinimalOutputOption(parser)


def run(config):

    DMS.obi_atexit()
    
    logger("info", "obi buildgenomesizedb")

    # Open the input
    input = open_uri(config['obi']['inputURI'])
    if input is None:
        raise Exception("Could not read input")
            
    # Check that it's a view
    if isinstance(input[1], View) :
        i_view = input[1]
    else: 
        raise NotImplementedError()

    # Open the output
    output = open_uri(config['obi']['outputURI'],
                      input=False,
                      newviewtype=View)
    if output is None:
        raise Exception("Could not create output view")
    
    i_dms = input[0]
    entries = input[1]
    o_dms = output[0]
    output_0 = output[0]
    
    # If stdout output create a temporary view that will be exported and deleted.
    if type(output_0)==BufferedWriter:
        temporary_view_name = b"temp"
        i=0
        while temporary_view_name in i_dms:  # Making sure view name is unique in input DMS
            temporary_view_name = temporary_view_name+b"_"+str2bytes(str(i))
            i+=1
        o_view_name = temporary_view_name
        o_dms = i_dms
        o_view = View.new(i_dms, o_view_name)
    else:
        o_view = output[1]
    
    taxo_uri = open_uri(config['obi']['taxoURI'])
    if taxo_uri is None or taxo_uri[2] == bytes:
        raise RollbackException("Couldn't open taxonomy, rollbacking view", o_view)
    taxo = taxo_uri[1]

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
    se_col = "STANDARD_ERROR_GENOME_SIZE"
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

    Column.new_column(o_view,
                      mean_size_col,
                      OBI_FLOAT)

    Column.new_column(o_view,
                      median_size_col,
                      OBI_FLOAT)

    Column.new_column(o_view,
                      var_col,
                      OBI_FLOAT)

    Column.new_column(o_view,
                      sd_col,
                      OBI_FLOAT)

    # Initialize some columns
    for taxon in taxo:
        taxid = taxon.taxid
        o_view[taxid][infonode_col] = False
        o_view[taxid][species_count_col] = 0
        o_view[taxid][genome_count_col] = 0
        o_view[taxid][tax_rank_col] = taxo.get_rank(taxid)
        o_view[taxid][scientific_name_col] = taxo.get_scientific_name(taxid)
        o_view[taxid][density_col] = 0.0
        o_view[taxid][taxid_col] = taxid

    logger("info", "Initialized columns")

    print(o_view[33961][infonode_col])
    print(o_view[33961])

    # Compute and store info about the nodes with assembly info
    
    genome_dict = {}
    for genome in i_view:
        # Get taxid
        taxid = genome[TAXID_COLUMN]
        taxid = taxo.get_taxon_by_taxid(taxid).taxid
        genome_size = genome[genome_ungapped_length_col]
        
        #if taxid == 33961:
        #    print(taxo.get_rank(taxid))
        
        # Store the info for that taxid
        if taxid not in genome_dict:
            genome_dict[taxid] = [genome_size]
        else:
            genome_dict[taxid].append(genome_size)
    
    for taxid in genome_dict:
        o_view[taxid][infonode_col] = True
        #if taxid == 33961:
        #    print('33961 or 1614', taxo.get_taxon_by_taxid(taxid).taxid)
        if taxo.get_rank(taxid) != b"species": # computed later if species
            o_view[taxid][genome_size_col] = tuple(genome_dict[taxid])
            o_view[taxid][genome_count_col] = len(genome_dict[taxid])
            o_view[taxid][mean_size_col] = statistics.mean(genome_dict[taxid])
            o_view[taxid][median_size_col] = statistics.median(genome_dict[taxid])
            if len(genome_dict[taxid]) >= 2 :
                o_view[taxid][var_col] = statistics.variance(genome_dict[taxid])
                o_view[taxid][sd_col] = statistics.stdev(genome_dict[taxid])
                o_view[taxid][se_col] = o_view[taxid][sd_col] / math.sqrt(len(genome_dict[taxid]))
    
    logger("info", "Computed assembly statistics at nodes with assemblies")
    
    # Then compute for each node:
    # from the leaves of each node, mean median CI var sd emptiness(%of children leaves with a GSR)
    
    # Propagate infos up the taxonomic tree
    
    # Species count info
    
    # Compute species count under each taxon
    for taxon in taxo:
        taxid = taxon.taxid
        # if species rank:
        if o_view[taxid][tax_rank_col] == b"species":
            # for each ancestor:
            itself=True
            for ancestor in taxo.parental_tree_iterator(taxid):
                # +1 to species count column
                if not itself: # first parent yielded is itself
                    o_view[ancestor.taxid][species_count_col] += 1
                else:
                    itself = False
            
    logger("info", "Computed children species count at all nodes")
    
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
                if sp_taxid == 33961:
                    print('oui dans le dict 204')
                if taxid == 33961:
                    print('oui dans le dict 204 is taxid:')
                    print([taxon.taxid for taxon in taxo.parental_tree_iterator(taxid)])
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
            o_view[species][se_col] = o_view[species][sd_col] / math.sqrt(len(sp_genome_dict[species]))
        if species == 33961:
            print(o_view[species])
                
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

    logger("info", "Propagated assembly metadata up to all nodes")

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
            o_view[ancestor][se_col] = o_view[ancestor][sd_col] / math.sqrt(len(anc_genome_dict[ancestor]))
        if ancestor == 33961:
            print(o_view[33961])

    logger("info", "Computed assembly statistics for all nodes")

    # Compute density
    for taxon in taxo:
        taxid = taxon.taxid
        if taxid == 33961:
            print('oui 33961 in taxo')
        if taxid == 1614:
            print('oui 1614 in taxo')
        if o_view[taxid][species_count_col] > 0:
            o_view[taxid][density_col] = o_view[taxid][genome_count_col] / o_view[taxid][species_count_col]

    logger("info", "Computed density for all nodes")   
    
    print(o_view[33961][infonode_col])
    print(o_view[33961])
    
    # Save command config in View and DMS comments
    command_line = " ".join(sys.argv[1:])
    input_dms_name=[input[0].name]
    input_view_name=[input[1].name]
    if 'taxoURI' in config['obi'] and config['obi']['taxoURI'] is not None:
        input_dms_name.append(config['obi']['taxoURI'].split("/")[-3])
        input_view_name.append("taxonomy/"+config['obi']['taxoURI'].split("/")[-1])
    o_view.write_config(config, "buildgenomesizedb", command_line, input_dms_name=input_dms_name, input_view_name=input_view_name)
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

    logger("info", "Done.")
    
    
    # TODO compute stats from direct children (less weight to nodes with lots of ancestors)    
    # children_dict = {} # dict of direct children
    # for taxon in taxo:
        # child = taxon.taxid
        # ancestor = taxon.parent.taxid
        # if ancestor not in children_dict:
            # children_dict[ancestor] = [child]
        # else:
            # children_dict[ancestor].append(child)
    # for ancestor in children_dict:
        # genome_count = 0
        # children_sizes = []
        # for child in children_dict[ancestor]:
            # if child <= len(o_view) and o_view[child][infonode_col] == True:
                # genome_count += 1
                # children_sizes.append(o_view[taxid][mean_size_col]) # or median... TODO

    # First walkthrough
    # for taxon in o_view:
        # if taxon[infonode_col] is True:
        #
        #
    # for ancestor in children_dict:
        # genome_count = 0
        # children_sizes = []
        # for child in children_dict[ancestor]:
            # if child <= len(o_view) and o_view[child][genome_count_col] is not None:
                # genome_count += 1
                # children_sizes.append(o_view[taxid][mean_size_col]) # or median... TODO
                #
                #
        # total_children = len(children_dict[ancestor])
        # o_view[emptiness_col][child] = genome_count / total_children

