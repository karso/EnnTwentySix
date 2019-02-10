# Project Title

1. DNS over TLS proxy

### Prerequisites

1. Docker 
```
https://www.docker.com/
```

### How to run

1. Go inside N26 directory
```
cd N26
```

2. Create docker image 
```
docker build -t dot-proxy-server .
```

3. Start the container
```
docker run -it dot-proxy-server
```
### Verify
To verify, from another terminal, run
```
docker exec -it {container ID} nslookup chess.com
```
If everything works; you'll see a message as below and get the result of your query.
```
DNS request successfully sent
```

### 	Concerns
Not every DNS server / service provider supports this.

TLS has it's own set of vulnerabilities. 

### Use in MicroService Architecture
In a microservice architecture, to implement service discovery, if you are using a DNS based aproach, this applcation can secure the communication to your DNS server. 


### Improvements
Multiple DOT servers.

Docker subnet agnost.

IP white / black list.

## Versioning

Version 1.0

## Authors

* **Soumitra Kar**
