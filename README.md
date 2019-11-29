#### About

**HTTParrot** is http echo server which can be used when debugging, configure or testing your infrastructure. The utility is built on native Python3 classes and does not need any dependencies.

#### Usage

<pre>
httparrot.py [-h] [--port PORT] [--address ADDRESS]
                    [--echo [TYPE [TYPE ...]]]
                    [--header [HEADER [HEADER ...]]]
                    [--body [BODY [BODY ...]]] [--status STATUS]
                    [--version {1.0,1.1,2}] [--time] [--silent]
</pre>

Arguments: 

* *port* - server listen port, default 8000
* *address* - server address, default localhost
* *echo* - list of  echo message types: headers - include request headers in echo response, body - include request body in echo response, query - include request line in echo response, all - include all in echo response, none - no include
* *header* - list extending the response headers
* *body* - echo response body
* *version* - HTTP version, default 1.1
* *time* - include current time in echo response body
* *silent* - silent mode
* *status* - response code status

#### Examples

$ ./httparrot.py -p 8010 -v 1.0

<pre>
$ curl -v localhost:8010/test?q=1

> GET /test?q=1 HTTP/1.1
> Host: localhost:8010
> User-Agent: curl/7.52.1
> Accept: */*
> 
< HTTP/1.0 200 OK
< Server: BaseHTTP/0.6 Python/3.5.3
< Date: Thu, 28 Nov 2019 19:07:59 GMT
< Content-Type: text/html
< 
</pre>

$ ./httparrot.py -p 8010 --body OK --echo headers query --header "Connection: keep-alive" "Content-Type: text/html" --time

<pre>
$ curl -v localhost:8010/test?q=1

> GET /test?q=1 HTTP/1.1
> Host: localhost:8010
> User-Agent: curl/7.52.1
> Accept: */*
> 
< HTTP/1.1 200 OK
< Server: BaseHTTP/0.6 Python/3.5.3
< Date: Thu, 28 Nov 2019 19:07:59 GMT
< Connection: keep-alive
< Content-Type: text/html
< Content-Length: 96
< 
Host: localhost:8010
User-Agent: curl/7.52.1
Accept: */*

GET /test?q=1 HTTP/1.1
1574968079
OK

</pre>


