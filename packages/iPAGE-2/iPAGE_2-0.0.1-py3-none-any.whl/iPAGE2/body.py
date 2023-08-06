from . import heatmap
from . import stat_ipage
from . import preprocess
from . import MI
import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.stats.multitest import multipletests
import pickle

# A number of variables in ipage were renamed, which was not done in other files.
# expression_level -> de_profile
# expression_profile -> de_profile_discr
# database_name -> annotation_name
# db_names -> ann_names
# db_profiles -> ann_profiles
# db_annotations -> ann_annotations
# e_ft -> de_ft
# db_ft -> ann_ft
# tmp -> annotation_dir
# freq_bins -> a_bins
# e_bins -> de_bins
# draw_bins -> heatmap_bins
# max_draw_output -> max_heatmap_rows


def process_input(expression_level, genes, database_index_file, input_format, output_format, expression_bins,
                  abundance_bins, species, tmp, symmetric_expression):

    expression_profile, genes = preprocess.get_expression_profile(expression_level, genes, expression_bins,
                                                                  input_format, output_format, species, tmp,
                                                                  symmetric_expression)

    database_name = database_index_file.split('/')[-1].split('.')[0]
    db_names, db_annotations, db_genes, db_profiles = preprocess.load_database(database_name, tmp)

    genes, expression_profile, db_profiles = preprocess.sort_genes(genes, db_genes, expression_profile, db_profiles)

    abundance_profile = db_profiles.sum(0)
    abundance_profile = MI.discretize_equal_size(abundance_profile, abundance_bins)

    return expression_profile, db_names, db_profiles, db_annotations, abundance_profile, genes


def count_cmi_for_profiles(expression_profile, db_profiles, abundance_profile, expression_bins, db_bins,
                           abundance_bins, function):
    cmis = []
    for profile in db_profiles:
        if function == 'cmi':
            cmi = MI.cond_mut_info(expression_profile, profile, abundance_profile, expression_bins, db_bins, abundance_bins)
        elif function == 'mi':
            cmi = MI.mut_info(expression_profile, profile, expression_bins, db_bins)
        cmis.append(cmi)
    cmis = np.array(cmis)
    return cmis


def statistical_testing(cmis, expression_profile, db_profiles, abundance_profile, expression_bins, db_bins,
                        abundance_bins, function, shuffles=10000, alpha=0.01, multipletest_method='None',
                        filter_redundant=False, redundancy_ratio=0.1):
    indices = np.argsort(cmis)[::-1]
    rev_indices = np.argsort(indices)
    db_profiles = db_profiles[indices]
    accepted_db_profiles = np.array([False] * len(db_profiles))
    z_scores = np.zeros(len(db_profiles), dtype=float)
    false_hits = 0
    for i in range(db_profiles.shape[0]):
        z_score, passed_thr = stat_ipage.test_cond_mi(expression_profile, db_profiles[i], abundance_profile,
                                                      expression_bins, db_bins, abundance_bins,
                                                      alpha=alpha, function=function, shuffles=shuffles)

        accepted_db_profiles[i] = passed_thr
        z_scores[i] = z_score
        false_hits = (false_hits + (not passed_thr)) * (not passed_thr)  # add 1 if 0, make zero if 1
        if false_hits > 5:
            break
    if multipletest_method != 'None':
        accepted_db_profiles = multipletests(norm.sf(z_scores), alpha, multipletest_method)[0]
    # remove_redundantly_informative_pathways
    if filter_redundant:
        for i in np.where(accepted_db_profiles)[0]:
            for j in np.where(accepted_db_profiles)[0][np.where(accepted_db_profiles)[0] < i]:
                cmi = MI.cond_mut_info(db_profiles[i], expression_profile, db_profiles[j], db_bins, expression_bins, db_bins)
                mi = MI.mut_info(db_profiles[i], db_profiles[j], db_bins, db_bins)
                if cmi / mi < redundancy_ratio:
                    accepted_db_profiles[i] = False
    accepted_db_profiles, z_scores = accepted_db_profiles[rev_indices], z_scores[rev_indices]
    return accepted_db_profiles, z_scores


