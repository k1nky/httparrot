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
* *echo* - echo message types (list): headers - include request headers, body - include request body, query - include request line, client - include client connection, all - include all, none - no include
* *header* - response headers (list)
* *body* - echo response body
* *version* - HTTP version, default 1.1
* *time* - insert current time into echo response body
* *silent* - enable silent mode
* *status* - response code status

#### Examples

* `$ ./httparrot.py -p 8010 -v 1.0`

<pre>
$ curl -v localhost:8010/test?q=1

> GET /test?q=1 HTTP/1.1
> Host: localhost:8010
> User-Agent: curl/7.52.1
> Accept: */*
> 
<i># -v 1.0</i>
< <b>HTTP/1.0</b> 200 OK	
< Server: BaseHTTP/0.6 Python/3.5.3
< Date: Thu, 28 Nov 2019 19:07:59 GMT
< Content-Type: text/html
< 
</pre>

* `$ ./httparrot.py -p 8010 --body OK --echo headers --echo query --header "Connection: keep-alive" "Content-Type: text/html" --time`

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
<i># --header "Connection: keep-alive"</i>
< <b>Connection: keep-alive</b>
<i># --header "Content-Type: text/html"</i>
< <b>Content-Type: text/html</b> 
< Content-Length: 96
< 

<i># --echo headers</i>
<b>Host: localhost:8010</b>
<b>User-Agent: curl/7.52.1</b>
<b>Accept: */*</b>

<i># --echo query</i>
<b>GET /test?q=1 HTTP/1.1</b>
<i># --time</i>
<b>1574968079</b>
<i># --body OK</i>
<b>OK</b>
</b>
</pre>

* `$ ./httparrot.py -s 301 --header "Location: http://example.com"`

<pre>
$ curl -L -v localhost:8000/any-query --silent

> GET /any-query HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/7.52.1
> Accept: */*
> 
<i># -s 301</i>
< HTTP/1.1 <b>301</b> Moved Permanently
< Server: BaseHTTP/0.6 Python/3.5.3
< Date: Sat, 07 Dec 2019 08:35:03 GMT
<i># --header "Location: http://example.com"</i>
< <b>Location: http://example.com</b>
< Content-Length: 1
< 
...
* Issue another request to this URL: 'http://example.com'
* Rebuilt URL to: http://example.com/
*   Trying 93.184.216.34...
* TCP_NODELAY set
* Connected to example.com (93.184.216.34) port 80 (#1)
> GET / HTTP/1.1
> Host: example.com
> User-Agent: curl/7.52.1
> Accept: */*
> 
< HTTP/1.1 200 OK
...

</pre>
