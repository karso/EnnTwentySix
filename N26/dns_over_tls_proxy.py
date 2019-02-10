'''
Nowadays, some providers (such as Cloudflare) provide a DNS-over-TLS feature that could let
us enhance privacy by encrypting our DNS queries.
Our applications don't handle DNS-over-TLS by default. Your task is to design and create a
simple DNS to DNS-over-TLS proxy that we could use to enable our application to query a
DNS-over-TLS server.
'''

import thread       
import socket
import ssl


## DNS request padding
def dnsDataParser(data):
    initQ = "\x00"+chr(len(data))
    finalQ = initQ + data
    return finalQ

## Send DNS req to the DNS server
def sendReq(tlsConn, data):
    dnsQuery = dnsDataParser(data)
    tlsConn.send(dnsQuery)
    result=tlsConn.recv(1024)
    return result

## Make TLS connection to the DNS server
def makeTLSConn(dnsServer):
    remPort = 853
    certLoc = '/etc/ssl/certs/ca-certificates.crt'
    sockRem = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockRem.settimeout(10)
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(certLoc)
    wrappedSock = context.wrap_socket(sockRem, server_hostname=dnsServer)
    wrappedSock.connect((dnsServer, remPort))
    return wrappedSock

## Reroute the request to a TLS enabled DNS server
def reqParser(data, sndr, dnsServer):
    tlsConn = makeTLSConn(dnsServer) 
    queryRes = sendReq(tlsConn, data)
    if queryRes:
        retVal = queryRes[:6].encode("hex")
        retVal = str(retVal)[11:]
        if (int(retVal, 16) == 1):
            print "DNS request invalid"
        else:
            res = queryRes[2:]
            sock.sendto(res, sndr)
            print "DNS request successfully sent"
    else:
        print "DNS request invalid"
    
## Listen to port 53 and intercept DNS requests
if __name__ == '__main__':
    dnsServer = '8.8.8.8'   # Google's DNS
    localPort = 53
    localHost = '172.17.0.2' # Docker default subnet 
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((localHost, localPort))
        while True:
            data,sndr = sock.recvfrom(1024)
            thread.start_new_thread(reqParser,(data, sndr, dnsServer))
    except Exception, e:
        print e
        sock.close()