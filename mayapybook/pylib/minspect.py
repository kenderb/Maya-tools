import pymel.core as pmc
import sys

def syspath():
    print 'sys.path'
    for p in sys.path:
        print ' ' + p

def info(obj):
    '''Prints information about the object.'''

    lines = ['info for %s' % obj.name(), 'Attributes:']
    # Get the name of all attributes
    for a in obj.listAttr():
        lines.append(' ' + a.name())
    lines.append('Mel type: %s'% obj.type())
    lines.append('MRO: ')
    lines.extend([' '+t.__name__ for t in type(obj).__mro__])
    result = '\n'.join(lines)
    print result