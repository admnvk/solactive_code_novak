# solactive_code_novak

The solution starts by initializing the dataset and inserting a datetime column in order to easily use timestamps. It then chooses the starting index portfolio based on the prices recorded on 31/12/2019. The chosen stocks and corresponding index value are both recorded for later use.

To calculate the rest of the index values, the code uses a for loop to iterate across all the dates. The code checks if there is a change in the datetime month value at each row. If the month value is the same, then it simply calculates the new index value by using a dot product between chosen stock prices and the specified weights. The calculated index value is appended to an array that will be used in the end to aggregate all the index values. Alternatively, if there is a change in the datetime month value, then the code recalibrates the index portfolio. To do so, it starts out by calculating the current index portfolio value and also by choosing the top performing stocks based on the last closing date of the month before. Then, we basically update the portfolio weights by allocating the specified portfolio distribution (50%, 25%, 25%) according to how large our index portfolio currently is. The index value is recorded and the new weights/parameters are updated for use at the next loop.

In the end, the code creates a csv output based on the created dataframe.
