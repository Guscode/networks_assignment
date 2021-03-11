# Networks Assignment

Here you'll find my solution to Assignment 4 in language analytics. 
- Your script should be able to be run from the command line
- It should take any weighted edgelist as an input, providing that edgelist is saved as a CSV with the column headers "nodeA", "nodeB"
- For any given weighted edgelist given as an input, your script should be used to create a network visualization, which will be saved in a folder called viz.
- It should also create a data frame showing the degree, betweenness, and eigenvector centrality for each node. It should save this as a CSV in a folder called output.


In order to try the code, run this line to clone the directory and change directory to the folder.
```
git clone https://github.com/Guscode/networks_assignment.git
cd networks_assignment
```

Then create and open the virtual environment lang_ass
```
bash ./create_lang_ass.sh #create virtual environment
source ./lang_ass/bin/activate #activate lang_ass
```

In the virtual environment you can run networks.py on edgelist.csv or any other edgelist dataframe with a 'nodeA' and 'nodeB' column
Here you specify the file with -p and weight threshold with -t
```
python networks.py -p edgelist.py -t 500
```

have fun be yourself
