# Automation of system administration tasks
### general-info
simple python sort log application using python and doing statistic with sorted data, we'll maybe also add graph and other things that can make our project different from other project 
Authors Lim Maxence Lacheray Louis 
### Table of content 
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [usage](#usage)
* [add on](#addon)

### technologies
* python version : 3.0

### Setup 
* have python version: 3.0 on your computer 
* module needed : re and json
### usage 
* logs 
logs must look like that or the program might don't run 
```
83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1" 200 203023 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
```
Here we can clearly see there is different part like the time part, the remote_ip, ...
* how json should look like 
it will look like this :
```json
{
      "time" : "-------",
      "remote-ip" : "------",
      "request" : "------",
      "response" : "-------",
      "bytes" : "------",
      "referrer" : "------",
      "system_agent" : "------",
      "user_agent" : "------",
}
```
here we can see the different part we talked before, the whole logs will be list like that.
if their is nothing in the log there will just be a -
```json
{
       "bytes" : "-",
}
```
* dump a file into a json file
 ```json
python '.\Projet_python_LIM_LACHERAY_1A.py' --dump test.txt_example.txt
```
so --dump is the option then the name of the file to dumb and how you want the json file to be named
* statistic
we have done many statistic that we think usefull so here a exemple of how to use it
 ```json
python .\Projet_python_LIM_LACHERAY_1A.py --ip     log.json
 ```
so the --ip is the option and it will show whitch ip come the more often  it can also be 
 ```json
--mobile
```
to show number of mobile that are used 
 ```json
--error
```
to show ip that make error (to much error can be usefull for security)
 ```json
--hours
```
to show hours sorted by popularity 
 ```json
--bots
```
to show differents bots 
### add on 
you can add graph to make stat more visible 
or a graphic interface