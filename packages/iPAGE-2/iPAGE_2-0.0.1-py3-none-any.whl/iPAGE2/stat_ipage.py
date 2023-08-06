from scipy.stats import hypergeom
import numpy as np
from . import MI


def hypergeometric(objects_in_bin, total_size, objects_total, bin_size):
    p_over = np.log10(hypergeom.sf(objects_in_bin-1, total_size, objects_total, bin_size))
    p_under = np.log10(hypergeom.cdf(objects_in_bin, total_size, objects_total, bin_size))
    if p_over < p_under:
        p = -p_over
    else:
        p = p_under
    if abs(p) > 3:
        return p/(abs(p))*3
    else:
        return p


def get_p_values(profile, nbins):
    bin_size = len(profile) // nbins
    remain = len(profile) - nbins * bin_size
    p_values = []
    objects_total = sum(profile)
    total_size = len(profile)
    objects_in_bin = sum(profile[:bin_size+remain])
    p = hypergeometric(objects_in_bin, total_size, objects_total, bin_size + remain)
    p_values.append(p)
    for i in range(1, nbins):
        objects_in_bin = sum(profile[bin_size * i:bin_size * (i + 1)])
        p = hypergeometric(objects_in_bin, total_size, objects_total, bin_size)
        p_values.append(p)
    return p_values


def test_cond_mi(expression_profile, db_profile, abundance_profile=None, expression_bins=10, db_bins=2, abundance_bins=3,
                 shuffles=1000, alpha=0.01, function='cmi'):
    if function == 'cmi':
        cmi = MI.cond_mut_info(expression_profile, db_profile, abundance_profile, expression_bins, db_bins, abundance_bins)
    elif function == 'mi':
        cmi = MI.mut_info(expression_profile, db_profile, expression_bins, db_bins)
    max_vectors_over = shuffles * alpha
    expression_shuffled_profile = expression_profile.copy()
    vectors_over = 0
    cmis = []
    np.random.seed()
    for i in range(shuffles):
        np.random.shuffle(expression_shuffled_profile)

        if function == 'cmi':
            new_cmi = MI.cond_mut_info(expression_shuffled_profile, db_profile, abundance_profile, expression_bins,
                                       db_bins, abundance_bins)
        elif function == 'mi':
            new_cmi = MI.mut_info(expression_shuffled_profile, db_profile, expression_bins, db_bins)

        cmis.append(new_cmi)
        if cmi <= new_cmi:
            vectors_over += 1
        if vectors_over >= max_vectors_over:
            z_score = 0
            passed_thr = False
            return z_score, passed_thr
    z_score = (cmi - np.average(cmis)) / np.std(cmis)
    passed_thr = True
    return z_score, passed_thr
