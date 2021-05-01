#include "EthernetSonarAPI.h"
#include "DVSFileWriter.h"
#include "DSSPParser.h"
#include <fstream>
#include "zmq.h"
#include "windows.h"
#include <iostream>
#include <string>

#define ZMQ_EXPORT __declspec(dllexport)

#define BUFFERSIZE 2048

using namespace std;

int main() {


	std::vector<int> ports;					
	std::vector<std::string> IPs;		

	CEthernetSonarAPI::FindSonar(&IPs, &ports);

	for (unsigned int i = 0; i < IPs.size(); i++) {
		std::cout << "Sonar with IP " << IPs[i] << " found." << std::endl;
	}
	if (IPs.size() == 0) {
		return -1;				
	}

	void* context = zmq_ctx_new();
	void* requester = zmq_socket(context, ZMQ_PUB);
	int rc = zmq_bind(requester, "tcp://127.0.0.1:5555");

.
	CEthernetSonarAPI Sonar(IPs[0], ports[0]);

	CDVSFileWriter DVSFile;								
	CDSSPParser parser;

	float range = 20;									    // Sonar range in meters
	int nSamples = 500;									    // Number of samples per active side and ping

	int nPeriods = 32;									    // Number of periods of transmitted pulse
	float startFreq = 320000;								// Starting frequency of transmitted pulse
	float deltaFreq = 40000;								// Delta frequency of transmitted pulse
	bool leftActive = true;									// true if left side is to be used
	bool rightActive = true;								// true if right side is to be used
	float resolution = (float)(range * 1.0) / nSamples;	    // Resolurion of the resulting image in meters

	Sonar.DSSP_SetPulseDual(nPeriods, startFreq, deltaFreq, nPeriods, startFreq, deltaFreq);

	Sonar.DSSP_SetSampling(nSamples, leftActive, rightActive, false);

	Sonar.StartRec(range);

	char sonarData[BUFFERSIZE];

	int receivedSamples = Sonar.GetData(sonarData, BUFFERSIZE);		
	while (receivedSamples <= 0) {
		Sonar.StartRec(range);
#ifdef WIN32
		Sleep(50);
#elif LINUX
		usleep(50000);
#endif
		receivedSamples = Sonar.GetData(sonarData, BUFFERSIZE);
#ifdef WIN32
		Sleep(50);
#elif LINUX
		usleep(50000);
#endif
	}

	std::cout << "Sonar connected successfully." << std::endl;

	// Create your 'test' file here
	DVSFile.Create("my_test_file.dvs", leftActive, rightActive, resolution, nSamples);

	int pings = 500;
	int n = 0;


	while (pings > 0) {
		receivedSamples = Sonar.GetData(sonarData, BUFFERSIZE);	
		if (receivedSamples > 0) {
			for (int i = 0; i < receivedSamples; i++) {			
				if (parser.Add(sonarData[i])) {
					char* data0;
					char* data1;
					int size0 = 0;
					int size1 = 0;

					parser.GetChannelData(data0, &size0, data1, &size1);


					DVSFile.AddPingData(0.0, 0.0, 0.0, 0.0, data0, size0, data1, size1);

					string result;

					for (int i = 0; i < size0; i++) {
						result += to_string((int)data0[i]) + " ";
					}
					for (int i = 0; i < size1; i++) {
						result += to_string((int)data1[i]) + " ";
					}
					const char* valueChar = result.c_str();
					int rcb = zmq_send(requester, valueChar, strlen(valueChar), 0);

					std::cout << "Size0: " << size0 << ", size1: " << size1 << ", n=" << n++ << std::endl;

					pings--;
				}
			}

		}
	}
	zmq_close(requester);
	zmq_ctx_destroy(context);
	return 0;
}