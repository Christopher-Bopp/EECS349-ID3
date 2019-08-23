import csv
import sys

def parse(filename):
  '''
  takes a filename and returns attribute information and all the data in array of dictionaries
  '''
  # initialize variables

  out = []  
  csvfile = open(filename,'r')
  fileToRead = csv.reader(csvfile)

  headers = next(fileToRead)

  # iterate through rows of actual data
  for row in fileToRead:
    out.append(dict(zip(headers, row)))

#  blah = []
#  for i in out:
#    blah.append(i)

#  print(blah)
#  print ("/n /n /n")

  return out


#if __name__ == '__main__':
#    parse("house_votes_84.data")