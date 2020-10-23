import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn import svm
from sklearn.linear_model import SGDRegressor,Ridge,LinearRegression
from sklearn.neural_network import MLPRegressor
from yellowbrick.regressor import prediction_error,residuals_plot




def load_average_vehicle(file_dir):
    average_vehicle_df = pd.read_excel(file_dir, sheet_name="2.1, 2.2, 2.3,2.4", header=2, nrows=19, usecols="A:AH")
    return average_vehicle_df

def load_light_fleet_age(file_dir):
    light_fleet_age_df = pd.read_excel(file_dir, sheet_name="2.10", header=1, nrows=7)
    return light_fleet_age_df

def load_co2_emission(file_dir):
    co2_emission_df = pd.read_excel(file_dir, sheet_name="1.10", header=2, nrows=17, usecols="A:E")
    return co2_emission_df

def plot_normality(target, name):
    mean,std = np.mean(target), np.std(target)
    X = np.linspace(np.min(target), np.max(target), 1000)
    pdf = stats.norm.pdf(X, mean, std)
    plt.plot(X, pdf, label="PDF")
    plt.grid()
    plt.title('Check Normal Distribution for %s' %name,fontsize=10)
    plt.xlabel('x')
    plt.ylabel('Probability')
    plt.show()

def get_sort_array_index(array):
    # print(np.sort(array))
    order = []
    for element in np.sort(array):
        for idx, pca_value in enumerate(array):
            if element == pca_value:
                order.append(idx)

    print(order)

def step_2_4_1_imputation_co2_emission_df(co2_emission_df):
    missing_values = [[2000] + [np.nan for i in range(4)], [2018] + [np.nan for i in range(4)]]

    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(co2_emission_df)
    X = imp.transform(missing_values)

    df = pd.DataFrame(X, columns=co2_emission_df.columns)
    co2_emission_df = pd.concat([co2_emission_df, df])
    co2_emission_df = co2_emission_df.sort_values(by=['Year'])
    co2_emission_df.index = [x for x in range(len(co2_emission_df.index))]

    return co2_emission_df

def step_2_4_2_check_normality(number_fleets_df, light_fleet_age_df,co2_emission_df):
    plot_normality(number_fleets_df['Total LPV new'], 'Total LPV new')
    plot_normality(number_fleets_df[' Total LPV used'], 'Total LPV used')
    plot_normality(number_fleets_df['Total LCV new'], 'Total LCV new')
    plot_normality(number_fleets_df[' Total LCV used'], 'Total LCV used')

    plot_normality(np.array(light_fleet_age_df.iloc[0][1:20].astype(int)), '0-4 age group')
    plot_normality(np.array(light_fleet_age_df.iloc[1][1:20].astype(int)), '5-9 age group')
    plot_normality(np.array(light_fleet_age_df.iloc[2][1:20].astype(int)), '10-14 age group')
    plot_normality(np.array(light_fleet_age_df.iloc[3][1:20].astype(int)), '15-19 age group')
    plot_normality(np.array(light_fleet_age_df.iloc[4][1:20].astype(int)), '20+ age group')


    plot_normality(co2_emission_df['Light passenger'], 'Light passenger co2 emssion')
    plot_normality(co2_emission_df['Light commercial'], 'Light commercial co2 emission')

def step_3_1_clean_light_age_distribution(light_fleet_age_df):
    light_fleet_age_df = light_fleet_age_df.T
    light_fleet_age_df.index = [x for x in range(len(light_fleet_age_df.index))]

    numbers = pd.DataFrame(light_fleet_age_df[1:20])
    numbers = numbers.drop(columns=[6])
    numbers.columns = ['0-4 years', '5-9 years', '10-14 years', '15-19 years', '20+ years', 'Total']
    numbers.index = [i for i in range(2000, 2019)]

    percentages = pd.DataFrame(light_fleet_age_df[20:])
    percentages = percentages.drop(columns=5)
    percentages.columns = ['0-4 years percentage', '5-9 years  percentage',
                           '10-14 years percentage', '15-19 years percentage',
                           '20+ years percentage', '15+ years percentage']
    percentages.index = [i for i in range(2000, 2019)]

    new_age_distribution = pd.concat([numbers, percentages], axis=1, join='inner')
    new_age_distribution.insert(0, 'Period', new_age_distribution.index)
    new_age_distribution.index = [i for i in range(len(new_age_distribution.index))]

    return new_age_distribution

