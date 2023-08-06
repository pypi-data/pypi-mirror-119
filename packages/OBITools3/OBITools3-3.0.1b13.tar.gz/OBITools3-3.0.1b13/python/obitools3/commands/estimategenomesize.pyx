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
 
__title__="Estimate genome size from amplicon data"


def addOptions(parser):    
    addMinimalInputOption(parser)
    addTaxonomyOption(parser)
    addMinimalOutputOption(parser)

    group = parser.add_argument_group('obi estimategenomesize specific options')

    group.add_argument('-D', '--genome-size-ref-db',
                     action="store", dest="estimategenomesize:db",
                     metavar="<URI>",
                     default=None,
                     type=str,
                     help="URI to the genome size reference database")

    group.add_argument('-R', '--original-genome-size-ref-db',
                     action="store", dest="estimategenomesize:odb",
                     metavar="<URI>",
                     default=None,
                     type=str,
                     help="URI to the original genome size reference database (for testing)")
        
    group.add_argument('-T', '--testing-mode',
                     action="store_true", dest="estimategenomesize:test",
                     default=False,
                     help="Test mode: sampling without replacement for queries already in the database")

    group.add_argument('-o', '--only-id',
                     action="store", dest="estimategenomesize:only",
                     metavar="<URI>",
                     default=None,
                     type=str,
                     help="Only compute for this sequence id")



def method1_unweighted_mean(config, o_view, idx, db, odb, taxo, best_matches, \
            mean_size_col_name, estimated_size_col_name, actual_size_col_name, assigned_mean_size_col_name, refs_col_name, dist_col_name, diff_col_name, \
            mean_dist_col_name, mean_diff_col_name, all_sizes_under_col_name, conf_inter_col_name, st_error_col_name):
    mean_sizes=[]
    actual_sizes = []
    refs=[]
    dist=[]
    diff=[]
    for match in best_matches:
        d = 0
        got_actual_size = False
        for p in taxo.parental_tree_iterator(match):
            ptaxid = p.taxid
            if db[ptaxid][mean_size_col_name] is not None: # TODO save col for efficiency
                if "test" in config["estimategenomesize"] and config["estimategenomesize"]["test"] and d==0:
                    actual_sizes.append(db[ptaxid][mean_size_col_name])
                    got_actual_size = True
                    pass
                else:
                    mean_sizes.append(db[ptaxid][mean_size_col_name])
                    if got_actual_size:
                        diff.append(actual_sizes[-1] - db[ptaxid][mean_size_col_name])
                    refs.append(ptaxid)
                    dist.append(d)
                    break
            d+=1

    o_view[idx][estimated_size_col_name] = round(statistics.mean(mean_sizes))
    o_view[idx][actual_size_col_name] = actual_sizes
    o_view[idx][assigned_mean_size_col_name] = mean_sizes
    o_view[idx][refs_col_name] = refs
    o_view[idx][dist_col_name] = dist
    o_view[idx][diff_col_name] = diff
    if len(dist)>0:
        o_view[idx][mean_dist_col_name] = round(statistics.mean(dist))
    if len(diff)>0:
        o_view[idx][mean_diff_col_name] = round(statistics.mean(diff))


