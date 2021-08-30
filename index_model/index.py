
import datetime as dt
import pandas as pd
import numpy as np
import sys
import os



class IndexModel:
    
    def __init__(self) -> None:
        
        #importing dataset
        data=pd.read_csv("/Users/adamnovak/Desktop/solactive_code_novak/data_sources/stock_prices.csv")
        data.insert(1,"Datetime", self.date_transform(data.iloc[:,0]))
        self.data=data
        
    def date_transform(self, date_array) -> None:
        
        #adding datetime format to dataframe
        dt_dates=np.array([dt.datetime.strptime(date, "%d/%m/%Y").date() for date in date_array])
        return dt_dates

        
    def calc_index_level(self, start_date: dt.date, end_date: dt.date, datetime_column=1) -> None:
        
        #getting first date of calculation and indexes of dates
        if start_date not in self.data.iloc[:,datetime_column].values or end_date not in self.data.iloc[:,datetime_column].values:
            print("Specified dates cannot be found in the data!")
            return

        try:
            calc_date=start_date-dt.timedelta(1)
            calc_ix=self.data.loc[self.data["Datetime"]==calc_date].index[0]
            start_ix=self.data.loc[self.data["Datetime"]==start_date].index[0]
            stop_ix=self.data.loc[self.data["Datetime"]==end_date].index[0]
            
            #creating zip for highest price and respective index
            start_zip=sorted(zip(self.data.iloc[calc_ix, 2:].values,np.arange(2,12)), reverse=True)[:3]
            self.a=start_zip
            
            #extracting stocks with highest market cap
            start_stock=np.array([stock for price,stock in start_zip])
            
            #calculating starting index value
            weights=[0.5,0.25,0.25]
            start_price=self.data.iloc[start_ix, start_stock]
            start_index=np.dot(start_price, weights)
            
            #creating index dataframe
            self.index_dataframe=pd.DataFrame(columns=["Date","Index"])
            self.index_dataframe["Date"]=self.data.iloc[start_ix:stop_ix+1,0].reset_index(drop=True)
            
            #getting data by date
            data_used=self.data.loc[start_ix:stop_ix+1,].reset_index(drop=True)
         
                
            #initializing parameters
            current_month=data_used.iloc[0,datetime_column].month
            current_stock=start_stock
            current_value=start_index
            current_weights=weights
            
            index_values=[]
            
            
            for i in range(data_used.shape[0]):
                if data_used.iloc[i,datetime_column].month == current_month:
        
                    #calculating index value with no rebalancing
                    current_price=data_used.iloc[i,current_stock].values
                    current_value=np.dot(current_price,current_weights)
                    new_index=current_value/start_index
                    index_values.append(new_index*100)
                
                else:
                    
                    #calculating value of current index portfolio
                    current_price=data_used.iloc[i,current_stock]
                    current_value=np.dot(current_price,current_weights)
                    
                    #rebalancing the index
                    new_zip=sorted(zip(data_used.iloc[i-1,2:],np.arange(2,12)), reverse=True)[:3]
                    new_stock=np.array([stock for price,stock in new_zip])
                    new_price=data_used.iloc[i,new_stock]
                    new_weights=np.multiply(weights, (current_value/new_price))
                    index_values.append((current_value/start_index)*100)
                    
                    #setting new parameters
                    current_month=data_used.iloc[i,datetime_column].month
                    current_stock=new_stock
                    current_weights=new_weights
                    
            self.index_dataframe["Index"]=np.array(index_values)
            
        except:
            print("Something went wrong!")
            return 
        
    def export_values(self, file_name: str) -> None:
        self.index_dataframe.to_csv(file_name)