def step_3_3_construct_new_distribution_df(nums_columns, percentage_columns, number_fleets_df, new_age_distribution_df):

    # new_table = {'Period':[i for i in range(2000,2019)]} for internal output
    new_table = {}
    for num_column in nums_columns:
        for percenate_column in percentage_columns:
            new_column = new_age_distribution_df[percenate_column] * number_fleets_df[num_column]
            new_column_name = '%s of %s' % (percenate_column[:-11].strip(), num_column[6:].strip())
            new_table[new_column_name] = new_column

    new_age_distribution_df = pd.DataFrame(new_table)

    return new_age_distribution_df

def step_3_5_convert_object_to_int(data_df):
    for column in data_df.columns:
        if data_df.dtypes[column] != np.float64:
            data_df[column] = data_df[column].astype(np.int64)

    return data_df

def step_4_1_LPV_cols(data_df, printed=True):
    default_LPV_cols = ['Period', 'Total LPV new',' Total LPV used', 'Light passenger average age',
                        '0-4 years of LPV new', '5-9 years of LPV new', '10-14 years of LPV new',
                        '15-19 years of LPV new', '20+ years of LPV new', '15+ years of LPV new',
                        '0-4 years of LPV used', '5-9 years of LPV used', '10-14 years of LPV used',
                        '15-19 years of LPV used', '20+ years of LPV used', '15+ years of LPV used', ]

    LPV = data_df[default_LPV_cols]
    pca = PCA(n_components=len(LPV.columns))
    pca.fit(LPV)
    pca_values =pca.explained_variance_ratio_
    if printed:
        print(pca_values)
        print(pca.components_[0:2])
        print(pca_values[0] + pca_values[1])
        get_sort_array_index(pca.components_[0])
        get_sort_array_index(pca.components_[1])

    reduced_LPV_cols = ['Total LPV new', ' Total LPV used', 'Light passenger average age',
                '0-4 years of LPV new', '5-9 years of LPV new', '10-14 years of LPV new',
                '15-19 years of LPV new', '20+ years of LPV new',
                '0-4 years of LPV used', '5-9 years of LPV used', '10-14 years of LPV used',
                '15-19 years of LPV used', '20+ years of LPV used', 'Light passenger']

    return reduced_LPV_cols

def step_4_1_LCV_cols(data_df,printed=True):
    default_LCV_cols = ['Period',  'Total LCV new', ' Total LCV used', 'Light commercial average age',
                        '0-4 years of LCV new', '5-9 years of LCV new', '10-14 years of LCV new',
                        '15-19 years of LCV new', '20+ years of LCV new',
                        '0-4 years of LCV used', '5-9 years of LCV used', '10-14 years of LCV used',
                        '15-19 years of LCV used', '20+ years of LCV used', ]


    LCV = data_df[ default_LCV_cols]

    pca = PCA(n_components=len(LCV.columns))
    pca.fit(LCV)
    pca_values =pca.explained_variance_ratio_
    if printed:
        print(pca_values)
        print(pca.components_[0])
        print(pca_values[0])
        get_sort_array_index(pca.components_[0])

    reduced_LCV_cols = ['Total LCV new', ' Total LCV used', 'Light commercial average age',
                        '0-4 years of LCV new', '5-9 years of LCV new', '10-14 years of LCV new',
                        '15-19 years of LCV new', '20+ years of LCV new',
                        '0-4 years of LCV used', '5-9 years of LCV used', '10-14 years of LCV used',
                        '15-19 years of LCV used', '20+ years of LCV used', 'Light commercial']
    return reduced_LCV_cols

