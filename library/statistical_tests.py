from scipy.stats import kstest, zscore, ttest_ind, mannwhitneyu

"""
def evaluate_statistical_significance_differece_algorithm_fitnesses(
    fitness_list_1,
    fitness_list_2,
    label_1="Algorithm 1",
    label_2="Algorithm 2"
):
    
    #Compares two lists of final fitness values using a normality test
    #and performs a t-test or Mann–Whitney U test accordingly.

    #Args:
     #   fitness_list_1 (list): Final fitness values from configuration 1
      #  fitness_list_2 (list): Final fitness values from configuration 2
       # label_1 (str): Name of configuration 1
        #label_2 (str): Name of configuration 2

    #Returns:
     #   dict: Contains the test used, p-value, and significance conclusion
    # Standardize the data for normality testing
    z1 = zscore(fitness_list_1)
    z2 = zscore(fitness_list_2)

    # Normality test
    ks1 = kstest(z1, 'norm')
    ks2 = kstest(z2, 'norm')

    print(f"\nNormality Check (Kolmogorov–Smirnov Test):")

    # Determining if distribution for fitness_list_1 is normal
    if ks1.pvalue >= 0.05:
        print(f"  {label_1}: p = {ks1.pvalue:.5f} → Normal")
    else:
        print(f"  {label_1}: p = {ks1.pvalue:.5f} → Not normal")

    # Determining if distribution for fitness_list_2 is normal
    if ks2.pvalue >= 0.05:
        print(f"  {label_2}: p = {ks2.pvalue:.5f} → Normal")
    else:
        print(f"  {label_2}: p = {ks2.pvalue:.5f} → Not normal")


    # Determine which test to use based on normality
    if ks1.pvalue >= 0.05 and ks2.pvalue >= 0.05:
        # Both normal → use t-test
        stat, p = ttest_ind(fitness_list_1, fitness_list_2)
        test_used = "Student's t-test"
    else:
        # Use non-parametric Mann–Whitney U test
        stat, p = mannwhitneyu(fitness_list_1, fitness_list_2, alternative='two-sided')
        test_used = "Mann–Whitney U test"


    # Print results
    print(f"\n{test_used} between {label_1} and {label_2}:")
    print(f"  Test Statistic = {stat:.4f}")
    print(f"  p-value        = {p:.5f}")
    if p < 0.05:
        print("  Result: Statistically significant difference (p < 0.05)")
    else:
        print("  Result: No statistically significant difference")

    return {
        "test_used": test_used,
        "statistic": stat,
        "p_value": p,
        "significant": p < 0.05
    }

"""

def evaluate_statistical_significance_differece_algorithm_fitnesses(
    fitness_list_1,
    fitness_list_2,
    label_1="Algorithm 1",
    label_2="Algorithm 2"
):
    """
    Compares two lists of final fitness values using the Mann–Whitney U test.
    This non-parametric test does not assume normality and is suitable for most cases.

    Args:
        fitness_list_1 (list): Final fitness values from configuration 1
        fitness_list_2 (list): Final fitness values from configuration 2
        label_1 (str): Name of configuration 1
        label_2 (str): Name of configuration 2

    Returns:
        dict: Contains the test used, p-value, and significance conclusion
    """

    # Run Mann–Whitney U test (non-parametric)
    stat, p = mannwhitneyu(fitness_list_1, fitness_list_2, alternative='two-sided')
    test_used = "Mann–Whitney U test"

    # Print results
    print(f"\n{test_used} between {label_1} and {label_2}:")
    print(f"  Test Statistic = {stat:.4f}")
    print(f"  p-value        = {p:.5f}")
    if p < 0.05:
        print("  Result: Statistically significant difference (p < 0.05)")
    else:
        print("  Result: No statistically significant difference")

    return {
        "test_used": test_used,
        "statistic": stat,
        "p_value": p,
        "significant": p < 0.05
    }

