import symro
from symro.core.handlers.entitybuilder import EntityBuilder
from symro.core.parsing.amplparser import AMPLParser
from symro.test.test_util import *


# Scripts
# ----------------------------------------------------------------------------------------------------------------------

SUB_SET_SCRIPT = """
set NUM_SET = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
set EVEN_SET = {0, 2, 4, 6, 8};

set LETTER_SET = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'};

set NUM_LETTER_SET = {NUM_SET, LETTER_SET};

set INDEXED_SET{i in NUM_SET} = 0..i;
set INDEXED_SET_2{i in NUM_SET} = {(i,j) in NUM_LETTER_SET};

var VAR_1{i in NUM_SET} >= 0;
var VAR_2{i in NUM_SET, j in LETTER_SET} >= 0;
var VAR_test{i in NUM_SET: 1 in union{i1 in NUM_SET}{1..1: i == 5}};

minimize OBJ: 0;

display {i in NUM_SET: 1 in union{i1 in NUM_SET}{1..1: i == 5}};
"""


# Tests
# ----------------------------------------------------------------------------------------------------------------------


def run_entity_builder_test_group():
    tests = [("Build sub-meta-entities", sub_meta_entity_builder_test)]
    return run_tests(tests)


def sub_meta_entity_builder_test():

    problem = symro.build_problem(script_literal=SUB_SET_SCRIPT,
                                  working_dir_path=SCRIPT_DIR_PATH)

    entity_builder = EntityBuilder(problem)
    ampl_parser = AMPLParser(problem)

    results = []

    mv_1 = problem.get_meta_entity("VAR_1")
    mv_2 = problem.get_meta_entity("VAR_2")

    # test 1: {i in NUM_SET} VAR_1[i]
    idx_node = ampl_parser.parse_entity_index("[i]")
    sub_meta_entity = entity_builder.build_sub_meta_entity(idx_subset_node=mv_1.idx_set_node,
                                                           meta_entity=mv_1,
                                                           entity_idx_node=idx_node)
    results.append(check_result(sub_meta_entity, "var VAR_1{i in NUM_SET}"))

    # test 2: {i in EVEN_SET} VAR_1[i]
    idx_subset_node = ampl_parser.parse_indexing_set_definition("{i in EVEN_SET}")
    idx_node = ampl_parser.parse_entity_index("[i]")
    sub_meta_entity = entity_builder.build_sub_meta_entity(idx_subset_node=idx_subset_node,
                                                           meta_entity=mv_1,
                                                           entity_idx_node=idx_node)
    results.append(check_result(sub_meta_entity, "var VAR_1{i in NUM_SET: i in {i1 in EVEN_SET}}"))

    # test 3: {i in NUM_SET} VAR_1[5]
    idx_node = ampl_parser.parse_entity_index("[5]")
    sub_meta_entity = entity_builder.build_sub_meta_entity(idx_subset_node=mv_1.idx_set_node,
                                                           meta_entity=mv_1,
                                                           entity_idx_node=idx_node)
    results.append(check_result(sub_meta_entity, "var VAR_1{i in NUM_SET: i == 5}"))

    # problem.engine.api.reset()
    # problem.engine.api.eval(SUB_SET_SCRIPT)

    return results
