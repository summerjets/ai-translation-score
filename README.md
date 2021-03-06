# AI Translation Score

## About AI Translation Score

AI Translation Score is a microservice for comparing a student's submission to a list of exemplar solutions. 

The architecture is a Python Flask app, running in Docker, with a Ngnix production-ready webserver in front.


## API Contract

### /health endpoint

* GET request

Expected Success Output

```
{
  "status": "healthy"
}
```

### /compare endpoint

* POST request

Expected Input Payload
Note: the header should contain X-Api-Key, configured in Moodle

```
{
    "submission": "user answer",
    "exemplar": ["answer 1","answer 2","answer 3","answer 4"]
}
```

Expected Success Output

```
{
  "status": "success",
  "payload": {
               "comparison_score": float,
               "accept_solution": boolean
             }
}
```

Expected Failed Output

```
{
  "status": "error",
  "payload": {
               "message": "error running AI module."
             }
}
```

Expected Unauthorized Request

```
{
	"status": "error",
	"payload": {
                "message": "invalid authentication"
               }
}
```

The above error suggests a problem with the AI scoring component and is a problem with the server itself.

Invalid input payloads are handled gracefully, with payload messages such as "payload is empty", "exemplar not in payload", "submission not in payload".


## Setup

### 1. Clone this Repository

```
## might also need to install git if you haven't already: sudo yum install git -y
git clone https://this-repo
```


### 2. Installing Docker

The application requires Docker and Docker Compose. The instructions below are tested on an Amazon Linux t2.medium EC2 instance. If you are running on significantly different hardware, it is advisable to follow the installation instructions on the Docker website.

```
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo systemctl enable docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

### 3. Running the Container

The service uses an authentication key, contained in a hidden file, .env
Update the sample file, env_example and move it to .env

```
TRANSLATION_API_KEY=yourApiKey
```

```
mv env_example .env
```

The startup script handles all setup, installation and booting.
1. Installs all package dependencies in the container
2. Runs unit tests on the AI component  
3. Starts the Flask application
4. Runs Ngnix as a production-ready webserver in front of the Flask application

```
chmod u+x run_docker.sh
sudo ./run_docker.sh
```

Upon successful completion of the script, the easiest way to check the application is available is to GET request the /health endpoint and confirm a healthy response.

```
$ curl localhost:8000/health
{"status":"healthy"}
```


### 4. Calling from elsewhere

Update the request URL in the curl request below - the sample shows the syntax for pointing at an EC2 instance.

```
curl --location --request POST 'ec2-100-27-24-27.compute-1.amazonaws.com:8000/compare' 
-H 'Content-Type: application/json' 
--data-raw '{"submission": "Caecelius is in the house match", "exemplar": "Caecelius is in his garden"}' 
--header 'x-api-key: yourApiKey'
```

which should return a success payload:

```
{"status": "success", "payload": {"comparison_score": 0.5501229176408523, "accept_solution": false}}
```


## Debugging

### Security Settings for Inbound Traffic on AWS EC2

The webservice requires an open TCP connection on port 8000 for inbound traffic. This can be configured in AWS Console if this is your deployment architecture.

### Standard Out and Error Logs

The output logs are available at
```
/dev/stdout
/dev/stderr
```

