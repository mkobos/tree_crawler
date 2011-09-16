- in the downloading code, handle 404 errors more gently. Place information that given file was not available due to broken link.
- add more unit tests for different scenarios of algorithm and tree state e.g.:
	- tree with the root only
	- a large tree
	- tree with no missing nodes and without errors
	- root's children are leafs
- in the Unit tests, when the mechanize.Browser opens the "/root/2011-07-02" webpage, the "HTTP Error 404: File not found" error _sometimes_ shows up. The entry in the logs looks as follows: `WARNING thread=="Thread-95", exception in node "/root/2011-07-12": "Moving to child failed". Detailed message: "HTTP Error 404: File not found".`. 
	- probably fault of the HTTP file server?
? change the order of nodes saved in the `*.xml`: order by names not by state

Documentation
-------------
- describe main and root nodes
- description of the program, its construction and construction's philosophy (along with some UML diagrams), advantages and disadvantages
