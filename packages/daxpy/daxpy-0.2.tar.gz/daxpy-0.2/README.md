# daxpy

A pre-machine-learning model package.

Package is consisted of following features:

	module checker (check_modules): ensures if necessary modules are installed in the environment.

	library importer (import_libraries) : imports required libraries.

	file reader (read_files): reads or reloads all csv, excel and pickle files given path.

	dataset describers (col_stats, df_cols): describes dataset's information.

	column summarizers (cat_sum, num_sum, col_sum): gives specific informations about columns.

Installation:

```
pip install daxpy
```

Usage:

```
from daxpy import analyzer

display_ = True 		# Displays the calculated tables.
plot_    = True 		# Plots related data given function.
data     = '../data/' 	# Directory where csv, excel and pickle data is loaded or pd.DataFrame() object.
sep_     = ',' 			# Seperator for csvs.


# Field belov should be run if the pickle files have not been created before. Otherwise next cell can be run to save some time.

mp = analyzer(display_=True, plot_=True, data=data, sep_='|')
mp.rename_dfs({'data1_111':'data_1','data2_1231': 'data2'})
mp.save_dfs('./data')


# Field below can be run after the pickle files are created. (can be run repeatedely)

mp = analyzer(data='./', plot_=True, display_=True)


mp.head_tail(mp.data1);

col_stats = mp.col_stats(mp.data1, display=False)

id_cols, date_cols, num_cols, cat_cols, cat_but_car_cols, num_but_cat_cols, num_but_cat_but_car_cols = mp.df_cols(mp.data1, display_=True, cat_th=32, car_th=10)

# Plot all columns' summary
for cat_col in cat_but_car_cols:
    mp.cat_summ(mp.data1, cat_col, threshold=0.01);
for cat_col in cat_cols:
    mp.cat_summ(mp.data1, cat_col, threshold=False);
# Analyze num_cols
for num_col in num_cols:
    mp.num_summ(mp.data1, num_col)

```