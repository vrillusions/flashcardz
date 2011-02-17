#!/usr/bin/env python
# vim:ts=4:sw=4:expandtab:ft=python:fileencoding=utf-8
"""FlashcardZ

Takes a list, randomizes it, and asks for the answer

"""

__version__ = "0.1"

import sys
import os
import traceback
import random
from optparse import OptionParser


def main():
    '''The main function.
    
    See https://github.com/vrillusions/timelog for another different looping
    mechanism.
    
    '''
    global monitor
    parser = OptionParser(version='%prog v' + __version__)
    parser.add_option('-f', '--file', default='datafile.txt',
        help='use FILE (default: %default)', metavar='FILE')
    (options, args) = parser.parse_args()
    
    if os.path.isfile(options.file) == False:
        print 'Data file (' + options.file + ') could not be found.'
        sys.exit(1)
    fh = open(options.file, "r")
    # This isn't very efficient on large datasets since it reads the whole
    # thing into memory.
    # This also won't like two lines with the same "question"
    questions = dict()
    line = fh.readline()
    while line:
        # strips off the \n at end and then splits on |
        (question, answer) = line.rstrip().split('|')
        questions[question] = answer
        line = fh.readline()
    print 'Type the answer to the question, q to quit or s for solution.'
    print
    newquestion = True
    # we'll increment a couple counters
    number_correct = 0
    number_wrong = 0
    while True:
        if newquestion:
            # dictionaries are pretty messy to try and get a random line from it
            i = random.randint(0, len(questions))
            linecount = 0
            for question, answer in questions.items():
                if i == linecount:
                    # we have our question and answer, leave the loop
                    break;
                else:
                    linecount += 1
            newquestion = False;
        msg = raw_input(question + ' = ')
        if msg == 'q':
            # quit the while loop
            print
            print 'Number of quetions:'
            print 'correct', str(number_correct)
            print 'wrong  ', str(number_wrong)
            break;
        elif msg == 's':
            # print the solution and then get a new question
            print 'The answer was: ' + answer
            newquestion = True
        elif msg == answer:
            # they answered correctly, new question
            print 'CORRECT!'
            number_correct += 1
            newquestion = True
        else:
            # didn't answer correctly and not a command, retry
            print 'WRONG! Try again.'
            number_wrong += 1


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt, e:
		# Ctrl-c
        raise e
	except SystemExit, e:
		# sys.exit()
		raise e
	except Exception, e:
		print "ERROR, UNEXPECTED EXCEPTION"
		print str(e)
		traceback.print_exc()
		sys.exit(1)
	else:
		# Main function is done, exit cleanly
		sys.exit(0)

