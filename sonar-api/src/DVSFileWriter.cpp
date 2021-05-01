#include "DVSFileWriter.h"


CDVSFileWriter::CDVSFileWriter(void)
{
}

CDVSFileWriter::~CDVSFileWriter(void)
{
}

bool CDVSFileWriter::Create(const char* fileName, bool left, bool right, float res, int nSamples)
{
	m_file.open(fileName, std::fstream::out);
	if (m_file.is_open()) {

		// Version 1
		unsigned int version = 1;
		m_file.write((char*)&version, sizeof(version));

		// Write header
		V1_FileHeader header;
		header.sampleRes = res;
		header.nSamples = nSamples;
		header.left = left;
		header.right = right;
		header.lineRate = float(750.0 / (nSamples * res));
		m_file.write((char*)&header, sizeof(header));

		return true;

	}
	else {
		return false;

	}
}

void CDVSFileWriter::AddPingData(double lat, double lon, float speed, float heading, BYTE* pLeftData, int nLeft, BYTE* pRightData, int nRight)
{
	// Write position data
	V1_Position pos;
	pos.heading = heading;
	pos.lat = lat;
	pos.lon = lon;
	pos.speed = speed;
	m_file.write((char*)&pos, sizeof(V1_Position));

	if (nLeft)
		m_file.write(pLeftData, nLeft);

	if (nRight)
		m_file.write(pRightData, nRight);
}

void CDVSFileWriter::CreateDemoFile(const char* fileName)
{
	const double C_PI = 3.1415926535897932384626433832795;
	const double C_ER = 6353000;	// Eart radius in [m]

	// Create a dual side file, 2x50m, 2x500 samples
	Create(fileName, true, true, 0.1f, 500);

	double lat = 56.0 / 180.0 * C_PI;	// approx 56 deg north
	double lon = 16.0 / 180.0 * C_PI;	// approx 16 deg east, in the Baltic Sea

	double dx = 1.0 * 50.0 / 750.0;

	// Add 500 ping lines
	for (int i = 0; i < 500; i++) {

		// Create ping return data, use same on both channels
		BYTE data[500];
		for (int j = 0; j < 500; j++) {
			data[j] = (i + j) % 100 + 50;
		}

		AddPingData(lat, lon, 1.0, float(180 / 180 * C_PI), data, 500, data, 500);
		lat -= dx / C_ER;	// Move dx [m] north per ping
	}


}
