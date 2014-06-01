import sys, os, shutil, argparse

# edit this to point to the makefile template or run the script from this directory
MAKEFILE_TEMPLATE_PATH = "template"

MAKE_SHELL        = "/bin/sh"
MAKE_CC           = "gcc"

MAKE_FLAGS        = "-ansi"
MAKE_CFLAGS       = "-Wall"
MAKE_DEBUGFLAGS   = "-O0 -g"
MAKE_RELEASEFLAGS = "-O2"

MAKE_TARGET       = None
MAKE_SOURCES      = "$(shell echo src/*.c)"
MAKE_HEADERS      = "$(shell echo include/*.h)"
MAKE_OBJECTS      = "$(SOURCES:.c=.o)"

MAKE_LIBS         = ""
MAKE_LIBCFLAGS    = ""

MAKE_PC_LIBS      = "$(shell pkg-config {} --libs) "
MAKE_PC_CFLAGS    = "$(shell pkg-config {} --cflags) "

def confirmPrompt(msg):
    i = None
    while  i != "Y" and i != "N":
        i = raw_input('Do you wish to {}? Y/N: '.format(msg))
    return bool(i == "Y")

def createDirs(name):
    try:
        os.mkdir(name)
        os.mkdir(name+"/src")
        os.mkdir(name+"/include")
    except:
        pass

def writeMakefile(name):
    try:
        infile = open(MAKEFILE_TEMPLATE_PATH, 'r')
    except:
        print "Couldn't open Makefile template, exiting..."
        sys.exit(1)

    try:
        outfile = open(name+"/Makefile", 'w')
    except:
        print "Couldn't open Makefile for writing, exiting..."
        sys.exit(1)

    intext = infile.read()
    MAKE_TARGET = name.split("/").pop()
    formattedtext = intext.format(MAKE_SHELL, MAKE_CC, MAKE_FLAGS, MAKE_CFLAGS, MAKE_DEBUGFLAGS, MAKE_RELEASEFLAGS, MAKE_TARGET, MAKE_SOURCES, MAKE_HEADERS, MAKE_OBJECTS, MAKE_LIBCFLAGS, MAKE_LIBS)
    outfile.write(formattedtext)
    infile.close()
    outfile.close()

def addPcPkg(pkg):
    global MAKE_LIBS, MAKE_LIBCFLAGS
    MAKE_LIBS += MAKE_PC_CFLAGS.format(pkg)
    MAKE_LIBCFLAGS += MAKE_PC_LIBS.format(pkg)

def createProject(args):
    global MAKE_LIBS, MAKE_LIBCFLAGS
    if os.path.exists(args.create_project[0]):
        if confirmPrompt("overwrite {}".format(args.create_project[0])) == False:
            sys.exit(1)
    if args.libs:
        for i in args.libs:
            MAKE_LIBS += "-l" + i + " "
    if args.cflags:
        for i in args.cflags:
            MAKE_LIBCFLAGS += i
    if args.pkg_config:
        for i in args.pkg_config:
            addPcPkg(i)

    createDirs(args.create_project[0])
    writeMakefile(args.create_project[0])

def deleteProject(args):
    if confirmPrompt("delete {}".format(args.delete_project[0])):
        shutil.rmtree(args.delete_project[0])

def main():
   parser = argparse.ArgumentParser()
   group = parser.add_mutually_exclusive_group()
   group.add_argument("--create-project", "-c", nargs=1)
   group.add_argument("--delete-project", "-d", nargs=1)
   parser.add_argument("--libs", "-l", action='append')
   parser.add_argument("--cflags", "-cf", action='append')
   parser.add_argument("--pkg-config", "-pc", action='append')
   
   args = parser.parse_args()
   if args.create_project:
       createProject(args)
   elif args.delete_project:
       deleteProject(args)
   else:
       parser.print_help()

if __name__ == '__main__':
    main()
