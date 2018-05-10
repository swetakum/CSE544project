import pandas, math
import numpy as np
from scipy import stats
import matplotlib.pylab as plot_a

def ks_test(first_half, second_half):
    # using the module scipy to get the tow sample KS test results
    first_half_length = len(first_half)
    second_half_length = len(second_half)
    print first_half_length, second_half_length
    ks_result = stats.ks_2samp(first_half, second_half)
    sum = float(first_half_length + second_half_length)
    product = float(first_half_length * second_half_length)
    critical_value = float(1.36 * math.sqrt(sum/product))
    print "KS Test Score:", ks_result.statistic
    print critical_value
    # , ", P-Value:", ks_result.pvalue
    # if ks_result.statistic > critical_value:
    #     print "Hypo"

def walds_two_population_test(first_half, second_half):
    first_half_mean, second_half_mean, first_half_sum, second_half_sum, first_half_variance, second_half_variance, first_half_standard_deviation, second_half_standard_deviation = 0, 0, 0, 0, 0, 0, 0, 0
    for x in first_half:
        first_half_sum = first_half_sum + x
    for x in second_half:
        second_half_sum = second_half_sum + x
    first_half_mean = first_half_sum/len(first_half)
    second_half_mean = second_half_sum/len(second_half)
    # print first_half_mean,  second_half_mean
    for x in first_half:
        first_half_variance = first_half_variance + (first_half_mean - x)*(first_half_mean - x)
    first_half_variance = first_half_variance/len(first_half)
    first_half_standard_deviation = math.sqrt(first_half_variance)
    # np.std()
    # print first_half_standard_deviation
    for x in second_half:
        second_half_variance = second_half_variance + (second_half_mean - x)*(second_half_mean - x)
    second_half_variance = second_half_variance/len(second_half)
    second_half_standard_deviation = math.sqrt(second_half_variance)
    # print second_half_standard_deviation
    first_half_variance_n = first_half_variance/len(first_half)
    second_half_variance_n = second_half_variance/len(second_half)
    w = abs((first_half_mean - second_half_mean)/math.sqrt(first_half_variance_n + second_half_variance_n))
    print "Two Population Wald's Test Score:", w

# checking the range of outliers
def outlier_range(list):
    list = np.array(list)
    upper_quartile = np.percentile(list, 75)
    lower_quartile = np.percentile(list, 25)
    iqr = (upper_quartile - lower_quartile) * 1.5
    acceptable_range = (lower_quartile - iqr, upper_quartile + iqr)
    return acceptable_range

def main():
    with open('processed_data.csv', 'r') as csv_file:
        # read the csv file using pandas
        df = pandas.read_csv(csv_file)

        # for years from 2013 to 2015, we run the tests
        for year in range(2013, 2016):
            print "-------------------------------------------------------------"
            print "For year:", year
            print "=============="
            only_year = df['year'] == year
            payroll_year = df[only_year]

            # get the data only for employees who are working full time
            full_time = payroll_year['employment_type'] == 'Full Time'
            full_time_only = payroll_year[full_time]

            # calculate for each departments
            list_of_departments = ["Police (LAPD)", "City Attorney","City Clerk", "Housing And Community Investment Department"]
            for x in list_of_departments:
                only_fire_year = full_time_only['department_title'] == x
                fire_department = full_time_only[only_fire_year]

                print "-----------------"
                print x
                print "-----------------"

                # quarterly payments q1,q2,q3,q4
                fire_q1_payments = fire_department['q1_payments']
                fire_q2_payments = fire_department['q2_payments']
                fire_q3_payments = fire_department['q3_payments']
                fire_q4_payments = fire_department['q4_payments']

                # initialise lists to hold processed data
                fire_q1_payments_list, fire_q2_payments_list, fire_q3_payments_list, fire_q4_payments_list = [], [], [], []
                fire_q1_no_outliers,fire_q2_no_outliers,fire_q3_no_outliers,fire_q4_no_outliers = [],[],[],[]
                fire_first_half, fire_second_half = [],[]

                # converting pandas series into lists
                for x in fire_q1_payments:
                    fire_q1_payments_list.append(x)
                for x in fire_q2_payments:
                    fire_q2_payments_list.append(x)
                for x in fire_q3_payments:
                    fire_q3_payments_list.append(x)
                for x in fire_q4_payments:
                    fire_q4_payments_list.append(x)

                # determine the range where data is to be accepted. others will be treated as outliers
                fire_q1_acceptable_range = outlier_range(fire_q1_payments)
                fire_q2_acceptable_range = outlier_range(fire_q2_payments)
                fire_q3_acceptable_range = outlier_range(fire_q3_payments)
                fire_q4_acceptable_range = outlier_range(fire_q4_payments)

                # for loop to reject outliers
                for i in range(0, len(fire_q1_payments_list)):
                    if ((fire_q1_payments_list[i] > fire_q1_acceptable_range[0]) and (fire_q2_payments_list[i] > fire_q2_acceptable_range[0]) and (fire_q3_payments_list[i] > fire_q3_acceptable_range[0]) and (fire_q4_payments_list[i] > fire_q4_acceptable_range[0])):
                        if fire_q1_payments_list[i] < fire_q1_acceptable_range[1] and fire_q2_payments_list[i] < fire_q2_acceptable_range[1] and fire_q3_payments_list[i] < fire_q3_acceptable_range[1] and fire_q4_payments_list[i] < fire_q4_acceptable_range[1]:
                            if fire_q1_payments_list[i]!= 0 and fire_q2_payments_list[i]!= 0 and fire_q3_payments_list[i]!= 0 and fire_q4_payments_list[i]!= 0:
                                fire_q1_no_outliers.append(fire_q1_payments_list[i])
                                fire_q2_no_outliers.append(fire_q2_payments_list[i])
                                fire_q3_no_outliers.append(fire_q3_payments_list[i])
                                fire_q4_no_outliers.append(fire_q4_payments_list[i])
                            else:
                                continue

                # q1+q2 as first_half and q3+q4 and second half
                for i in range(0, len(fire_q1_no_outliers)):
                    fire_first_half.append(fire_q1_no_outliers[i] + fire_q2_no_outliers[i])
                    fire_second_half.append(fire_q3_no_outliers[i] + fire_q4_no_outliers[i])
                '''
                    The tests used for our hypothesis.
                    Here we assume that the data is normal.
                '''

                min = len(fire_first_half)
                fire_first_half_modified = fire_first_half[0:min]
                fire_first_half_modified = fire_first_half

                # firing the two tests
                walds_two_population_test(fire_first_half, fire_second_half)
                ks_test(fire_first_half, fire_second_half)

            print "-------------------------------------------------------------"

if __name__ == "__main__":
    main()
