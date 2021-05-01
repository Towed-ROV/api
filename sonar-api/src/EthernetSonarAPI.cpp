

#include "EthernetSonarAPI.h"

CEthernetSonarAPI::CEthernetSonarAPI(std::string ip, int port)
{
	m_ip = ip;
	m_port = port;
}

CEthernetSonarAPI::~CEthernetSonarAPI()
{
#if defined(LINUX)
	close(m_sock);
#elif defined(WIN32)
	closesocket(m_sock);
	WSACleanup();
#endif
}


/* Start Sonar recording with given range.*/
bool CEthernetSonarAPI::StartRec(float range)
{
	if (range >= 10 && range <= 500)
		m_range = range;
	else
		m_range = 10;

	if (OpenTCP())
	{
		SetupSonar();
		DSSP_Run();
		return true;
	}
	return false;
}

/* Ends the recording. */
void CEthernetSonarAPI::StopRec()
{
	CloseTCP();
}

/* Receive data from sonar. */
int CEthernetSonarAPI::GetData(char* buffer, int buffersize) {
	if (m_TCPOpen) {
		return ReceiveTCP(buffer, buffersize);
	}
	else {
		return -1;
	}
}

/* Set the pulse characteristics of the two sonar channels.
* Channel one is the left channel as standard on side scan sonars.
*/
void CEthernetSonarAPI::DSSP_SetPulseDual(
	U32		nPeriods0,	// Channel one number of output periods of ping 
	float	StartFreq0,	// Channel one start frequency in [Hz] 
	float	DeltaFreq0,	// Channel one chirp delta frequency in [Hz], must be positive
	U32		nPeriods1,	// Channel two number of output periods of ping 
	float	StartFreq1,	// Channel two start frequency in [Hz] 
	float	DeltaFreq1	// Channel two chirp delta frequency in [Hz], must be positive
)
{
	m_nPeriods0 = nPeriods0;
	m_StartFreq0 = StartFreq0;
	m_DeltaFreq0 = DeltaFreq0;
	m_nPeriods1 = nPeriods1;
	m_StartFreq1 = StartFreq1;
	m_DeltaFreq1 = DeltaFreq1;
}

/* Set the sampling characteristics of the sonar.
* The resolution of the sonar data can be calculated as the range
* devided by the number of samples.
* Channel one is the left channel as standard on side scan sonars.
*/
void CEthernetSonarAPI::DSSP_SetSampling(
	U32 nSamples,			// Number of samples per side and ping
	bool CH0Active,			// True channel one is active
	bool CH1Active,			// True channel two is active
	bool onePing			// false if continuous pinging
)
{
	m_nSamples = nSamples;
	m_left = CH0Active;
	m_right = CH1Active;
	m_onePing = onePing;
}

/* ---------- Static functions ---------- */

// Function for finding all DepVision Ethernet Sonars connected to the network.
bool CEthernetSonarAPI::FindSonar(std::vector<std::string>* ip, std::vector<int>* ports)
{
	bool retVal = false;
#if defined(LINUX)
	int sock;
#elif defined(WIN32)
	SOCKET sock;
	WSADATA wsa;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
	{
		exit(EXIT_FAILURE);
	}
#endif
	sock = socket(AF_INET, SOCK_DGRAM, 0);
	int enabled = 1;
	if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, (char*)&enabled, sizeof(&enabled)) < 0)
	{
		return retVal;
	}

	struct sockaddr_in remoteAddr, SenderAddr;

	struct timeval iTimeout;
	iTimeout.tv_sec = 1;
	iTimeout.tv_usec = 0;
	if (setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (char*)&iTimeout, sizeof(iTimeout)) < 0)
	{
		return retVal;
	}
	remoteAddr.sin_family = AF_INET;
	remoteAddr.sin_port = htons(4626);
	remoteAddr.sin_addr.s_addr = htonl(INADDR_BROADCAST);
	char msg[] = { 0x56, 0x00 };
	if (sendto(sock, (const char*)msg, 1, 0, (sockaddr*)&remoteAddr, sizeof(remoteAddr)) < 0) {
		return retVal;
	}
#if defined(LINUX)
	usleep(200000);
#elif defined(WIN32)
	Sleep(200);
#endif
	char RecvBuf[1024];
	int BufLen = 1024;

#ifdef LINUX
	socklen_t SenderAddrSize = sizeof(SenderAddr);
#elif defined(WIN32)
	int SenderAddrSize = sizeof(SenderAddr);
#endif

	int iResult = recvfrom(sock, RecvBuf, BufLen, 0, (sockaddr*)&SenderAddr, &SenderAddrSize);

	int i = 0;
	while (iResult > i) {
		if ((RecvBuf[i + 0] == 0x57) && (iResult >= i + 8)) {
			unsigned int ServiceId = (RecvBuf[i + 2] << 24) | (RecvBuf[i + 3] << 16) | (RecvBuf[i + 4] << 8) | RecvBuf[i + 5];
			unsigned port = (RecvBuf[i + 6] << 8) | RecvBuf[i + 7];

			if (ServiceId == 0xD0010101) {
				char iAddr[64];
#if defined(LINUX)
				inet_ntop(AF_INET, &(SenderAddr.sin_addr), iAddr, 64);
#elif defined(WIN32)
				InetNtop(AF_INET, &(SenderAddr.sin_addr), iAddr, 64);
#endif
				std::string addr = iAddr;
				ip->push_back(addr);
				ports->push_back(port);
				retVal = true;
			}
			i = 0;
		}
		iResult = recvfrom(sock, RecvBuf, BufLen, 0, (sockaddr*)&SenderAddr, &SenderAddrSize);
	}
	return retVal;
}