def method2_weighted_mean(config, o_view, idx, db, odb, taxo, best_matches, \
            mean_size_col_name, estimated_size_col_name, actual_size_col_name, assigned_mean_size_col_name, refs_col_name, \
            dist_col_name, diff_col_name, mean_dist_col_name, mean_diff_col_name, all_sizes_under_col_name, conf_inter_col_name, st_error_col_name):
    mean_sizes=[]
    actual_sizes = []
    refs=[]
    dist=[]
    diff=[]
    all_sizes_under=[]
    standard_errors=[]
    got_actual_size = False

    if "test" in config["estimategenomesize"] and config["estimategenomesize"]["test"]:
        true_taxid = o_view['TRUE_TAXID'][idx]
        if odb[true_taxid][mean_size_col_name] is not None: # TODO save col for efficiency
            actual_size = odb[true_taxid][mean_size_col_name]
            got_actual_size = True
    
    for match in best_matches:
        #print(match, '########################################', match)
        d = 0
        for p in taxo.parental_tree_iterator(match):
            ptaxid = p.taxid
            #print('ancestor:', ptaxid, db[ptaxid][mean_size_col_name])
            if db[ptaxid][mean_size_col_name] is not None: # TODO save col for efficiency
                if ptaxid not in refs:
                    mean_sizes.append(db[ptaxid][mean_size_col_name])
                    standard_errors.append(db[ptaxid]['STANDARD_ERROR_GENOME_SIZE']) # TODO macro
                    # for confidence interval
                    #all_sizes_under.extend(db[ptaxid][all_sizes_under_col_name])
                    if got_actual_size:
                        diff.append(actual_size - db[ptaxid][mean_size_col_name])
                    refs.append(ptaxid)
                    dist.append(d)
                break
            d+=1

    #print(len(best_matches), len(refs))
    
    estimated_size = 0
    sum_weights = 0
    for i in range(len(mean_sizes)):
        estimated_size += ( (1.0/(dist[i]+1)) * mean_sizes[i] )
        sum_weights += (1.0/(dist[i]+1))
    
    #print(o_view[idx].id)
    #print(best_matches)
    #print(mean_sizes)
    #print(dist)
    
    estimated_size /= sum_weights
    
    o_view[idx][estimated_size_col_name] = estimated_size
    
    # the standard error of the weighted mean is sqrt( (w1*s1)^2 + (w2*s2)^2 + (w3*s3)^2). 
    # And then you can get your CI as the usual weighted mean plus or minus 1.96 times its standard error.

    # if at least 2 values, compute standard error and confidence interval

    Z = 1.96     # 95% CI
    if len(standard_errors) >= 2:
        # compute standard error of weighted mean
        st_err = 0
        for i in range(len(standard_errors)):
            if standard_errors[i] is not None: # None problem
                weight = 1/(dist[i]+1)
                st_err_i = standard_errors[i]
                st_err += (weight * st_err_i)**2
        o_view[idx][st_error_col_name] = math.sqrt(st_err)
    
        # compute confidence interval
        o_view[idx][conf_inter_col_name] = Z * o_view[idx][st_error_col_name]
    elif db[ptaxid]['STANDARD_ERROR_GENOME_SIZE'] is not None:
        o_view[idx][st_error_col_name] = db[ptaxid]['STANDARD_ERROR_GENOME_SIZE']
        o_view[idx][conf_inter_col_name] = Z * db[ptaxid]['STANDARD_ERROR_GENOME_SIZE']
    
#    if len(all_sizes_under) >= 2 :
#        Z = 1.96     # 95% CI
#        standard_deviation = statistics.stdev(all_sizes_under)
#        o_view[idx][conf_inter_col_name] = # Z * (standard_deviation / math.sqrt(len(all_sizes_under)))
        #o_view[idx][conf_inter_col_name] = 
#    else:
  #      o_view[idx][conf_inter_col_name] = 0.0
    # compute standard error
#    if len(all_sizes_under) >= 2 :
 #       o_view[idx][st_err_col_name] = math.sqrt( (w1*sterr1)^2 + (w2*sterr2)^2 + (w3*sterr3)^2 )
        # standard_deviation / math.sqrt(len(all_sizes_under))
 #   else:
 #       o_view[idx][st_err_col_name] = 0.0   
    
    if "test" in config["estimategenomesize"] and config["estimategenomesize"]["test"]:
        o_view[idx][b'DIFF'] = actual_size - estimated_size
        o_view[idx][actual_size_col_name] = actual_size
        o_view[idx][diff_col_name] = diff
        if len(diff)>0:
            o_view[idx][mean_diff_col_name] = round(statistics.mean(diff))
    
    o_view[idx][assigned_mean_size_col_name] = mean_sizes
    o_view[idx][refs_col_name] = refs
    o_view[idx][dist_col_name] = dist
    if len(dist)>0:
        o_view[idx][mean_dist_col_name] = round(statistics.mean(dist),2)