def step_4_2_normalization(data_df,LPV_cols,LCV_cols):
    LPV_df, LCV_df = data_df[LPV_cols],data_df[LCV_cols]
    # LPV_data,LCV_data = normalize( LPV_df, axis=1, norm='l2'),normalize(LCV_df, axis=1, norm='l2')
    # LPV_df, LCV_df = pd.DataFrame(LPV_data, columns= LPV_cols),pd.DataFrame(LCV_data, columns= LCV_cols)
    return LPV_df, LCV_df

def step_5_split_data_add_noisy_data(data_df, test_size):
    noisy_x_row = pd.DataFrame({x: [0.0] for x in data_df.columns[:-1]})
    second_last_row = data_df.iloc[-2]

    X_train, X_test, y_train, y_test = train_test_split(data_df[data_df.columns[:-1]], data_df[data_df.columns[-1]], test_size=test_size)

    X_train, X_test, y_train, y_test =  pd.concat([X_train, noisy_x_row]),pd.concat([X_test, noisy_x_row]), \
                                        y_train.append(pd.Series([0.0])),y_test.append(pd.Series([0.0]))

    X_train, y_train = X_train.append(pd.Series(second_last_row[:-1])), y_train.append(pd.Series(second_last_row[-1]))


    return X_train, X_test, y_train, y_test

def step_6_1_1_conduct_dt_svm_knn(LPV_X_train,LPV_X_test,LPV_y_train, LPV_y_test, LCV_X_train,LCV_X_test,LCV_y_train,LCV_y_test):

    regressors = [DecisionTreeRegressor(), svm.SVR(), KNeighborsRegressor(), ]

    print('LPV')
    for regressor in regressors:
        regressor.fit(LPV_X_train, LPV_y_train)
        print(regressor.score(LPV_X_test, LPV_y_test))
        print('preict values')
        print(regressor.predict(LPV_X_test))

    print('LCV')
    for regressor in regressors:
        regressor.fit(LCV_X_train, LCV_y_train)
        print(regressor.score(LCV_X_test, LCV_y_test))
        print('preict values')
        print(regressor.predict(LCV_X_test))


def step_6_1_2_conduct_linear_nn(LPV_X_train,LPV_X_test,LPV_y_train, LPV_y_test, LCV_X_train,LCV_X_test,LCV_y_train,LCV_y_test):

    regressors = [LinearRegression(), SGDRegressor(), Ridge(),
                  MLPRegressor(activation='logistic', hidden_layer_sizes=(7, ), max_iter=100000)]
    print('LPV')
    for regressor in regressors:
        regressor.fit(LPV_X_train, LPV_y_train)
        print(regressor.score(LPV_X_test, LPV_y_test))
        print('preict values')
        print(regressor.predict(LPV_X_test))

    print('LCV')
    for regressor in regressors:
        regressor.fit(LCV_X_train, LCV_y_train)
        print(regressor.score(LCV_X_test, LCV_y_test))
        print('preict values')
        print(regressor.predict(LCV_X_test))


