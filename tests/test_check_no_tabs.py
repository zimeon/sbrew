"""Given that Python relies upon spacing for block structure, tabs are
bad. Check that none exist in the source code for this project. I do 
not want to get caught out by them again! -- Simeon/2014-11-09
"""
import unittest
import os
import os.path

class TestAll(unittest.TestCase):

    def check_file(self,filename):
        line_nums=[]
        fh=open(filename,'r')
        n=0
        for line in fh.readlines():
            n+=1
            if (line.find('\t')>=0):
                line_nums.append(str(n))
        self.assertEqual( len(line_nums), 0, "File '%s' has tabs in lines %s"%(filename,','.join(line_nums)))

    def test_no_tabs(self):
        for root, dirs, files in os.walk('.'):
            if ('build' in dirs):
                dirs.remove('build')
            for filename in files:
                if (filename[-3::]=='.py'): #assume extension typing for python code
                    self.check_file(os.path.join(root,filename))

# Do tests run from command line
if __name__ == '__main__':
    unittest.main()