def run(config):

    DMS.obi_atexit()
    
    #logger("info", "obi estimategenomesize")

    estimate_fun = method2_weighted_mean
    
    if 'only' in config['estimategenomesize']:
        only = config['estimategenomesize']['only']
    else:
        only = None
    
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

    # If the input and output DMS are not the same, import the input view in the output DMS before cloning it to modify it
    # (could be the other way around: clone and modify in the input DMS then import the new view in the output DMS)
    if i_dms != o_dms:
        imported_view_name = i_view_name
        i=0
        while imported_view_name in o_dms:  # Making sure view name is unique in output DMS
            imported_view_name = i_view_name+b"_"+str2bytes(str(i))
            i+=1
        View.import_view(i_dms.full_path[:-7], o_dms.full_path[:-7], i_view_name, imported_view_name)
        i_view = o_dms[imported_view_name]

    # Clone output view from input view
    o_view = i_view.clone(o_view_name)
    if o_view is None:
        raise Exception("Couldn't create output view")
    i_view.close()

    if "db" in config["estimategenomesize"]:
        dbi = open_uri(config["estimategenomesize"]["db"])
        if dbi is None:
            raise Exception("Could not open genome size reference database")
        db = dbi[1]
    else:
        raise Exception("No genome size reference database provided")

    if "odb" in config["estimategenomesize"]:
        odbi = open_uri(config["estimategenomesize"]["odb"])
        if odbi is None:
            raise Exception("Could not open original genome size reference database")
        odb = odbi[1]
    else:
        odb = None
    
    taxo_uri = open_uri(config['obi']['taxoURI'])
    if taxo_uri is None or taxo_uri[2] == bytes:
        raise RollbackException("Couldn't open taxonomy, rollbacking view", o_view)
    taxo = taxo_uri[1]

    best_match_col_name = "BEST_MATCH_TAXIDS"
    #best_match_col_name = "TAXID"
    mean_size_col_name = "MEAN_GENOME_SIZE"
    estimated_size_col_name = "ESTIMATED_GENOME_SIZE"  
    assigned_mean_size_col_name = "ASSIGNED_MEAN_GENOME_SIZES"
    refs_col_name = "GENOME_REFS"
    dist_col_name = "DISTANCE_TO_GENOME_REFS"
    diff_col_name = "DISTANCE_TO_ACTUAL_SIZE"
    mean_dist_col_name = "MEAN_DISTANCE_TO_GENOME_REFS"
    mean_diff_col_name = "MEAN_DISTANCE_TO_ACTUAL_SIZE"
    actual_size_col_name = "ACTUAL_GENOME_SIZE"
    all_sizes_under_col_name = "GENOME_SIZE"
    conf_inter_col_name = "CONFIDENCE_INTERVAL"
    st_error_col_name = "STANDARD_ERROR"

    # Create columns
    Column.new_column(o_view,
                      assigned_mean_size_col_name,
                      OBI_FLOAT,
                      tuples=True)
    Column.new_column(o_view,
                      estimated_size_col_name,
                      OBI_FLOAT)
    Column.new_column(o_view,
                      actual_size_col_name,
                      OBI_FLOAT)
    Column.new_column(o_view,
                      conf_inter_col_name,
                      OBI_FLOAT)
    Column.new_column(o_view,
                      diff_col_name,
                      OBI_FLOAT,
                      tuples=True)
    Column.new_column(o_view,
                      refs_col_name,
                      OBI_INT,
                      tuples=True)
    Column.new_column(o_view,
                      dist_col_name,
                      OBI_INT,
                      tuples=True)
    
    # Save col instance for efficiency
    best_match_col = o_view[best_match_col_name]
        
    # For each query
    for i in range(len(o_view)):
        if only is None or o_view[i].id == tobytes(only):
            #best_matches = [best_match_col[i]]
            best_matches = best_match_col[i]
            #print(best_matches)
            estimate_fun(config, o_view, i, db, odb, taxo, best_matches, \
                         mean_size_col_name, estimated_size_col_name, actual_size_col_name, assigned_mean_size_col_name, refs_col_name, \
                         dist_col_name, diff_col_name, mean_dist_col_name, mean_diff_col_name, all_sizes_under_col_name, conf_inter_col_name, st_error_col_name)
    
    #logger("info", "Recovered genome size information")
    
    # Save command config in View and DMS comments
    command_line = " ".join(sys.argv[1:])
    input_dms_name=[input[0].name]
    input_view_name=[i_view_name]
    if 'taxoURI' in config['obi'] and config['obi']['taxoURI'] is not None:
        input_dms_name.append(config['obi']['taxoURI'].split("/")[-3])
        input_view_name.append("taxonomy/"+config['obi']['taxoURI'].split("/")[-1])
    o_view.write_config(config, "estimategenomesize", command_line, input_dms_name=input_dms_name, input_view_name=input_view_name)
    o_dms.record_command_line(command_line)

    # stdout output: write to buffer
    if type(output_0)==BufferedWriter:
        logger("info", "Printing to output...")
        o_view.print_to_output(output_0, noprogressbar=config['obi']['noprogressbar'])
        o_view.close()

    # If the input and the output DMS are different or if stdout output, delete the temporary imported view used to create the final view
    if i_dms != o_dms or type(output_0)==BufferedWriter:
        View.delete_view(o_dms, imported_view_name)
        o_dms.close(force=True)
    i_dms.close(force=True)

    #logger("info", "Done.")



