# Ftsa
Ftsa is a package for the clustering of financial time series data with the realized volatility allowed for. This work provides a method to cluster daily financial time series. The objective is to find transaction dates with unusual financial behaviors or large volatility.

The clustering consists of 2 stages. 

Stage 1: The clustering based on the shape of time series. This stage can be viewed as a normal clustering for the time series data.

Stage 2: The clustering based on the realized volatility. For each cluster found in the first stage, the algorithm will further divide the series within it to different groups according to the realized volatility. 

As a result, the final partition is conducted with both the shape and the volatility of the series taken into consideration.

## How to use Ftsa
### 1. Import the package
```
from Ftsa import ftsworker
```

### 2. Initialize a Ftsa worker. 

The following example shows the necessary parameters: 

* The path of the data (CSV file); 

* A dictionary that specifies the column name of the time and that of the corresponding value. In this case, the column names are 'Date' and 'Close', respectively.
```
worker = ftsworker.worker('SH000001.csv', 
	{
	'time':'Date', 
	'val':'Close'
	})
```

### 3. Load the data.
```
df = worker.load()
```

### 4. Conduct the clustering.

The parameters are:

* The first parameter refers to the data, i.e., the loaded dataframe.

* h: The window size for the smooth function. Default: 5.

* K: The number of clusters in the first stage. Default: 2.

* rv_K: The number of clusters in the second stage. Default: 2.

* op: Whether to output dendrograms. 1 - output; 0 - not output. Default: 0.

* mop: Whether to implement the second stage. If mop is set to 1, it will conduct the 2 stages. If mop is set to 0, it will only conduct first stage, the clustering based on the shape of the time series. Default: 1.
```
label = worker.cluster(df, K=3, rv_K=2, mop=1, op=0, h=5)
```

The output label shows the final partition for all daily time series. The following example display the format of the output. A dictionary is provided to describe the partition. Each date refers to a daily time series.
```
{
	'changepoint cluster 1': 
		{
			'RV cluster 1': ['2015-01-01', '2015-03-02', ...],
			'RV cluster 2': ['2015-06-30', ...]
		},
	'changepoint cluster 2': 
		{
			'RV cluster 1': ['2015-10-11', '2015-10-12', ...],
			'RV cluster 2': ['2015-12-01', ...]
		}
	...
}
```
