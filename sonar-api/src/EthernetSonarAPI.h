#pragma once
//=============================================================================
// Project:       OEM
// Copyright:     DeepVision AB
// Author:        Johan Berneland 
// Revision:      1.1
//-----------------------------------------------------------------------------
// Description:	Ethernet Sonar Interface class.
// 
// Define WIN32 or LINUX depending on the operating system used.
//
// FindSonar can be used to find all sonars on the network.
//-----------------------------------------------------------------------------


#if defined(LINUX)
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#elif defined(WIN32)
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "Ws2_32.lib")
#endif
#include <string>
#include <iostream>
#include <vector>

const double PIx2 = 6.283185307179586476925286766559f;

typedef unsigned int U32;
typedef unsigned short U16;
typedef unsigned char U8;

#define REG_COMMAND 0x01
#define C_COMMAND_SHOOT 0x01
#define C_COMMAND_RESET 0x02
#define C_COMMAND_GET_VERSION 0x03
#define REG_PULSER_1_A 0x11
#define REG_PULSER_2_A 0x12
#define REG_PULSER_1_A_B 0x14
#define REG_PULSER_2_A_B 0x15
#define REG_POW_DET_0_A 0x20
#define REG_POW_DET_1_A 0x21
#define REG_POW_DET_2_A 0x22
#define REG_POW_DET_3_A 0x23
#define REG_POW_DET_4_A 0x24
#define REG_POW_DET_5_A 0x25
#define REG_POW_DET_6_A 0x26

class CEthernetSonarAPI
{
public:
	CEthernetSonarAPI(std::string ip, int port);
	~CEthernetSonarAPI();

	void DSSP_SetPulseDual(
		U32 nPeriods0, 			// 0-off, min 4, max TBD
		float StartFreq0,		// [Hz]
		float DeltaFreq0, 		// [Hz] positive, end frequency = StartFreq + DeltaFreq
		U32 nPeriods1, 			// 0-off, min 4, max TBD
		float StartFreq1,		// [Hz]
		float DeltaFreq1 		// [Hz] positive, end frequency = StartFreq + DeltaFreq
	);

	void DSSP_SetSampling(
		U32 nSamples,			// Number of samples per side per ping
		bool CH0Active,			// True channel one is active
		bool CH1Active,			// True channel two is active
		bool onePing			// false if continuous pinging
	);

	bool StartRec(float range);
	void StopRec();

	int GetData(char* buffer, int buffersize);

	int	m_type = 0;
	int	m_model = 0;

	static bool FindSonar(std::vector<std::string>* ip, std::vector<int>* ports);
private:

	// DSSP private functions
	void		DSSP_Run();
	void		DSSP_SetReg(U16 reg, U32 value);
	void		DSSP_Reset();

	// TCP Interfacing
	bool		OpenTCP();
	bool		CloseTCP();
	int			ReceiveTCP(char* buff, int buffSize);
	U32			m_port = 0;
	bool		m_TCPOpen = false;
	int			m_sock = -1;
	std::string m_ip;
	sockaddr_in m_remoteAddr;

	// Sonar settings
	void		SetupSonar();

	U32			m_nPeriods0 = 32;		// Channel one periods
	float		m_StartFreq0 = 320000;	// Channel one start freq [Hz]
	float		m_DeltaFreq0 = 20000;	// Channel one delta freq [Hz]
	U32			m_nPeriods1 = 32;		// Channel two periods
	float		m_StartFreq1 = 320000;	// Channel two start freq [Hz]
	float		m_DeltaFreq1 = 20000; 	// Channel two delta freq [Hz]

	bool		m_onePing = false;
	int			m_nSamples = 500;		// Number of samples per channel
	bool		m_left = true;		// Left channel (Channel one) active flag
	bool		m_right = true;		// Right channel (Channel two) active flag
	int			m_range = 10;		// Range [m]

};

