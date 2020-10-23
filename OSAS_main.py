import random
import os
from help_methods import *

# hyper parameters
# pd.set_option('display.max_columns', None)
pd.set_option('display.precision',12)

SEED = 722
# SEED = 123
random.seed(SEED)
np.random.seed(SEED)

split_2017_LPV_rows = [[1.59009400e+06, 1.61762700e+06, 1.43115413e+01, 2.84522000e+05, 2.54697000e+05,
                        4.53646000e+05, 2.51078000e+05, 3.46148000e+05, 2.89449000e+05, 2.59108000e+05,
                        4.61501000e+05, 2.55426000e+05, 3.52141000e+05],
                       [284522.0, 0.0, 2.975101564, 284522.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       [254697.0, 0.0, 7.975101564, 0.0, 254697.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       [453646.0, 0.0, 12.97510156, 0.0, 0.0, 453646.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       [251078.0, 0.0, 17.97510156, 0.0, 0.0, 0.0, 251078.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       [346148.0, 0.0, 22.97510156, 0.0, 0.0, 0.0, 0.0, 346148.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       [0.0, 289449.0, 9.130000000, 0.0, 0.0, 0.0, 0.0, 0.0, 289449.0, 0.0, 0.0, 0.0, 0.0],
                       [0.0, 259108.0, 14.13000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 259108.0, 0.0, 0.0, 0.0],
                       [0.0, 461501.0, 19.13000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 461501.0, 0.0, 0.0],
                       [0.0, 255426.0, 24.13000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 255426.0, 0.0],
                       [0.0, 352141.0, 29.13000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 352141.0], ]

split_2017_LCV_rows = [[4.76173000e+05, 1.06367000e+05, 1.25145441e+01, 8.52030000e+04, 7.62720000e+04,
                        1.35849000e+05, 7.51880000e+04, 1.03658000e+05, 1.90320000e+04, 1.70370000e+04,
                        3.03460000e+04, 1.67950000e+04, 2.31550000e+04],
                       [085203.0, 0.0, 2.868356783, 085203.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       [076272.0, 0.0, 7.868356783, 0.0, 076272.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       [135849.0, 0.0, 12.86835678, 0.0, 0.0, 135849.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       [075188.0, 0.0, 17.86835678, 0.0, 0.0, 0.0, 075188.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       [103658.0, 0.0, 22.86835678, 0.0, 0.0, 0.0, 0.0, 103658.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       [0.0, 019032.0, 07.98000000, 0.0, 0.0, 0.0, 0.0, 0.0, 019032.0, 0.0, 0.0, 0.0, 0.0],
                       [0.0, 017037.0, 12.98000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 017037.0, 0.0, 0.0, 0.0],
                       [0.0, 030346.0, 17.98000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 030346.0, 0.0, 0.0],
                       [0.0, 016795.0, 22.98000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 016795.0, 0.0],
                       [0.0, 023155.0, 27.98000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 023155.0], ]


if __name__ == '__main__':
    # ---- step 1 ----
    file_dir = os.path.join('./','NZ-Vehicle-Fleet-Statistics-2018_web.xlsx')

    # ---- step 2.1 2.2 ----
    number_fleets_df = load_average_vehicle(file_dir)
    light_fleet_age_df = load_light_fleet_age(file_dir)
    co2_emission_df = load_co2_emission(file_dir)

    # ---- step 2.3 ----
    # print(number_fleets_df)
    # print(light_fleet_age_df)
    # print(co2_emission_df)

    # ---- step 2.4.1 ----
    co2_emission_df = step_2_4_1_imputation_co2_emission_df(co2_emission_df)

    # ---- step 2.4.2 ----
    # step_2_4_2_check_normality(number_fleets_df, light_fleet_age_df, co2_emission_df)

    # ---- step 3.1 ----
    num_fleets_select_cols = ['Period', 'Total light new', 'Total light used import', 'Total LPV new',
                              ' Total LPV used', 'Total LCV new', ' Total LCV used', 'Light passenger NZ new',
                              'Light passenger used import', 'Light commercial NZ New',
                              'Light commercial used import', 'Light fleet average age', 'Light passenger average age',
                              'Light commercial average age', 'Light used average age', 'NZ new light average age']

    co2_select_cols = ['Light passenger', 'Light commercial']

    new_age_distribution_df = step_3_1_clean_light_age_distribution(light_fleet_age_df)

    # ---- step 3.2 ----
    num_fleets_select_cols = ['Period', 'Total LPV new', ' Total LPV used', 'Total LCV new', ' Total LCV used',
                              'Light passenger average age', 'Light commercial average age']

    percentage_columns = ['0-4 years percentage', '5-9 years  percentage','10-14 years percentage',
                         '15-19 years percentage', '20+ years percentage', '15+ years percentage']

    # ---- step 3.3 ----
    nums_columns = ['Total LPV new', ' Total LPV used', 'Total LCV new', ' Total LCV used']
    new_age_distribution_df = step_3_3_construct_new_distribution_df(nums_columns, percentage_columns,
                                                                     number_fleets_df, new_age_distribution_df)

    # ---- step 3.4 ----
    cleaned_data_df = pd.concat([number_fleets_df[num_fleets_select_cols], new_age_distribution_df,co2_emission_df[co2_select_cols]], axis=1)
    # print(cleaned_data_df)

    # ---- step 3.5 ----
    # print(cleaned_data_df.dtypes)
    cleaned_data_df = step_3_5_convert_object_to_int(cleaned_data_df)
    # print('')
    # print(cleaned_data_df.dtypes)

    # ---- step 4.1 ----
    reduced_LPV_cols = step_4_1_LPV_cols(cleaned_data_df,printed= False)
    # print(reduced_LPV_cols)
    reduced_LCV_cols = step_4_1_LCV_cols(cleaned_data_df, printed = False)

    # ---- step 4.2 ----
    LPV_df, LCV_df = step_4_2_normalization(cleaned_data_df,reduced_LPV_cols,reduced_LCV_cols)

    # ---- step 5 ----
    LPV_X_train, LPV_X_test, LPV_y_train, LPV_y_test = step_5_split_data_add_noisy_data(LPV_df, test_size=0.3)
    LCV_X_train, LCV_X_test, LCV_y_train, LCV_y_test = step_5_split_data_add_noisy_data(LCV_df, test_size=0.3)

    # ---- step 6.1 6.2 ----

    # step_6_1_1_conduct_dt_svm_knn(LPV_X_train, LPV_X_test, LPV_y_train, LPV_y_test,
    #                               LCV_X_train, LCV_X_test, LCV_y_train, LCV_y_test)
    #
    # step_6_1_2_conduct_linear_nn(LPV_X_train, LPV_X_test, LPV_y_train, LPV_y_test,
    #                               LCV_X_train, LCV_X_test, LCV_y_train, LCV_y_test)

    # ---- step 6.3 ----
    # step_6_3_tune_parameters(LPV_X_train, LPV_X_test, LPV_y_train, LPV_y_test,
    #                               LCV_X_train, LCV_X_test, LCV_y_train, LCV_y_test)

    # ---- step 7.1 ----
    LPV_2017_obj_2, LCV_2017_obj_2 = step_7_1_prepare(split_2017_LPV_rows,LPV_df.columns[:-1]),\
                                     step_7_1_prepare(split_2017_LCV_rows,LCV_df.columns[:-1])


    # ---- step 7.2 ----
    # --- build DM models ---
    LPV_regressor, LCV_regressor = step_7_2_build_model( LPV_X_train, LPV_y_train),\
                                  step_7_2_build_model( LCV_X_train, LCV_y_train)
    # --- run predicts ---
    LPV_predicts, LCV_predicts, LPV_2017_predict, LCV_2017_predict = step_7_2_conduct_data_mining(LPV_regressor, LCV_regressor,
                                                                                                  LPV_X_test, LPV_y_test,
                                                                                                  LCV_X_test, LCV_y_test,
                                                                                                  LPV_2017_obj_2,LCV_2017_obj_2)

    # ---- step 7.3 ----
    print('')
    print('Data Mining Objective One result discover, LPV')
    for idx,y_real_value in enumerate(LPV_y_test):
        year = cleaned_data_df['Period'][LPV_X_test.index[idx]]
        print('%i year, real value = %f, predict value = %f' %(year, y_real_value, LPV_predicts[idx]))
    print('')
    print('Data Mining Objective One result discover, LCV')
    for idx,y_real_value in enumerate(LCV_y_test):
        year = cleaned_data_df['Period'][LCV_X_test.index[idx]]
        print('%i year, real value = %f, predict value = %f' %(year, y_real_value, LCV_predicts[idx]))

    print('')
    print('Data Mining Objective TWO result discover, 2017 LPV')
    for idx,single_age_group_value in enumerate(LPV_2017_predict):
        print('%s : %f '%(LPV_2017_obj_2.columns[2:][idx], np.abs(single_age_group_value)  ))
    print('')
    print('Data Mining Objective TWO result discover, 2017 LCV')
    for idx,single_age_group_value in enumerate(LCV_2017_predict):
        print('%s : %f '%(LCV_2017_obj_2.columns[2:][idx], np.abs(single_age_group_value)  ))

    # ---- step 8.1 ----
    print('')
    print('LPV Percentage')
    LPV_obj_2_percentage_list = generate_percentage_list(LPV_2017_predict[1:])
    for idx,percentage in enumerate(LPV_obj_2_percentage_list):
        col_name = LPV_2017_obj_2.columns[3:][idx]
        num_fleets = LPV_df.iloc[-2][col_name]
        print('%23s: # of fleets: %i, co2 percentage: %.4f%%'%(col_name,num_fleets,percentage*100))

    print('')
    print('LCV Percentage')
    LCV_obj_2_percentage_list = generate_percentage_list(LCV_2017_predict[1:])
    for idx,percentage in enumerate(LCV_obj_2_percentage_list):
        col_name = LCV_2017_obj_2.columns[3:][idx]
        num_fleets = LCV_df.iloc[-2][col_name]
        print('%23s: # of fleets: %i, co2 percentage: %.4f%%'%(col_name,num_fleets,percentage*100))

    print('sum of used new')

    # ---- step 8.2 ----

    LPV_predict_visualizer,LPV_residual_viz = step_8_2_visualizaiton(LPV_regressor, LPV_X_train, LPV_y_train,
                                                                     LPV_X_test, LPV_y_test)
    LCV_predict_visualizer, LCV_residual_viz = step_8_2_visualizaiton(LCV_regressor, LCV_X_train, LCV_y_train,
                                                                      LCV_X_test, LCV_y_test)

    LPV_pie = step_8_2_percentage_viz(LPV_obj_2_percentage_list, LPV_2017_obj_2.columns[3:])
    LCV_pie = step_8_2_percentage_viz(LCV_obj_2_percentage_list,LCV_2017_obj_2.columns[3:])


    # ---- step 8.5 ----
    # set different seed
    # set saga solver


