# fansite_analytics
It is for the coding challenge
# Table of Contents_modified from original Insight Challenge requests
1. [Challenge Summary](README.md#challenge-summary)
2. [Details of Implementation](README.md#details-of-implementation)
3. [Download Data](README.md#download-data)
4. [Description of Data](README.md#description-of-data)
5. [Repo directory structure](README.md#repo-directory-structure)
6. [Testing the directory structure and output format](README.md#testing-your-directory-structure-and-output-format)


# Challenge Summary

Dear with a NASA fan website that generates a large amount of Internet traffic data. The desired features are described below: 

### Feature 1: 
List the top 10 most active host/IP addresses that have accessed the site.

### Feature 2: 
Identify the 10 resources that consume the most bandwidth on the site

### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods 

### Feature 4: 
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.

##details of implementation

### Feature 1 
List in descending order the top 10 most active hosts/IP addresses that have accessed the site in `hosts.txt`.


### Feature 2 
Identify the top 10 resources on the site that consume the most bandwidth and store in `resources.txt`.
    

### Feature 3 
List in descending order the site’s 10 busiest (i.e. most frequently visited) 60-minute period and write to a file named `hours.txt`.


### Feature 4 
Detect patterns of three consecutive failed login attempts over 20 seconds in order to block all further attempts to reach the site from the same IP address for the next 5 minutes. Each attempt that would have been blocked will be written to a log file named `blocked.txt`.



![Feature 4 illustration](images/feature4.png)


Note that this feature should not impact the other features in this challenge. For instance, any requests that end up in the `blocked.txt` file should be counted toward the most active IP host calculation, bandwidth consumption and busiest 60-minute period.

### Additional Features

Feel free to implement additional features that might be useful to derive further metrics or prevent harmful activity. These features will be considered as bonus while evaluating your submission. If you choose to add extras please document them in your README and make sure that they don't interfere with the above four (e.g. don't alter the output of the four core features).

## Download Data
You can download the data here: https://drive.google.com/file/d/0B7-XWjN4ezogbUh6bUl1cV82Tnc/view

## Description of Data

A file, `log.txt`, in ASCII format with one line per request, containing the following columns:

* **host** making the request. A hostname when possible, otherwise the Internet address if the name could not be looked up.

* **timestamp** in the format `[DD/MON/YYYY:HH:MM:SS -0400]`, where DD is the day of the month, MON is the abbreviated name of the month, YYYY is the year, HH:MM:SS is the time of day using a 24-hour clock. The timezone is -0400.

* **request** given in quotes.

* **HTTP reply code**

* **bytes** in the reply. Some lines in the log file will list `-` in the bytes field. For the purposes of this challenge, that should be interpreted as 0 bytes.


e.g., `log.txt`

    in24.inetnebr.com - - [01/Aug/1995:00:00:01 -0400] "GET /shuttle/missions/sts-68/news/sts-68-mcc-05.txt HTTP/1.0" 200 1839
    208.271.69.50 - - [01/Aug/1995:00:00:02 -400] “POST /login HTTP/1.0” 401 1420
    208.271.69.50 - - [01/Aug/1995:00:00:04 -400] “POST /login HTTP/1.0” 200 1420
    uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 0
    uplherc.upl.com - - [01/Aug/1995:00:00:08 -0400] "GET /images/ksclogo-medium.gif HTTP/1.0" 304 0
    ...
    
In the above example, the third line shows a failed login (HTTP reply code of 401) followed by a successful login (HTTP reply code of 200) two seconds later from the same IP address.

## Repo directory structure

The directory structure for the repo should look like this:

    ├── README.md 
    ├── run.sh
    ├── src
    │   └── process_log.py
    ├── log_input
    │   └── log.txt
    ├── log_output
    |   └── hosts.txt
    |   └── hours.txt
    |   └── resources.txt
    |   └── blocked.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_features
            |   ├── log_input
            |   │   └── log.txt
            |   |__ log_output
            |   │   └── hosts.txt
            |   │   └── hours.txt
            |   │   └── resources.txt
            |   │   └── blocked.txt
            ├── your-own-test
                ├── log_input
                │   └── your-own-log.txt
                |__ log_output
                    └── hosts.txt
                    └── hours.txt
                    └── resources.txt
                    └── blocked.txt


## Testing the directory structure and output format

To make sure that the code has the correct directory structure and the format of the output files are correct, a test script, called `run_tests.sh` is in the `insight_testsuite` folder.

The tests are stored simply as text files under the `insight_testsuite/tests` folder. Each test should have a separate folder and within should have a `log_input` folder for `log.txt` and a `log_output` folder for outputs corresponding to the current test.

One can run the test with the following from the `insight_testsuite` folder:

    insight_testsuite~$ ./run_tests.sh 

On a failed test, the output of `run_tests.sh` should look like:

    [FAIL]: test_features (hosts.txt)
    [FAIL]: test_features (resources.txt)
    [PASS]: test_features (hours.txt)
    [FAIL]: test_features (blocked.txt)
    [Thu Mar 30 16:28:01 PDT 2017] 1 of 4 tests passed

On success:

    [PASS]: test_features (hosts.txt)
    [PASS]: test_features (resources.txt)
    [PASS]: test_features (hours.txt)
    [PASS]: test_features (blocked.txt)
    [Thu Mar 30 16:25:57 PDT 2017] 4 of 4 tests passed
