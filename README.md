## Rough Draft

This is a very rough draft of my first project to build system to scrape and display diagnostics for the BL systems across many networks.

At the following link you can find my first attempt at creating the data and creating a basic DAG UI.  
 

### How this works
A previous volunteer made a few scripts and a few programs to run on the head node. The head node would ssh into every computer on the network and run commands that would then be parsed into YAML files.

These YAML files were far from perfect but I tried to make them work. After heavy processing I created two products:
* One massive CVS was created, containing a ton of information (Network, System, Type, Make,Model, Capacity/Speed, S/N, Other) for every node (e.g. computer) and component (i.e. GPU, CPU, disk etc.)
* A JSON file that represents the network as a DAG. This JSON is then used by D3.

After parsing, the data is called by the [csv-to-html-table](http://derekeder.github.io/csv-to-html-table/) javascirpt and a tree UI that I made with D3.

### Moving forward
After discussion with Andrew and David, we decided the next iteration should:
* Have scripts totally written by me.
* Be color coded
* Be much more detailed
Now I'm going back to the drawing board to rewrite the scraping scripts. 

