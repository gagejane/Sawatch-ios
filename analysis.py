import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
# import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
# from statsmodels.stats.diagnostic import het_goldfeldquandt
from statsmodels.stats.outliers_influence import variance_inflation_factor


def scatter(df):
    scatter_matrix(vars, alpha=0.2, figsize=(12,12), diagonal='hist')
    plt.tight_layout()
    plt.show()
    # plt.savefig('images/scatmatrix')

def bar_weather(df):
    grouped = df.groupby(['weather_type'])['fuel_used'].mean()
    grouped.plot.bar()
    plt.xticks(rotation=50, horizontalalignment='right')
    plt.xlabel('Bad Weather', weight='bold')
    plt.ylabel('Liters of Fuel Used', weight='bold')
    plt.title('Liters of Fuel Used by Weather Type', weight='bold', fontsize=15)
    plt.tight_layout()
    plt.show()
    # plt.savefig('images/bad_weath')

def bar_veh(df):
    grouped = df.groupby(['type'])['fuel_used'].mean()
    grouped.plot.bar()
    plt.xticks(rotation = 50, horizontalalignment='right')
    plt.xlabel('Vehicle Type', weight='bold')
    plt.ylabel('Liters of Fuel Used', weight='bold')
    plt.title('Fuel used per Liter by Vehicle Type', weight='bold', fontsize=15)
    plt.tight_layout()
    plt.show()
    # plt.savefig('images/type')

def clean(X):
    #turn booleans into integers
    X = X.applymap(lambda x: 1 if x == True else x)
    X = X.applymap(lambda x: 0 if x == False else x)
    #turn weather_type and thpe into binary variables, drop mist so that it is reference group
    X = pd.get_dummies(X, columns=['weather_type'])
    X.drop(['weather_type_Good'], axis=1, inplace=True)
    X = pd.get_dummies(X, columns=['type'])
    X.drop(['type_Sedan'], axis=1, inplace=True)
    return X

def linear_train(X_train, y_train):
    X_train = sm.add_constant(X_train)
    result_train = sm.OLS(y_train,X_train).fit()
    print('TRAINING MODEL')
    print(result_train.summary())
    return result_train

def linear_test(X_test, y_test):
    X_test = sm.add_constant(X_test)
    result_test = sm.OLS(y_test,X_test).fit()
    print('TESTING MODEL')
    print(result_test.summary())

def QQ(result):
    resid_stud = result.outlier_test()['student_resid']
    dev_null = sm.graphics.qqplot(resid_stud, line='45', fit=True)
    plt.title('Q-Q plot for Testing Model', weight='bold', fontsize=15)
    plt.show()
    # plt.savefig('images/QQ_Training')

def heteroscedasticity(result):
    print('Goldfeld-quandt test returns: F stat, p-value:')
    print(het_goldfeldquandt(result.resid, result.model.exog))
    plt.scatter(result.fittedvalues, result.resid)
    plt.title('Scatterplot of Residuals for Model 1', weight='bold', fontsize=15)
    plt.xlabel('Predicted Values', weight='bold')
    plt.ylabel('Residuals', weight='bold')
    plt.tight_layout()
    plt.title('Scatterplot of Residuals for Training Model', weight='bold', fontsize=15)
    # plt.show()
    plt.savefig('images/Resids_Training')

def VIF(X_train):
    #from https://www.kaggle.com/ffisegydd/sklearn-multicollinearity-class
    print('VIF:')
    variables = X_train.columns
    vif = [variance_inflation_factor(X_train[variables].values, X_train.columns.get_loc(var)) for var in X_train.columns]
    zipped = list(zip(variables, vif))
    print(zipped)
    # create heatmap of correlations between features
    # corr_df = X_train.corr(method='pearson')
    # mask = np.zeros_like(corr_df)
    # mask[np.triu_indices_from(mask)] = True
    # sns.heatmap(corr_df, cmap='RdYlGn_r', vmax=1.0, mask=mask, linewidth=2.5)
    # plt.yticks(rotation=0)
    # plt.xticks(rotation=90)
    # plt.title('Correlations Among Features for Testing Model', weight='bold', fontsize=15)
    # # plt.title('Correlations Among Features for Model 2', weight='bold', fontsize=15)
    # plt.tight_layout()
    # plt.show()

if __name__ == '__main__':
    # df = pd.read_excel('data/ios_telemetry.xlsx', index_col='id')
    # df.to_csv('data/ios_telemetry.csv')
    df = pd.read_csv('data/ios_telemetry.csv', index_col='id')
    pd.options.display.max_columns = 200

    #all values for rfd (ready for deletion) are False, so keep all
    #hard_brake is 100% False
    #Weather: coding 'Not Reported' as missing
    df['weather'].replace(to_replace=['Not Reported'],value=np.NaN, inplace=True)
    weather_dict = {'broken clouds':'Bad', 'clear sky': 'Good', 'few clouds':'Good', 'mist':'Bad', 'overcast clouds':'Bad'}
    df['weather_type'] = df['weather'].replace(weather_dict)
    #kmph: coding 0 as missing
    # df['kmph'].replace(to_replace=0,value=np.NaN, inplace=True)
    df['fuel_used'].replace(to_replace=0, value=np.NaN, inplace=True)

    #Recod vehicle_id with vehicle info
    model_dict = {3272:'2002 Mitsubishi Lancer', 18338:'2015 Chrysler ', 20478:'2017 BMW 530i', 14345:'2012 Jeep Grand Cherokee 4WD', 19599:'2016 Ford ESCAPE FWD'}
    type_dict = {3272:'Sedan', 18338:'Sedan', 20478:'Sedan', 14345:'SUV', 19599:'SUV'}
    df['vehicle_id_name'] = df['vehicle_id'].replace(model_dict)
    df['type'] = df['vehicle_id'].replace(type_dict)

    df.dropna(inplace = True)

    '''EDA'''
    vars = df[['fuel_used', 'kmph', 'celsius', 'altitude_delta', 'g_force', 'kml', 'kilometers']]
    # print(scatter(vars))
    # print(bar_weather(df))
    # print(bar_veh(df))

    '''Linear regression'''
    #dfs for linear regression
    X = df[['kmph', 'celsius', 'altitude_delta', 'g_force', 'kml', 'weather_type', 'type']]
    y = df[['fuel_used']]

    #Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    #Testing regression assumptions
    print(VIF(clean(X_train)))
    print(QQ(linear_train(clean(X_train), y_train)))
    print(heteroscedasticity(linear_train(clean(X_train), y_train)))

    #Run model on test data
    print(linear_test(clean(X_test), y_test))
