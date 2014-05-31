import sys, os, shutil

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

SDL2_LIBS         = "$(shell sdl2-config --libs)"
SDL2_LIBCFLAGS    = "$(shell sdl2-config --cflags)"

# Libraries that can be added
def addSDL2():
    global MAKE_LIBS, MAKE_LIBCFLAGS
    MAKE_LIBS      += SDL2_LIBS + " "
    MAKE_LIBCFLAGS += SDL2_LIBCFLAGS + " "

def addOpenGL():
    global MAKE_LIBS
    MAKE_LIBS += "-lGL -lGLU"

LIB_FUNCS = dict(sdl2=addSDL2, opengl=addOpenGL)

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

def addLibs(libargs):
    for i in libargs:
        f = LIB_FUNCS[i]
        if f is not None:
            f()
        else:
            print "Unknown library {}, ignoring...".format(i)

def main():
    if len(sys.argv) < 3:
        print "usage: projman.py <mk,rm> <projectname>"
        sys.exit(1)
    
    if sys.argv[1] == "mk":
        name = sys.argv[2]
        if os.path.exists(name):
            if confirmPrompt("overwrite {}".format(name)) == False:
                sys.exit(1)

        if len(sys.argv) > 3:
           addLibs(sys.argv[3:])

        createDirs(name)
        writeMakefile(name)

    elif sys.argv[1] == "rm":
        name = sys.argv[2]
        if confirmPrompt("delete {}".format(name)):
            shutil.rmtree(name)
    else:
        print "Unknown command, please try again."
        sys.exit(1)

if __name__ == '__main__':
    main()
