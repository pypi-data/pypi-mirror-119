# Webscraping Project

## Predicting the Band Gap of Compounds using Elemental Descriptors

## Abstract

It has been shown that there is a predictive relationship
between 'known discrete scalar descriptors associated with crystal and electronic structure and observed properties of materials'.
However, the property space of these materials is of high dimensionality which highlights the complex nature of predictive models at the fundamental level. Additionally, the elemental descriptors at this level have a certain degree of co-dependence which makes prediction even more complicated. It has been demonstrated using data reduction methods that the property space of observable material properties can be diminished.  In this project, a dataset of elements and some of their corresponding elemental descriptors have been collected using webscraping techniques. The elemental descriptors/features were limited to five since it has been shown that it is possible to predict band gap energies using only five (5) elemental descriptors.

## Motivation

Recent advances in material science and engineering have been focused on 
producing rational design rules and principles for material fabrication.
The development of these design rules have huge implications for various fields such as crystal engineering, opto-electronics and photonics . In this regard, considerable attempts have been made to utilize already accumulated datasets to create models that facilitate the prediction of various material properties using machine learning techniques. Despite recent advances in this field, there is a dearth of machine-learning-based models to predict band gap energies.

## Methodology

Implementing python libraries such as selenium and pandas, a database of elements with elemental descriptors have been extracted. The code was written to function in a multifaceted way as detailed below:

* Open the desired website containing information on the elements or compound.

* Extract specific information on the attributes of the element or compound.
    * To do this, the python codes ```OQMD_new_version.py``` and ```periodic_table_new.py``` utilized. Within this code, a scraper class has been defined with the following attributes:
    * `n` whose definition depends on the code being executed. For ```OQMD_new_version```, `n` is
    an integer that defines the number of pages to extract data from while `n` in ```periodic_table_new.py``` defines the number of elements to extract data from. In this case data from 60 elements where extracted.
    * `root` defines the target url where data is being extracted.
    * `features` initialises a dictionary with keys that define the necessary data to be extrach for ecah element or compound.
    It takes either of these forms: ```features = {'Element_Name':[], 'Atomic_Number':[], 'Electronegativity':[], 'Boiling_Point':[]}``` or
    ```features = {'Name':[], 'Spacegroup':[], 'Volume':[], 'Band_gap':[]}```

     These codes contain the function ```extract_data()```  that carry out the extraction of elements and compounds data.
    * Specifically, ```extract_data(to_DF)``` depends on ```to_DF``` which only accepts boolean values. to_DF determines whether or not the data will be converted into a Data Frame.

* Convert the result into a dataframe for further processing us
    * Using Pandas, the extracted data was stored as a data frame using the ```convert_to_DF()``` function which depends on the following variables: ```data_name```, ```file_out```, ```to_csv```.

* Clean the data

    * For the extracted elements data, the boiling point of  elements was extracted in both &deg;C and Kelvin(K) with the boiling point in &deg;C within parentheses. For consistency, we delete all values in parentheses leaving values in K. To do this, we import the module ```regex``` and implement the following code :

         ```re.sub(r'\([^)]*\)', '', '[filename]')``` 

* Import as an SQL database
    * Implementing the python modules ```psycopg2``` and ```SQLAlchemy``` , the output data was imported to SQL in     tabular form. 

Specifically, the main python library used for the extraction of data was selenium. Pandas was used to convert the raw data into a desired output (i.e. a csv file).

## Setting up venv

* Using anaconda3 set up a virtual environment (venv) while meeting necessary code requirements. All necessary requirements can be found in the file ```requirements.txt```. 

    ```source activate [env name]```

    ```pip install requirements.txt```

# Installing and Running
* To install this package:

    ```pip install el-compX-scraper```

## Running the Project

1. Within python import the necessary modules:

    ``` 
        import scraper
        from scaper.OQMD_new_version import Compound_Scraper
        from scraper.periodic_table_new import PeriodicTableScraper 
    ```  

2. To instantiate a scraper object, we can implement the CompoundScraper class. Hence,
    ```
    root = "http://oqmd.org/api/search#apisearchresult"
    features = {'Name':[], 'Spacegroup':[], 'Volume':[], 'Band_gap':[]}
    scraper = CompoundScraper(n=1, root=root, list=[], features=features)
    scraper.extract_data()

    ```
    Similarly for the PeriodicTableScraper,
    ```
    root = "https://pubchem.ncbi.nlm.nih.gov/periodic-table/#view=list"
    features = {'Element_Name':[], 'Atomic_Number':[], 'Electronegativity':[], 'Boiling_Point':[]}
    scraper = PeriodicTableScraper(n=5, root=root, list=[], features=features)
    scraper.extract_data(to_DF=True)
    ```
3. We can also example script which instantiates specific scraper objects depending on the url. Thus to execute this,

    ```import scraper.example```









