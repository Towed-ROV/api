
//=============================================================================
// Project:       EthernetSonarAPI
// Copyright:     DeepVision AB
// Author:        Johan Berneland
// Revision:      1.1b
//
//-----------------------------------------------------------------------------
// Description:	  User example of EthernetSonarAPI
// The code connects to a Deepvision ethernet sonar of and records
// a short sonar recording with a sonar frequency of 340 kHz center frequency
// and 40 kHz chirp frequency.
//
//
// The purpouse of the example is to show how the sonar is set up and how to 
// create a .dvs file from the data received.
//
// The API has been verified on Windows 10 and on Debian 8.1.
//
//-----------------------------------------------------------------------------


//#include "EthernetSonarAPI.h"
//#include "DVSFileWriter.h"
//#include "DSSPParser.h"
//
//#define BUFFERSIZE 2048
//
//int main() {
//
//	/* --- Interfacing example ---
//	* This does not have to be done with vectors.
//	* If fixed IP is used the sonar IP and port can
//	* be hard-coded and FindSonar() doesn't have to
//	* be used.
//	*/
//	std::vector<int> ports;						// Vector that stores port data
//	std::vector<std::string> IPs;				// Vector that stores ip data
//
//	CEthernetSonarAPI::FindSonar(&IPs, &ports);	// Find all DeepVision EthernetSonars on the network
//
//	for (unsigned int i = 0; i < IPs.size(); i++) {
//		std::cout << "Sonar with IP " << IPs[i] << " found." << std::endl;		// Print the IPs of all Sonars found
//	}
//	if (IPs.size() == 0) {
//		return -1;								// Return -1 if no sonars were found
//	}
//
//	// Declase a EthernetSonar object using the first sonar found
//	// This could be hard-coded if the IP of the sonar is known.
//	CEthernetSonarAPI Sonar(IPs[0], ports[0]);
//
//	CDVSFileWriter DVSFile;									// The DVS File writer class
//	CDSSPParser parser;
//
//	float range = 30;									// Sonar range in meters
//	int nSamples = 500;									// Number of samples per active side and ping
//
//	int nPeriods = 32;									// Number of periods of transmitted pulse
//	float startFreq = 320000;								// Starting frequency of transmitted pulse
//	float deltaFreq = 40000;								// Delta frequency of transmitted pulse
//	bool leftActive = true;									// true if left side is to be used
//	bool rightActive = true;								// true if right side is to be used
//	float resolution = (float)(range * 1.0) / nSamples;	// Resolurion of the resulting image in meters
//
//
//	// Set up the pulse characteristics.
//	Sonar.DSSP_SetPulseDual(nPeriods, startFreq, deltaFreq, nPeriods, startFreq, deltaFreq);
//
//	// Set up the sampling characteristics.
//	Sonar.DSSP_SetSampling(nSamples, leftActive, rightActive, false);
//
//	// Start the recording.
//	Sonar.StartRec(range);
//
//	// Buffer to receive sonar data which is to be written to file.
//	char sonarData[BUFFERSIZE];
//
//	int receivedSamples = Sonar.GetData(sonarData, BUFFERSIZE);		// Get data from the EthernetSonar
//	while (receivedSamples <= 0) {
//		Sonar.StartRec(range);
//#ifdef WIN32
//		Sleep(50);
//#elif LINUX
//		usleep(50000);
//#endif
//		receivedSamples = Sonar.GetData(sonarData, BUFFERSIZE);
//#ifdef WIN32
//		Sleep(50);
//#elif LINUX
//		usleep(50000);
//#endif
//	}
//
//	std::cout << "Sonar connected successfully." << std::endl;
//
//	// Set up the file writer with the filename "Example.dvs" and the settings we have sent to the sonar.
//	DVSFile.Create("Example.dvs", leftActive, rightActive, resolution, nSamples);
//
//	/*
//	 * We will receive 100 pings and add them to a .dvs file, using the DSSPParser.
//	*/
//	int pings = 100;
//	int n = 0;
//
//	while (pings > 0) {
//		receivedSamples = Sonar.GetData(sonarData, BUFFERSIZE);	// Get data from the EthernetSonar
//		if (receivedSamples > 0) {
//			for (int i = 0; i < receivedSamples; i++) {			// Parse the incoming data stream from TCP
//				// Add the received data to the parser.
//				// The parser.Add() will return true when a complete ping has been added.
//				if (parser.Add(sonarData[i])) {
//					// A complete ping has been added to the parser. We will add it to the
//					// .dvs file using the DVSFileWriter.
//					char* data0;
//					char* data1;
//					int size0 = 0;
//					int size1 = 0;
//
//					// Get the sonar data from the parser
//					parser.GetChannelData(data0, &size0, data1, &size1);
//
//					// Add the sonar data to the file, skipping positioning data for simplicity
//					DVSFile.AddPingData(0.0, 0.0, 0.0, 0.0, data0, size0, data1, size1);
//
//					std::cout << "Size0: " << size0 << ", size1: " << size1 << ", n=" << n++ << std::endl;
//					pings--;
//				}
//			}
//		}
//	}
//
//	return 0;
//}
