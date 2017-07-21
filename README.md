# cclib web repository

Web platform to parse data from chemistry logfiles using [cclib](https://github.com/cclib/cclib)


## Setup

### With Docker

* Install Docker and docker-compose on your machine  
* Clone this repository  
  ```bash
  git clone https://github.com/nitish6174/cclib-web
  ```
* Setup the docker environment file
  ```bash
  cp .env.example .env
  ```
  Set ```SETUP_DB``` as ```1``` to seed database with parsed files else set ```0```  
  ```DATA_FOLDER_PATH``` is the local path to the directory of log files which will be parsed and inserted in dockerized image's database if ```SETUP_DB``` is ```1```  
  Setting ```PRODUCTION``` to ```0``` runs flaskapp in ```debug``` mode
* Build the Docker setup and run it 
  ```bash
  sudo docker-compose build
  sudo docker-compose up
  ```  
* The flask application can now be accessed in browser at ```localhost:5000```


### Using python virtual environment

**Note** : Use Python 3. [OpenBabel](http://openbabel.org/docs/current/) setup is not added in the below steps.

Below instructions are given for ubuntu

* Install python pip and virtualenv  
  ```bash
  sudo apt-get install python3 python3-pip
  pip3 install virtualenv
  ```  
* Install MongoDB and start MongoDB server  
  ```bash
  sudo apt-get install mongo
  sudo service mongodb start
  ```  
* Clone repository and setup virtualenv for project  
  ```bash
  git clone https://github.com/nitish6174/cclib-web.git
  cd cclib-web
  virtualenv -p python3 venv_py3
  ```  
* Download [cclib](https://github.com/cclib/cclib) repository inside the ```cclib-web``` folder:  
  ```bash
  git clone https://github.com/cclib/cclib.git
  ```  
* Install pip dependencies and build cclib inside virtual environment  
  ```bash
  source venv_py3/bin/activate
  pip3 install -r requirements.txt
  cd cclib
  python3 setup.py build
  python3 setup.py install
  ```  
* Running :  
  * Go to ```cclib-web``` directory (root of repo) and make sure virtualenv is activated.  
    (Run ```source venv_py3/bin/activate``` to enter virtual environment)
  * Run ```python run.py <SETUP_DB> <PRODUCTION> <DATA_FOLDER_PATH>``` with suitable arguments:  
    - ```SETUP_DB``` : Set as ```1``` to seed database with parsed files else set ```0```  
    - ```PRODUCTION``` : Setting to ```0``` runs flaskapp in ```debug``` mode  
    - ```DATA_FOLDER_PATH``` : Path to the directory containing log files which will be parsed and inserted in host machine's MongoDB database (provided ```SETUP_DB``` is ```1```)  
    **Note** : All the 3 arguments are optional
  * Then, flask server will start on the machine at port 5000.  
  * The application can now be accessed in browser at ```localhost:5000```
  * Stop flask server with ```Ctrl-C``` and deactivate virtualenv using ```deactivate``` command


## Available functionality

Details can be found in the [TODO list](https://github.com/nitish6174/cclib-web/issues/1)

Here are the features available in web front-end as of now:

* Any computational chemistry log file (of format supported by cclib) can be uploaded on the webpage to view the parsed data from it
* Also, if atom coordinates information is available, a 3D rendering of the molecule is shown
* A browse menu is available listing the various molecular formulas for which files are available in the database
* Listing all files corresponding to a molecular formula
* Search page supporting filtering with various attributes of logfiles
* Displaying a file selected from browsing menu or search results


## Project plan

This project is currently being developed as 3 stages :
* Script which processes computational chemistry output files in specified folder and builds a MongoDB database (planned schema given below).
* API for searching molecules by various parameters and query calculation method results on them.
* Web-interface to search molecules using above API, get parsed data from an uploaded file and add new files to data repository.


### MongoDB schema

The current schema design has 3 collections:

* **parsed_file** : Documents containing the parsed data from each of the logfile. Contains parsed attributes and molecular formula.
* **molecule** : List of unique molecular formulas of the various parsed_files. Each document contains a list of ObjectIDs of the parsed_file documents corresponding to that molecular formula.
* **stats** : A single document containing min and max value for each parsed attribute.