/* ---------- Private functions ---------- */

void CEthernetSonarAPI::DSSP_Run()
{
	DSSP_SetReg(0x01, 0x80);
}

void CEthernetSonarAPI::SetupSonar()
{
	U32 PD_Mode = 1;
	U32 PD_nSamples = float(m_range) / 0.1781303;
	unsigned int PD_ActiveChannels = 0x0;
	if (m_left)
		PD_ActiveChannels |= 0x01;
	if (m_right)
		PD_ActiveChannels |= 0x02;
	if (m_onePing) {
		DSSP_SetReg(REG_POW_DET_0_A, ((0x1 << 16) | 0x03));
	}
	double fSample = 80e6 / 19.0;
	double fs = 200e3;
	unsigned int nSkip = 2048 / PD_nSamples;
	nSkip += fSample / fs * m_nPeriods0 / PD_nSamples;
	DSSP_SetReg(REG_POW_DET_1_A, (PD_nSamples << 16) | (PD_ActiveChannels << 3) | (PD_Mode));
	DSSP_SetReg(REG_POW_DET_5_A, (nSkip << 16) | m_nSamples);
	U32 F01 = (U32)(m_StartFreq0 * 0.0131072f + 0.5);
	U32 dfr1 = (U32)(m_DeltaFreq0 * 1.666667f / m_nPeriods0 + 0.5);
	DSSP_SetReg(REG_PULSER_1_A, (dfr1 << 16) | (0xFFFF & F01));
	DSSP_SetReg(REG_PULSER_2_A, ((0x03FF & m_nPeriods0) << 16));
	U32 F02 = (U32)(m_StartFreq1 * 0.0131072f + 0.5);
	U32 dfr2 = (U32)(m_DeltaFreq1 * 1.666667f / m_nPeriods1 + 0.5);
	DSSP_SetReg(REG_PULSER_1_A_B, (dfr2 << 16) | (0xFFFF & F02));
	DSSP_SetReg(REG_PULSER_2_A_B, ((0x03FF & m_nPeriods1) << 16));
}

void CEthernetSonarAPI::DSSP_SetReg(U16 reg, U32 value)
{
	U8 txBuff[8];
	txBuff[0] = 0xF5;
	txBuff[1] = U8((reg >> 8) & 0xFF);
	txBuff[2] = U8((reg) & 0xFF);
	txBuff[3] = U8((value >> 24) & 0xFF);
	txBuff[4] = U8((value >> 16) & 0xFF);
	txBuff[5] = U8((value >> 8) & 0xFF);
	txBuff[6] = U8((value) & 0xFF);
	txBuff[7] = 0;
	for (int i = 0; i < 7; i++)
		txBuff[7] += txBuff[i];
	int n = sendto(m_sock, (const char*)txBuff, 8, 0, (sockaddr*)&m_remoteAddr, sizeof(m_remoteAddr));
}

bool CEthernetSonarAPI::OpenTCP()
{
	unsigned sock_in_len = sizeof(sockaddr_in);
	m_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	struct timeval iTimeout;
	iTimeout.tv_sec = 1;
	iTimeout.tv_usec = 0;
	setsockopt(m_sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&iTimeout, sizeof(iTimeout));
	int enable = 1;
	setsockopt(m_sock, SOL_SOCKET, SO_REUSEADDR, (const char*)&enable, sizeof(int));
	m_remoteAddr.sin_family = AF_INET;
	m_remoteAddr.sin_port = htons(m_port);
	if (inet_pton(AF_INET, m_ip.c_str(), &m_remoteAddr.sin_addr.s_addr) == 0) {
		return false;
	}
	int iResult = connect(m_sock, (sockaddr*)&m_remoteAddr, sizeof(m_remoteAddr));
	if (iResult == -1) {
#if defined(LINUX)
		close(m_sock);
#elif defined(WIN32)
		closesocket(m_sock);
#endif
		m_sock = -1;
		m_TCPOpen = false;
		return false;
	}
	U8 buff[3];
	int n = recv(m_sock, (char*)buff, 3, 0);
	if (n != 3) {
		m_TCPOpen = false;
#if defined(LINUX)
		close(m_sock);
#elif defined(WIN32)
		closesocket(m_sock);
#endif
		return false;
	}
	m_model = buff[2];
	m_type = buff[1];
	m_TCPOpen = true;
	return true;
}

int CEthernetSonarAPI::ReceiveTCP(char* buff, int buffSize)
{
	int n = recv(m_sock, buff, buffSize, 0);
	return n;
}

bool CEthernetSonarAPI::CloseTCP()
{
	if (m_TCPOpen) {
#if defined(LINUX)
		close(m_sock);
#elif defined(WIN32)
		closesocket(m_sock);
#endif
		m_TCPOpen = false;
	}
	return true;
}
