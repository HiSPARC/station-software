import sys
sys.path.append('../../user/diagnosticchecks')
from checks import CRITICAL, checkBufferdb, check_lvusage


def parse_range(range):
    """
    Make a tuple from a range string. 'min:max' -> (min, max)
    """
    try:
        a = range.split(':')
        min = float(a[0])
        max = float(a[1])
        return (min, max)
    except:
        print 'Wrong argument! (%s)' % range
        sys.exit(CRITICAL)


def main(argv):
    if len(argv) < 1:
        print ('No argument:', str(argv))
        sys.exit(CRITICAL)

    function_name = argv[0]
    retval = 0

    # Buffer database connection.
    if function_name == 'bufferdb':
        warn = parse_range(argv[1])
        crit = parse_range(argv[2])
        retval = checkBufferdb(warn, crit)

    # labview usage
    elif function_name == 'lvusage':
        warn = parse_range(argv[1])
        crit = parse_range(argv[2])
        retval = check_lvusage(warn, crit)

    return retval


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
