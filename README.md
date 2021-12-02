# CS251-Project-3-Autograder-Docker-Image
## Acknowledgements
The basis for this autograder was built from one of the autograder examples provided by the nice folks at Gradescope. You can find it [here](https://github.com/gradescope/autograder_samples/tree/master/java).

## Overview
This auto grader has been designed to be used on Gradescope and thus follows Gradescope's autograder specifications. This project is intended for project 3 for CS251 Fall 2021 and is made up of the following modules:  

1. `setup.sh`
2. `run_autograder.sh`
3. `process_submissions.py`
4. `./lib`
5. `./replacement_code`
6. `./src` (All Java here)
    - `/jh61b`
    - `/project3`
        - `/tests`
7. `run.sh`

## Folder structure of the Docker image
An important fact to keep in mind while reading this is the folder structure of the Docker image. As I understand it, Gradescope spins up a Docker image for us where our autograder code is placed inside the `/autograder/source` folder, the students submission is located in `/autograder/submission`, and finally a folder to store the results from our autorader `/autograder/results`. These are the three folders relevant to this project. Most of our work will take place in the `/autograder/source` folder.

## Setup&#46;sh
`setup.sh` is a bash script that the Gradescope Docker image will run first after we upload our autograder. We are suppposed to use this file to install the dependencies for our project. In this project, we used this script to install Python, Java-17, and the Python packages listed in `requirments.txt`. We also make `run_autograder.sh` an executable in this script.

## Run_autograder.sh
`run_autograder.sh` is the script that is run after a student submits their code. Run_autograder.sh functions as the "Brain" of this program as it is responsible for calling all other relevant modules in the autograder. The first thing  this script does is to change our working directory from `./` to `./autograder/source`. It then runs `process_submission.py` to process the students submission. It the creates the folder `./autograder/source/classes` to store all the java classes produced by this project. After this, the script compiles all the java code in the `./autograder/source/src` directory (Testing Code + Smaple Solution Code + the student's prosseced submission) with all the necessary dependencies from `./autograder/source/lib` linked. Finally, `run.sh` is called with its output being sent into `/autograder/results/results.json`.

## Process_submissions.py
`process_submissions.py` is responsible for performing some pre-processing on the student's submission. The primary purpose of this pre-proccesing is to standardize student submissions in order to ensure that we will not run into any compile-time errors during the autograding phase. The following are the pre-processing steps I took for this assignment:  

- Ensure that the files that are needed for this assignment are in the student's submission (`Main.java`, `Sequence.java`, and `Pair.java`).
    1. If `Sequence.java` is missing, add the dummy file `./autograder/source/replacement_code/Sequence.java` that will compile but not pass tests.
    2. If `Pair.java` is missing, add functional file `./autograder/source/replacement_code/Pair.java`.
    3. If `Main.java` is missing, student may have used an alternative name. Try to find the file and rename it (and its class definition) to `Main`.
- Ensure that all methods that I will later unit test exist and have the correct parameters. Although student's are allowed to alter method definitions, there is no reliable way to write unit tests that will for all the possible imlpementations of each method. Thus, we will only be able to autograde submissions with un altered method definitions (Everyone else has to be manually graded). There are also compile-time errors to consider, so dummy methods that will fail the test have to be inserted into submissions with missing (or altered) methods. We also "neatrilize" altered methods by changing their names to avoid compile time errors.
- Remove all packages
- Remove non-standard library imports as these will compromise the autograder.
- Add the needed package names and imports that will be needed to get the submission to work with the autograder.
- Replace 'private' with 'public' for all method definitions.

After the script has completed its preprocessing, the processsed files are placed into `./autograder/source/src/main/java/com/gradescope/project3`.  

## Lib folder `./lib`
This folder contains the `.jar` files fot JUnit and its dependency Hamcrest. Both of these jar files will need to be linked during compilation and excecution.

## Replacement code folder `./replacement_code`
This folder contains the dummy files that will be added to student submissions that are missing either of these files.    
- `./autograder/source/replacement_code/Pair.java` is fully functional as student are not responsible for any methods in this file.
- `./autograder/source/replacement_code/Sequence.java` is partially functional. Everything works except for the pairwise iterator. This ensures that the code in the student's main file can run while the pairwise iterator test will not pass.

## SRC folder `./src/main/java/com/gradescope`
This folder contains two folders, `jh61b/` and `project3/`. The sample solution, the student's processed submission, and all the testing code are located in `project3/code/`. `project3/code/` contains the sample solution and the student's processed submission. `project3/code/` also contains the folder `project3/code/test` where our testing code lives. `RunTests.java` is the java file that is run by `.run.sh`. It is our testing suite and thus is responsible for running `UnitTesting.java`. `UnitTesting.java` contains our unit tests. Both `RunTests.java` and `UnitTesting.java` leverage classes from `jh61b/grader/`.  
  
`jh61b/` contains two folders but the important one for our purposes is `grader/` as it contains the code that supprots our testing code in `project3/`. There are four files of note in `grader/`; `GradedTest.java`, `TestResult.java`, `GradedTestListenerJSON.java`, and `MyGradedTestListenerJSON.java`. `GradedTest.java` contains the annotation that we will use in `UnitTesting.java` to label our tests. `TestResult.java` is a class that we can use to represent the results of each of our tests. Its `.toString()` method will format our test results in the manner Gradescope expects them to be (see sample in `jh61b/grader/gradescope_schema.txt`). The last two methods perform similar function. They listen for the output of the tests we run and store that information in instances of `TestResult.java`. They then collate these result and the final product is then outputted by `RunTests.java` into `/autograder/results/results.json`. `GradedTestListenerJSON.java` was provided by the folks at Gradescope. I wrote `MyGradedTestListenerJSON.java` so that I could have more freedom in how I designed my test casses. Only `MyGradedTestListenerJSON.java` is active in this project. 