def step_6_3_tune_parameters(LPV_X_train,LPV_X_test,LPV_y_train,
                               LPV_y_test, LCV_X_train,LCV_X_test,LCV_y_train,LCV_y_test):

    solver_names = ['sag','svd','cholesky','saga','lsqr','sparse_cg']
    for solver_name in solver_names:
        LPV_regressor,LCV_regressor = Ridge(solver=solver_name),Ridge(solver=solver_name)
        LPV_regressor.fit(LPV_X_train, LPV_y_train)
        LCV_regressor.fit(LCV_X_train, LCV_y_train)
        # print(LPV_regressor.predict(LPV_X_test) )
        # print(LCV_regressor.predict(LCV_X_test) )
        print('solver %s, LPV r2 score = %f, LCV r2 score = %f'
              %(solver_name, LPV_regressor.score(LPV_X_test, LPV_y_test),LCV_regressor.score(LCV_X_test, LCV_y_test)))

    regressors = [
        MLPRegressor(activation='logistic', hidden_layer_sizes=(6, 3), max_iter=10000),
                  MLPRegressor(activation='logistic', hidden_layer_sizes=(7, 4), max_iter=10000),
                  MLPRegressor(activation='logistic', hidden_layer_sizes=(6,), max_iter=10000),
                  MLPRegressor(activation='logistic', hidden_layer_sizes=(3,6,), max_iter=10000),
                  MLPRegressor(activation='logistic', hidden_layer_sizes=(7,), max_iter=10000),
                  MLPRegressor(activation='logistic', hidden_layer_sizes=(8,), max_iter=10000),
                  MLPRegressor(activation='logistic', hidden_layer_sizes=(6,1,), max_iter=10000),
                  MLPRegressor(activation='logistic', hidden_layer_sizes=(6,2,), max_iter=10000),
                  MLPRegressor(activation='logistic', hidden_layer_sizes=(6,4,),max_iter=10000),
    ]

    print('LPV')
    for regressor in regressors:
        regressor.fit(LPV_X_train, LPV_y_train)
        print(regressor.score(LPV_X_test, LPV_y_test))
        print('preict values')
        print(regressor.predict(LPV_X_test))

    print('LCV')
    for regressor in regressors:
        regressor.fit(LCV_X_train, LCV_y_train)
        print(regressor.score(LCV_X_test, LCV_y_test))
        print('preict values')
        print(regressor.predict(LCV_X_test))


def step_7_1_prepare(rows, columns):

    test_obj_2 = {x:[] for _,x in enumerate(columns)}
    for row in rows:
        for idx, x in enumerate(columns):
            test_obj_2[x].append(row[idx])

    return pd.DataFrame(test_obj_2)

def step_7_2_build_model(X_train, y_train):
    regressor = Ridge(solver='sag')
    # regressor = Ridge(solver='saga')
    regressor.fit(X_train,y_train)
    return regressor

def regressor_get_score_predicts(regressor, X_test, y_test):

    score,predicts = regressor.score(X_test, y_test), regressor.predict(X_test)
    return score,predicts

def step_7_2_conduct_data_mining(LPV_regressor, LCV_regressor,LPV_X_test, LPV_y_test,
                                 LCV_X_test, LCV_y_test,LPV_2017_obj_2,LCV_2017_obj_2):
    # --- DM objective 1 ---
    LPV_score, LPV_predicts = regressor_get_score_predicts(LPV_regressor, LPV_X_test, LPV_y_test)
    LCV_score, LCV_predicts = regressor_get_score_predicts(LCV_regressor, LCV_X_test, LCV_y_test)


    print('Data Mining Objective One')
    print('LPV R2 score = %f, LCV R2 score = %f'%(LPV_score, LCV_score))
    print('')
    # --- DM objective 2 ---
    print('Data Mining Objective Two')
    LPV_2017_predict,LCV_2017_predict = LPV_regressor.predict(LPV_2017_obj_2), LCV_regressor.predict(LCV_2017_obj_2)
    print('2017 LPV real value = 8.07740664325, sum of predict values %f' % np.sum(LPV_2017_predict[1:]))
    print('2017 LCV real value = 2.47222703164, sum of predict values %f' % np.sum(LCV_2017_predict[1:]))

    return LPV_predicts, LCV_predicts, LPV_2017_predict,LCV_2017_predict

def generate_percentage_list(list):
    total = np.sum(np.abs(list))
    return [abs(x) /total for x in list ]

def step_8_2_visualizaiton(regressor, X_train, y_train, X_test, y_test):
    predict_visualizer = prediction_error(regressor, X_train, y_train, X_test, y_test)
    residual_viz = residuals_plot(regressor, X_train, y_train, X_test, y_test)
    return predict_visualizer,residual_viz

def step_8_2_percentage_viz(percentage_list, columns):
    fig = plt.figure(figsize=(9, 5.0625))
    ax1 = fig.add_subplot(121)

    ratios = percentage_list
    labels = columns
    # rotate so that first wedge is split by the x-axis
    angle = -180 * ratios[0]
    ax1.pie(ratios, autopct='%1.1f%%', startangle=angle, labels=labels, )
    plt.show()

