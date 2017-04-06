
'''
Insight code challenge

There are 4 features covered in the code. The detail can be found in README file

Time zone is especially taken account, although the conversion will cost running time. It is very important when different time zones are compared, especialy in my experience (deal with the data from healthy wearable devices when one travels a lot), although looks not so important in this case.

Heap method (e.g. Data-parallel over keys) is used to certain extention (e.g. 60 min windows), while can be further applied in this case to deal with the big data with partition
'''

##import the modules
import time
import calendar
import dateutil.parser
import string
import operator
import sys
import pytz
from time import strftime

## Function to convert date string to timestamp
def convert_to_timestamp(datetime):
    dt = dateutil.parser.parse(datetime)
    newstamp = calendar.timegm(dt.timetuple())
    return newstamp

## Function to collect the necessary informtion from log file for feature achievement
def create_dict(file_name):
    #access the log file and import the data into a dictionary list
    file_in = open(file_name,'r')
    lines = file_in.readlines()
    dictIP = {}  #create a dictionary to store the necessary info for feature 1
    dictResource = {} #create a dictionary to store the necessary info for feature 2
    dictTime = {} #create a dictionary to store the visit time by different IP
    
    #create sets for each keys in dictionary
    ipSet = set()
    resourseSet = set()
    time_set = set()
    
    #create variables for in 20 second log attempt and the dictionary for the blocks of different IP
    attempt_fail_1st_time = 0
    attempt_fail_2nd_time = 0
    #attempt_fail_3rd_time = 0
    block_time = 0
    #attempt_dict = {}
    attempt_list = [] #use list other than set for the time order
    blocked_dict = {}
    pre_block = {}
    
    for n in range(len(lines)):
        line = lines[n]
        line = line.strip()
        temp =  line.split(' ',5)
        
        ipName = temp[0]
        
        #Convert time string with Time Zone to time stamps
     
        localTime = temp[3].lstrip('[')
        tZone = temp[4].rstrip(']')
    
        
        DateSplit = localTime.split(':',1)
        datetime =string.join(DateSplit[0].split('/')[::-1]+[DateSplit[1]]+[tZone],'/')
        timestamp = convert_to_timestamp(datetime)

        #get the information for rescource, replycode, and bytes(bandwith)
        try:
            remain = temp[5].rsplit(' ',2)
        except:
            print line

        #resource on the site
        resource = remain[0].strip('"')

        #reply code from the site
        replycode = int(remain[1])

        #bytes(bandwith) used
        if remain[2] is '-':
            bytes = 0
        else:
            bytes = int(remain[2])
        
        
    #put the access times to the IP name in the dictionary
    #For Feature 1
        if ipName in dictIP.keys():
            dictIP[ipName] += 1
        else:
            dictIP[ipName] = 1

    #put and add up the bandwidth(bytes) to the corresponding resource in the dictionary
    #For Feature 2
        if resource in dictResource.keys():
            dictResource[resource] += bytes
        else:
            dictResource[resource] = bytes

    #put the access times to each time in the dictionary
    #For Feature 3
        if timestamp in time_set:
            dictTime[timestamp] += 1
        else:
            dictTime[timestamp] = 1
            time_set.add(timestamp)
   
   
   
    #detect patterns of 3 consecutive failed login attemps over 20 seconds
    #For Feature 4
    
        #record the information to attempt_set if block for ip in blocked_dict is activated
        if ipName in blocked_dict.keys():
            if (timestamp-blocked_dict[ipName])<=300 :
                attempt_list.append(line)
                continue
            else:
                del blocked_dict[ipName]
       
        #continue or activate block according to 3 fail log attempt
        else:
            if replycode in [304,401]:
                if ipName in pre_block.keys():
                    if (timestamp-pre_block[ipName][0])<=20:
                        
                        #add a second fail log to the value list in pre_block dictionary
                        if len(pre_block[ipName])==1:
                            pre_block[ipName].append(timestamp)
                            continue
                        
                        #block is activated for the ipName, which is stored in blocked_dict
                        else:
                            blocked_dict[ipName] = timestamp
                            del pre_block[ipName]
            
                else:
                    pre_block[ipName] = [timestamp] #add timestamp to pre_block dictionary

        #reset for block condtion if reply code is 200 (fully accessed) in 20 seconds
            if replycode==200:
                if ipName in pre_block.keys():
                    if (timestamp-pre_block[ipName][0]) <= 20:
                        del pre_block[ipName]
    
    
    #return the needed information for feature achievement
    return (dictIP, dictResource, dictTime, time_set, attempt_list)


