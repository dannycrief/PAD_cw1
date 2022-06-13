import pandas as pd
from numpy import sqrt
import numpy as np
from scipy.stats import sem, t

df = pd.read_csv('DATA/cw9/PAD_09_PD.csv', delimiter=';')

mean = df.groupby('Gender')['Annual Income (k$)'].mean()
summa = df.groupby('Gender')['Annual Income (k$)'].sum()

std_dev_male = np.std(df.where(df['Gender'] == 'Male')['Annual Income (k$)'])
std_dev_female = np.std(df.where(df['Gender'] == 'Female')['Annual Income (k$)'])


def independent_ttest(data1, data2, alpha):
    # calculate means
    mean1, mean2 = mean(data1), mean(data2)
    # calculate standard errors
    se1, se2 = sem(data1), sem(data2)
    # standard error on the difference between the samples
    sed = sqrt(se1 ** 2.0 + se2 ** 2.0)
    # calculate the t statistic
    t_stat = (mean1 - mean2) / sed
    # degrees of freedom
    df = len(data1) + len(data2) - 2
    # calculate the critical value
    cv = t.ppf(1.0 - alpha, df)
    # calculate the p-value
    p = (1.0 - t.cdf(abs(t_stat), df)) * 2.0
    # return everything
    return t_stat, df, cv, p


if __name__ == '__main__':
    data1 = None
    data2 = None
    independent_ttest()
