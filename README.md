
# Adapter Service Architecture

<img align="center" width="310" height="90" src="AdapterServiceArchitecture.png">

# Checking out the Adatper Service branch

Fill in your Gerrit username for `<user>`.

```
git clone -b dev/hoa.nguyen/sal-modularization ssh://<user>@ci-gerrit.vse.rdlabs.hpecorp.net:29418/omni.git

```

Adapter Service code is under adapter-service/sdl-service-nitro

# Building the Adapter Service

## Building the code

```
cd adapter-service/sdl-service-nitro
```

```
mvn install
mvn -DskipTests=true install
```

## Building the tests

```
cd adapter-service/sdl-service-nitro/tests
mvn install
```

# Running the Adapter Service

Copy the Adapter Service to the target OV appliance (DCS or Composer)

```
scp sdl-ws/target/sdl-ws-5.30.9999999-SNAPSHOT-with-dependencies.jar  $OV_IP:/var/tmp
ssh root@$OV_IP
cd /var/tmp
java -jar sdl-ws-5.30.9999999-SNAPSHOT-with-dependencies.jar &
```

It will initialize Spring dependencies, wait for it to say:
__ Sdl server started __
 
This means the sdl service is ready to accept the requests at different endpoints at the given port or the default port.
 
Once the service is up, you can hit it with a simple command:
```
curl   http://localhost:8080/rest/sdl -- from the appliance
curl   http://$OV_IP:8080/rest/sdl -- from the laptop

```

# Running Adapter Service Component tests
 

## Set up DCS
 If you want to run the test on DCS appliance, get a new OV VM to start an SE schematic:

```
dcs status
dcs start /dcs/schematic/synergy_1encl_arista_nitro cold
curl -k -X POST -H "X-API-Version:300" https://localhost/rest/appliance/tech-setup
```
 

## Build and copy tests
In your sandbox -

Git pull to get the latest from remote branch

```
git pull origin dev/hoa.nguyen/sal-modularization
```

### Build the tests

```
cd adapter-service/sdl-service-nitro/tests
mvn install
scp -r sdl-service-integration-tests root@$OV_IP:/var/tmp
scp sdl-service-functional-tests/target/sdl-service-functional-tests-5.30.9999999-SNAPSHOT-with-dependencies.jar $OV_IP:/var/tmp
```
 
On your OV appliance, start the SDL Nitro jar. Follow instructions the in section "Running Adapter Service on OV appliance" above.
 

### Setup the test config
On the OV appliance -
```
cd /var/tmp
cd sdl-service-integration-tests
```
Edit the cfg.Nitro with following data and leave everything same:

```
ENC_CONFIG_INDEX = 0

Leave this 0 for test against SE. This is the index for the enclosure_configs dictionary
APPLIANCE_IP_ADDRESS = 'vcaldevxx.us.rdlabs.hpecorp.net'

Replace this value with your appliance hostname or IP address
DCS = True [This field is removed if your branch is rebased on April 30]

Set to True if running test on DCS.  If running on hardware, leave it as False.
'IBS' : '3'
This is the Nitro interconnect bay set number in your appliance.  The test currently only works with dual unit, so pick the bayset that has 2 Nitro units in both sideA and sideB.  For DCS schematic above, this should be 3.
'httpPrefix' : 'https://['

Since we are dealing with IPv6 address on authenticated connection, so need to replace with https://[          
'emInterface' : '%bond0]'

For hardware appliance, use '%bond0]'
For dcs appliance, use '%eth2]'
'icmInterface' : '%bond0'

For hardware appliance, use '%bond]'
For dcs appliance, use '%eth2'
logLevel = logging.INFO

If you want debug logging, change to logging.DEBUG.  Otherwise, leave it as is
``` 

Make sure your Tbird enclosure is only discovered by OV, no LE existed.


## Run the Adapter Service Component Tests
To run the tests, login to the OV appliance and the following environment variables can  be set if your target directory or service port is different than the default. Otherwise, you don't need to set these.

```
export PYTHON_TEST_PATH= “<PATH of the test dir>” //path of the python tests. Default is /var/tmp/sdl-service-integration-tests”
export SERVICE_PORT=”8080" //default is 8080 if it’s not set
cd /var/tmp
java -jar sdl-service-functional-tests-5.30.9999999-SNAPSHOT-with-dependencies.jar com.hp.ci.mgmt.sdl.tests.suites.ClaimAndConfigureTestSuite
```
(C) Copyright 2020 Hewlett Packard Enterprise Development LP
