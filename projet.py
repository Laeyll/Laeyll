#!/usr/bin/python3

import re
import json
import argparse

############################################__fuctions__############################################

#fuction to get the os
def user_agent(sysAgent):
    res = ""
    resinter= re.search('(\([^\)]*\))', sysAgent)
    if resinter:
        if 'Windows' in resinter.group(1) or 'Linux' in resinter.group(1) or 'Mac OS' in resinter.group(1):
            res = resinter.group(1)
        else:
            res = ' None or unknown '
    else :
        res = ' None or unknown '
    return(res)

#fuction to parse the line of the file as dictionaries containing the type as key and their values as value
def parse(entryFile):
    res = []
    resinter = {}
    f=open( entryFile , 'r')
    l= f.readlines()
    for i in l :
        resinter = {}
        i=i.translate({ord('\n'):None})
        search = re.search('([^ ]*) [^\[]*(\[[^\]]*\]) "([^"]*)" (-?[0-9]*) (-?[0-9]*) "([^"]*)" "([^"]*)"?', i)
        if search:
            resinter['time'] = search.group(2)
            resinter['remote_ip'] =  search.group(1)
            resinter['request'] =   search.group(3)
            resinter['response'] =   search.group(4)
            resinter['Bytes'] =   search.group(5)
            resinter['referrer'] =   search.group(6)
            resinter['system_agent'] =  search.group(7)
            resinter['user_agent'] = user_agent( search.group(7))
        else :
            resinter = None
        res.append(resinter)
    return(res)

#function to dump the result of parse to a json file
def dump(entryFile,outfil="log.json"):
    with open(outfil, 'w') as outfile:
        json.dump(parse(entryFile), outfile, indent=4)
    return None

############################################__stats fuctions__############################################

#function to get the ammount of entry in the log for each ip address that return the 15 with the most entry in the log sorted by number of entry
def ip(entryfile) :
    listip = []    
    dictip = {}
    with open(entryfile, 'r') as outfile:
        data = json.load(outfile)
        for i in data:
            if i :
                if i['remote_ip'] in dictip.keys() :
                    dictip[i['remote_ip']] +=1
                else :
                    dictip[i['remote_ip']] = 1                
    sort_order = sorted(dictip.items(), key=lambda x: x[1], reverse=True)
    i = 0
    while i< 15:
        ipv = sort_order[i]
        listip.append(ipv)
        i += 1
    return listip

#fuction to get the number of visit made with a mobile and total amout of visit
def mobile(entryfile) :      
    quantityMobile = [0,0]
    with open(entryfile, 'r') as outfile:
        data = json.load(outfile)
        for i in data:
            if i :
                quantityMobile[0] += 1
                if 'Mobile' in (i['system_agent']):
                    quantityMobile[1] += 1
        return quantityMobile      

#fuction to get the ip that made 400 errors and the number they made
def error400(entryfile) :      
    ipSus = {}
    with open(entryfile, 'r') as outfile:
        data = json.load(outfile)
        a = 0
        for i in data:
            if i :
                if 400<= int(i['response']) < 500 :
                    if (i['remote_ip']) in ipSus.keys():
                        ipSus[i['remote_ip']] += 1
                    else:
                        ipSus[i['remote_ip']] = 1
    sort_order = sorted(ipSus.items(), key=lambda x: x[1], reverse=True)
    return sort_order      

#function to get the different hours and the number of visit they each get
def hour(entryfile) :      
    hours = {}
    with open(entryfile, 'r') as outfile:
        data = json.load(outfile)
        for i in data:
            if i :
                houri = i['time'].split(":")
                if houri[1] in hours.keys():
                    hours[houri[1]] += 1
                else:
                    hours[houri[1]] = 1
    sort_order = sorted(hours.items(), key=lambda x: x[1], reverse=True)
    return sort_order
 
#fuction to get wich known bots visit and their number of visits
def goodBot(entryfile) :

    bots = {
        'Googlebot': 0,
        'Baiduspider': 0,
        'msnbot': 0,
        'Bingbot': 0,
        'yahooSlurp': 0,
        'YandexBot': 0,
        'Exabot': 0,
        'facebot': 0,
        'ia_archiver': 0,
    }

    with open(entryfile, 'r') as outfile:
        data = json.load(outfile)
        for i in data:
            if i :
                if 'Googlebot' in i['system_agent'] :
                    bots['Googlebot'] +=1
                if 'Baiduspider' in i['system_agent'] :
                    bots['Baiduspider'] +=1
                if 'msnbot' in i['system_agent'] :
                    bots['msnbot'] +=1
                if 'bingbot' in i['system_agent'] :
                    bots['Bingbot'] +=1
                if 'Slurp' in i['system_agent'] :
                    bots['yahooSlurp'] +=1
                if 'YandexBot' in i['system_agent'] :
                    bots['YandexBot'] +=1
                if 'Exabot' in i['system_agent'] :
                    bots['Exabot'] +=1
                if 'facebookexternalhit' in i['system_agent'] :
                    bots['facebot'] +=1
                if 'ia_archiver' in i['system_agent'] :
                    bots['ia_archiver'] +=1
    sort_order = sorted(bots.items(), key=lambda x: x[1], reverse=True)
    return sort_order 

############################################__main__############################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump",help="fileToDump_outfile with outfile being optional, log.json by default")
    parser.add_argument("--error",help="to display users that made 4xx errors")
    parser.add_argument("--ip",help="to display ips that have entries in the log")
    parser.add_argument("--mobile",help="to display the number of mobile in the log")
    parser.add_argument("--hours",help="to display the hours by popularity")
    parser.add_argument("--bots",help="to display the known bots mainly crawler")
    args = parser.parse_args()
    if args.dump :
        if "_" in args.dump :
            i = args.dump.split("_")
            dump(i[0],i[1])
        else :
            dump(args.dump)
        print("done")
    if args.ip :
        try :
            print("the 15 ip with the most visit and their number of visit are :\n"+str(ip(args.ip))+"\n")
        except FileNotFoundError:
            print("No such file : "+ str(args.ip))
    if args.mobile :
        try:
            usr = mobile(args.mobile)
            print("there is "+str(usr[1])+" visit made with a mobile device out of "+str(usr[0]) +" visit\n")
        except FileNotFoundError:
            print("No such file : "+ str(args.mobile))
    if args.error :
        try:
            print("the ip that made 4xx error along with the number they made are :\n"+str(error400(args.error))+"\n")
        except FileNotFoundError:
            print("No such file : "+ str(args.error))
    if args.hours :
        try:
           print("hours sorted by popularity :\n"+str(hour(args.hours))+"\n")
        except FileNotFoundError:
            print("No such file : "+ str(args.hours))
    if args.bots :
        try:
            print("the known bot that visited along with their number of visit are \n"+str(goodBot(args.bots))+"\n")  
        except FileNotFoundError:
            print("No such file : "+ str(args.bots))
