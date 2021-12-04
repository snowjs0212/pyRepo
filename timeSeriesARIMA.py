# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 22:24:00 2021

@author: KevinJoonsoo
"""
%reset

##### Time Series Analysis
#### Global Packages
import pandas as pd
from itertools import product
import numpy as np

class preProc:
    """
    Data pre-processing
    """
    import pandas as pd
    from itertools import product
    import numpy as np

    def __init__(self, file_path, file_name, pred_begin, zipcode_list = []):
        self.file_path = file_path
        self.file_name = file_name
        self.zipcode_list = zipcode_list
        self.pred_begin = pred_begin
        self.df = []
        self.y = []
        
    def dfSlice(self):
        # Import to python data object
        df_ = pd.read_csv(file_path + file_name)
        # Change datetime data type
        df_.ValDate = pd.to_datetime(df_.ValDate)
        # Slice data set by zipcodes
        df = []
        if len(zipcode_list) == 0:
            df = df_[(df_.ValDate < self.pred_begin)]
        else:
            df = df_[(df_.ValDate < self.pred_begin) &
                    (df_.RegionCode.isin(zipcode_list))]
        self.df = df
        
    def preproc(self):
        df = self.df
        # data pre-proc subset list
        x_region_list = df.RegionCode.drop_duplicates().reset_index(drop=True)
        x_bedrms_list = df.Bdrm.drop_duplicates().reset_index(drop=True)
        # Assign keys: RegionCode (zipcode) & Bdrm (number of bedrooms)
        z = [dict(zip(('RegionCode','Bdrm'), (i, j))) 
             for i, j in product(x_region_list, x_bedrms_list)]
        # y values (Zillow Home Value Index)
        y = [df[['ZHVI']]
             [(df['RegionCode']==list(x.values())[0]) & 
              (df['Bdrm']==list(x.values())[1])].reset_index(drop=True) 
             for x in z]
        self.y = y
        
    def inputData(self):
        return(self.df, self.y)

#### ARIMA Model
### ARIMA function
def func_arima(data, lag = 3):
    """
    ARIMA function
    """
    from statsmodels.tsa.arima.model import ARIMA
        
    model = ARIMA(data, order=(lag, 3, 0))
    model_fit = model.fit()
    yhat = model_fit.predict(len(data), len(data) + lag - 1, typ='levels')
    
    return (yhat)   

#### Running output
def last_day_of_month(date_value):
    from calendar import monthrange
    return (date_value.replace(day = monthrange(date_value.year, date_value.month)[1]))

### Forecast run - individual data obj
def arima_run(item, lag):
    from dateutil.relativedelta import relativedelta
    
    val_date = [last_day_of_month(max(df.ValDate) 
                                  + relativedelta(months = i)
                                  ).strftime('%Y-%m-%d') 
                for i in range(1, lag + 1)]
    
    pred_ = [func_arima(i, lag) for i in y]
    
    pred = [list(z[item].values()), 
            list(zip(list(val_date), list(pred_[item])))]

    return (pred)

### Forecast run - entire sample
class finalOutput():
    """
    Runing the entire process
        : By default, the lag of ARIMA model set to 3
    """
    def __init__(self, lag = 3):
        self.lag = lag
        
    def run(self):
        output_ = []
        output_y_ = []
        output_zip_ = []
        output_bdr_ = []
        # Result calculated in iterations
        for i in list(range(0,len(y))):
            output_.append(arima_run(i, self.lag)) 
            output_y_.append(output_[i][1])
            output_zip_.append([output_[i][0][0]] * self.lag)
            output_bdr_.append([output_[i][0][1]] * self.lag)
        output_y = pd.concat([pd.Series(x) for x in output_y_])
        output_zip = pd.concat([pd.Series(x) for x in output_zip_])
        output_bdr = pd.concat([pd.Series(x) for x in output_bdr_])
        # Return pandas dataframe
        df_y = pd.DataFrame(list(output_y), columns = ['ValDate', 'y_hat'])
        df_zip = pd.DataFrame(list(output_zip), columns = ['RegionCode'])
        df_bdr = pd.DataFrame(list(output_bdr), columns = ['Bdrm'])
        df = pd.concat([df_y, df_zip, df_bdr], axis = 1)
        return(df)

        
### Output Return
## Pre-proce
file_path_ = 'D:/Documents/5_OMSA/5_Spring2021/CSE6242/Project/2_Exploration/'
file_name_ = 'factHomeValue_Short_2019.csv'
pred_begin_ = '3/31/2020'
zipcode_list_ = [30097, 7111]
df_out = preProc(
    file_path = file_path_, file_name = file_name_,/
    pred_begin = pred_begin_, zipcode_list = zipcode_list_).inputData()
y = df_out[1]

## Run - w/ 6 lags
output = finalOutput(6).run()