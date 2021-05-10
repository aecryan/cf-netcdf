# Creating a CF-compliant netCDF file with the Python netCDF4 library

Using the demo-nc.py script, you can create a netCDF file that conforms to CF conventions. To change the data used to create the file, edit the sections in the script. Executing the script via the terminal using `python demo-nc.py` will create a CF-compliant netCDF file, demo.nc. 

NCO programs are recommended to view the data and metadata associated with this file and to understand how to make changes to suit your project. Installation instructions can be found here: http://nco.sourceforge.net/

The ncdump and ncks programs are especially useful to view metadata headings (`ncdump -h <filename.nc>`) and values per variable (`ncks -v <variable_name <filename.nc>`).

## Create a virtual environment

If not already installed, first install virtualenv: `pip install virtualenv`. 

Navigate to the root repository folder and create a new virtual environment called 'nc'. 

On macOS and Linux:

`python3 -m venv nc`

On Windows:

`py -m venv nc`

## Activate the virtual environment

On macOS and Linux:

`source nc/bin/activate`

On Windows:

`.\nc\Scripts\activate`

## Install dependencies from requirements.txt

`pip install -r requirements.txt`

## Create netCDF file

`python demo-nc.py`
