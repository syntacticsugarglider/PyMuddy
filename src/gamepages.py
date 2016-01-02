class GamePage:
    def __init__(self):
        self.registries={}
        self.helpmessage=""
        fp=open('../man/manpages')
        fp2=open('../man/help')
        for line in fp2.readlines():
            self.helpmessage+=line.strip('\r\n')+'\n\r'
        fp2.close()
        fp.seek(0)
        self.state='Reading'
        for line in fp.readlines():
            if line[0]=='@':
                deftype=line.split()[0][1:]
                command=line.split()[1]
                try:
                    arguments=line.split()[2:]
                except IndexError:
                    arguments=[]
                self.currentcommand=command
                self.registries[command]=ManRegistry(command,deftype,arguments)
            elif line[0]=='#':
                self.registries[self.currentcommand].appendTextLine(line[1:])
        fp.close()
    def getManualForCommand(self,commandname):
        try:
            return self.registries[commandname].getManPage()
        except KeyError:
            return "Sorry, no manual entry found for %s. That is not the manpage you are looking for." % commandname
    def getFullManual(self):
        returner=''
        for foo, value in self.registries.iteritems():
            returner+=value.getManPage()
        return returner
    def getHelpPage(self):
        return self.helpmessage+'\n\r'

class ManRegistry:
    def __init__(self,name,typed,arglist):
        self.type=typed
        self.arglist=arglist
        self.name=name
        self.text=''
    def appendTextLine(self,text):
        self.text+='%s\n\r' % text.strip('\r\n')
    def getManPage(self):
        manstring=' COMMAND: %s %s\n\r\n\r%s\n\r' % (self.name,' '.join(self.arglist),self.text)
        return manstring
