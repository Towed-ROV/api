#pragma once
//=============================================================================
// Project:       OEM
// Copyright:     DeepVision AB
// Author:        Fredrik Elmgren 
// Revision:      1.4
//-----------------------------------------------------------------------------
// Description:	  File Writer class DSSP OEM
//    
//-----------------------------------------------------------------------------
#include <iostream>
#include <fstream>
#define BYTE char

#pragma once
class CDVSFileWriter
{
public:
	CDVSFileWriter(void);
	~CDVSFileWriter(void);

	bool Create(const char* fileName, bool left, bool right, float res, int nSamples);

	void AddPingData(double lat, double lon, float speed, float heading, BYTE* pLeftData, int nLeft, BYTE* pRightData, int nRight);

	void CreateDemoFile(const char* fileName);

	std::fstream m_file;

	struct V1_FileHeader {
		float sampleRes;	// [m]
		float lineRate;		// [ ping/s ]
		int nSamples;		// Number of samples per side
		bool left;			// true if left side active
		bool right;			// true if right side active
	};

	struct V1_Position {
		double lat;	// [rad] WGS84
		double lon;	// [rad] WGS84
		float  speed;	// [m/s]
		float  heading;	// [rad]
	};
};

