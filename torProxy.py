import optparse
import pycountry
import stem.process
from stem.util import term

def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print(term.format(line, term.Color.BLUE))

def startTor(port, country = None):
    conf = {
        'SocksPort': str(port)
    }
    if country:
        conf['ExitNodes'] = '{%s}' % country
    return stem.process.launch_tor_with_config(
        config = conf,
        init_msg_handler = print_bootstrap_lines
    )

def main():
    parser = optparse.OptionParser('usage prog -p <port>')
    parser.add_option('-p', '--port', dest='port', type='int', help='specify proxy local port')
    (options, args) = parser.parse_args()
    port = 7000
    if options.port != None:
        port = options.port
    try:
        torProcess = startTor(port)
        print "[*] Started tor proxy on port " + str(port)
        while True:
            inp = raw_input(">> ")
            if "shuffle" in inp:
                torProcess.kill()
                torProcess = startTor(port)
                print "[+] Exit point changed randomly"
            elif "country: " in inp:
                country = (inp.split(": "))[1]
                cname = None
                try:
                    cname = pycountry.countries.get(alpha2=country.upper())
                except:
                    pass
                if cname == None:
                    print "invalid country"
                else:
                    torProcess.kill()
                    torProcess = startTor(port, country)
                    print "[+] Exit point changed to %s" % cname.name
            else:
                print "[+] Tor proxy running..."
    except:
        pass
    finally:
        torProcess.kill()
        print "\n\n[+] Closed tor proxy successfully"

if __name__ == "__main__":
    main()
