README FOR test_queries.py

This python file uses the inverted index data structure already formed by the previous component of out code. The files used include
	--( indt.json          --> Format { word  : {docid : tf}} )
	--( indwot.json--> Format { word  : {docid : tf}} )
	--( polt.json          --> Format { docid : {word  : tf}} )
	--( polwot.json      --> Format { docid : {word  : tf}} )
	--( title.json        --> Format { docid : titlename     )

It uses these data structures to calculate the score for each document for a particular user input query.
It provides the user with 4 different options to examine

	1--Examine the working of the normal IR system ( with all modifications )
	2--Examine the champion list modification
	3--Examine the title term inclusion modification
	4--Examine the query term overlap modification

It takes the user input as to what they want to examine
It will then take query from the user( prefer not to include any punctuation ) over which the code will run
It is programmed to show the user top 10 relevant documents if there are atleast 10 documents that have terms that match with query words.

How to run the test_queries.py file:
	
	1)First make sure that all the 5 files mentioned above are present in the same folder as of test_queries.py
	2)You will need a default python/python3 terminal
	3)Open the test_queries.py file using the python terminal.
	4)For some reason after taking both the inputs the code does not seem to work for the very first time( it autoejects)
	5)If point 4 happens then open the file again using the python terminal.
	6)This time it will work very fine
	7)The code has a while(True) statement which allows the user to examine different modifications of our IR system one after the other
	8)If at anytime you want to come out of the loop just press Ctrl + C and you will be ejected 