def get_rbp_expression(genes, output_format, expression_profile, accepted_db_profiles, db_names, db_annotations, species, tmp):
    rbp_names = [db_names[i].split('_')[0] for i in range(len(db_names)) if accepted_db_profiles[i]]
    rbp_annotations = [db_annotations[i] for i in range(len(db_names)) if accepted_db_profiles[i]]

    genes_symbols = preprocess.change_accessions(genes, output_format, 'gs', species, tmp)
    rbp_expression = dict(zip([rbp_annotations[i] for i in range(len(rbp_names)) if rbp_names[i] in genes_symbols],
                              [expression_profile[genes_symbols.index(name)] for name in rbp_names
                               if name in genes_symbols]))
    rbp_expression.update({el: np.nan for el in rbp_annotations if el not in rbp_expression})
    return rbp_expression


def produce_output(accepted_db_profiles, db_profiles, db_names, db_annotations, cmis, z_scores,
                   draw_bins, max_draw_output, output_name, cmap_main, cmap_reg, rbp_expression=None, export_heatmap=0):
    p_values = {}
    for i in range(len(db_profiles)):
        if accepted_db_profiles[i]:
            p_values[db_annotations[i]] = stat_ipage.get_p_values(db_profiles[i], draw_bins)
    up_regulated_func = lambda x: sum(p_values[x][:len(p_values[x]) // 2]) <= sum(p_values[x][len(p_values[x]) // 2:])
    down_regulated_func = lambda x: sum(p_values[x][:len(p_values[x]) // 2]) > sum(p_values[x][len(p_values[x]) // 2:])
    order_to_cmi = lambda x: cmis[db_annotations.index(x)]
    max_draw_output = min(max_draw_output, len(p_values))
    up_regulated = sorted(filter(up_regulated_func, p_values), key=order_to_cmi, reverse=True)
    down_regulated = sorted(filter(down_regulated_func, p_values), key=order_to_cmi, reverse=True)

    max_draw_output = min(max_draw_output, len(p_values))
    if max_draw_output // 2 >= len(up_regulated):
        p_names = up_regulated + down_regulated[: max_draw_output - len(up_regulated)]
    elif max_draw_output // 2 >= len(down_regulated):
        p_names = up_regulated[: max_draw_output - len(down_regulated)] + down_regulated
    else:
        p_names = up_regulated[:max_draw_output//2] + down_regulated[:max_draw_output//2]

    for i in range(draw_bins-2):
        p_names = sorted(p_names, key=lambda x: sum(p_values[x][i:i+3]), reverse=True)

    p_values = [p_values[name] for name in p_names]
    if rbp_expression:
        rbp_expression = [rbp_expression[name] for name in p_names]

    if export_heatmap:
        with open(output_name + '_heatmap.pickle', "wb+") as f:
            pickle.dump(p_names, f, pickle.HIGHEST_PROTOCOL)
            pickle.dump(p_values, f, pickle.HIGHEST_PROTOCOL)
            pickle.dump(rbp_expression, f, pickle.HIGHEST_PROTOCOL)

    if len(p_values) != 0 and output_name != 'shut':
        heatmap.draw_heatmap(p_names, p_values, output_name, rbp_expression, cmap_main, cmap_reg)
    output = pd.DataFrame(columns=['Group', 'CMI', 'Z-score', 'Regulation'])
    j = 0
    for name in up_regulated:
        i = db_annotations.index(name)
        output.loc[j] = [db_names[i], cmis[i], z_scores[i], 'UP']
        j += 1
    for name in down_regulated:
        i = db_annotations.index(name)
        output.loc[j] = [db_names[i], cmis[i], z_scores[i], 'DOWN']
        j += 1
    if output_name != 'stdout' and output_name != 'shut':
        output.to_csv(output_name + '.out.tsv', index=False, sep='\t')
    return output