## Function to sort out the top 10 most active hosts/IP address (Feature1)
def get_top_active_host(dictIP, output_file, n=10):
    #sort the dictionary by values and store the top items into a tuple list
    topIpTuples = sorted(dictIP.items(), key=operator.itemgetter(1), reverse=True)[0:n]
    
    #write into a output file
    file_out = open(output_file, 'w')
    for items in topIpTuples:
        file_out.write(str(items[0]))
        file_out.write(',')
        file_out.write(str(items[1]))
        file_out.write('\n')
    file_out.close()


## Function to sort out the top 10 resources on the site that consume the most bandwidth (Feature2)
def get_most_consume_resources(dictResource, output_file, n=10):
    #sort the dictioany by values and store the top items into a tuple list
    topResourceTuples = sorted(dictResource.items(), key=operator.itemgetter(1), reverse=True)[0:n]
  
    #write into a output file
    file_out = open(output_file, 'w')
    for items in topResourceTuples:
        ip_Name = items[0].split()[1]
        file_out.write(ip_Name + '\n')
    file_out.close()


## Function to list the site's busiest 60-minute period (Feature3)
def get_busiest_period(dictTime, timeSet, output_file, n=10):
    
    #create a Heap to store the busiest period
    #start time and visit times as one tuple in the list
    if len(timeSet)<n:
        topTupleList =[(0,0)]*len(timeSet)
    else:
        topTupleList = [(0,0)]*n
    
    for ii  in range(min(timeSet),max(timeSet)+1):
    #calculate the visit time in 60 minute windows
        if ii in timeSet: #check if the timestamp exists in the recorded data
            totalVisit = 0
            #put visit times together in one hour window
            for i in range(ii,ii+3600):
                if i in timeSet:
                    totalVisit += dictTime[i]

            #pipe out the tuple with min value
            #pipe in the new tuple to the list
            if totalVisit >= topTupleList[-1][1]:
                topTupleList.pop()
                topTupleList.append((ii,totalVisit))
                topTupleList=sorted(topTupleList, key=operator.itemgetter(1), reverse=True)
        else:
            continue

    #write into a output file
    file_out = open(output_file, 'w')
    for items in topTupleList:
        Date = time.gmtime(items[0])
        file_out.write(strftime("%d/%b/%Y:%H:%M:%S -0400", Date) + ',' + str(items[1]) + '\n')
    file_out.close()


## Function to write out the blocked log information (Feature 4)
def writeout_blocks(attempt_list, output_file):
    #write into a output file
    file_out = open(output_file, 'w')

    for i in attempt_list:
        file_out.write(i + '\n')
    file_out.close()


## A function to collect file names from the input arguments
def get_file_names():
    if len(sys.argv) != 6:
        print "please type in the names of all the 5 necessary files following the current python file"
        exit()
    List = sys.argv
    return List


if __name__ == "__main__":
    #get the necessary file names from arugument
    file_list = get_file_names()
    log_file = file_list[1]
    hosts_file = file_list[2]
    hours_file = file_list[3]
    resources_file = file_list[4]
    blocks_file = file_list[5]
    
    #Obtain the necessary information from the log file
    dictIP, dictResource, dictTime, timeSet, attempt_list = create_dict(log_file)
    
    #Output for Feature 1
    get_top_active_host(dictIP, hosts_file)
    
    #Output for Feature 2
    get_most_consume_resources(dictResource, resources_file)
    
    #Output for Feature 3
    get_busiest_period(dictTime, timeSet, hours_file)

    #Output for Feature 4
    writeout_blocks(attempt_list, blocks_file)


