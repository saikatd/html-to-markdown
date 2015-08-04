import HTMLParser
import re
import sys


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser.HTMLParser):
    def __init__(self, out=None, baseurl=''):
        HTMLParser.HTMLParser.__init__(self)
        self.memory=[]      #stack implementation for pushing in and popping out tags
        self.text=''        #stores the intermediate text which is to be shown in the markdown format
        self.link=''
        self.indent = -1    #counts the indentation level - for implementing nested <ul>...</ul>
        self.counter = 0    #for implementing ordered list
        self.heading_pattern = re.compile(r'h[1-9]')    #regex for headings
        self.last_popped='' #stores the last popped element

    def handle_starttag(self, tag, attrs):
        '''
        Function handles - When a open tag is encountered
        '''
        self.memory.append(tag)
        if tag == 'a':
            self.link = attrs[0][1]
        elif tag == 'hr':
            self.text+='\n* * *\n'
        elif tag == 'ul':
            self.indent+=1
        elif tag == 'li' and self.memory[-2] == 'ul':
            self.text+='\n'+' '*2*self.indent+'* '
        elif tag == 'ol':
            self.counter = 1
        elif tag == 'li' and self.memory[-2] == 'ol':
            self.text+='\n'+str(self.counter)+'. '
        elif tag == 'pre':
            self.text+='\n```'
        print 'added', self.memory

    def handle_endtag(self, tag):
        '''
        Function handles - When a close tag is encountered 
        '''
        if tag == 'ul':
            self.indent-=1
        if tag == 'pre':
            self.text+='\n```'
        self.last_popped = self.memory.pop()
        print 'removed', self.last_popped

    def handle_data(self, data):
        '''
        Function handles - When data between the tag is received
        '''
        #for heading case
        if (self.heading_pattern.match(self.memory[-1])):
            heading_number = int(self.memory[-1][1])
            self.text+='\n'+"#"*heading_number+' '+data

        #for the cases when the <p> tag and <ul> tags appear simultaneously and an extra break is required - \n\n
        elif self.memory[-1] == 'p' and (self.last_popped == 'ul' or self.last_popped == 'ol'):
            self.text+="\n\n"+data
        elif self.memory[-1] == 'p' and (self.last_popped != 'ul' or self.last_popped != 'ol'):
            self.text+="\n"+data

        #for handling links
        elif self.memory[-1] == 'a':
            self.text+='['+data+']'+'('+self.link+')'
            self.link = ''

        #for handling general <li> cases of <ul> and <ol>
        elif self.memory[-1] == 'li' and self.memory[-2] == 'ul':
            self.text+=data
        elif self.memory[-1] == 'li' and self.memory[-2] == 'ol':
            self.text+=data
            self.counter+=1

        #for handling code tag
        elif self.memory[-1] == 'code':
            self.text+='\n\t'+data
        elif self.memory[-1] == 'span':
            self.text+='\n\t'+data



    def printing(self):
        print self.text

# filename = sys.argv[1]      #stores the filename of the html file that has to be fed to parser
f = open("ul_ol_combination.html", 'r')
test = f.read()

#preprocessing the text
test = test.replace('\n','')  #removing any '\n's
test = test.strip('\t\r')     #removing any leading and trailing '\t' or '\r'

#instantiated the parser and fed it the HTML file
parser = MyHTMLParser()
parser.feed(test)
parser.printing()