# Data Collector
## By Query
To get the papers data by search query, you can use the following python script, 
```
from datacollector import datacollector_query
python datacollector_query.py SearchQuery NumberOfResults Download?(yes/no)
```
In this script, it takes 3 arguments.
* Search Query (Non-empty String)
* Number of results (Integer)
* Download PDF file? (yes/no)

NOTE: For the search query, it must be a non-empty String, and if you want more than one query, using + symbol between two words (Ex. word1+word2).
This script will 
* Search for the query at the PubMed repository
* Format the result as JSON format
* Name the JSON with paper’s id (Ex. 1234.json)

The JSON file will contain the metadata of the paper
* pmid
* authors
* year
* title
* abstract
* references
* citedby

If you type yes for the third argument, it also will download the paper with pdf format into the pdf directory from a repository HERE.
NOTE: Some of the paper might be downloaded. The reason I have found is first the repository doesn’t have it. Second, the paper hasn't been published yet because it’s too new.
## By PMIDs
To get the papers data by list of ids, you can use the following python script, 
```
python datacollector_id.py FilePath Download?(yes/no)
```
In this script, it takes 2 arguments.
* File path (TXT format)
* Download PDF file? (yes/no)

This script will do the same things as ABOVE.
NOTE: For the TXT file, you must separate those pmids with a new line character (“\n”).