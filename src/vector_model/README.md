Generalised Vector Space Model
==============================

**Information Retrieval Project for Demonstration of Generalised Vector Space Model**

**Note:** This project was implemented as a final assignment for CSF469 Information Retrieval at BITS Pilani K.K. Birla Goa Campus.

**GVSM Paper:**http://www.aclweb.org/anthology/E09-3009

**Required environment**  
1. Python v3.0  
2. Scikit Learn Machine Learning Library http://scikit-learn.org/

**Contributors:**  
Kunal Baweja 2011A7PS029G  
Saransh Varshneya 2011A7PS007G  
Nasrin Jaleel 2011A7PS444G  
Ashu Kalra 2011A7PS150G  

**Guidelines/Instructions to run the demo code:**

1. `test_large` folder contains 3000 documents and `test_small` folder contains the small 5 files data set
2. Execute `python IR_small.py` for checking output on a small dataset of 5-10 documents. Please enter the path to files to be ranked in the format
   `/path/to/current_folder/test_small/*` and the path to query document as `/path/to/current_folder/query.txt`
3. Execute `python IR_large.py` for checking output on large dataset of documents. Please enter the path to files to be ranked in the format
   `/path/to/current_folder/test_large/*`. **Here by default the first document read by the code is treated as the query document.**

**Note:** The code may be tested on other datasets too provided the paths mentioned above are provided correctly by the user when prompted by the script.
