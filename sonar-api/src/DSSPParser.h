#pragma once
//=============================================================================
// Project:       OEM
// Copyright:     DeepVision AB
// Author:        Fredrik Elmgren 
// Revision:      1.1
//-----------------------------------------------------------------------------
// Description:	  DSSP Parser class
//    
//-----------------------------------------------------------------------------

class CDSSPParser
{
public:
	CDSSPParser();
	~CDSSPParser();

	bool Add(char b);
	void GetChannelData(char*& data0, int* size0, char*& data1, int* size1);

private:

	int p_size = 0;
	char p_type;
	char p_sequence;
	bool p_0Active;
	bool p_1Active;

	int p_time;

	char p_0Data[2048];
	char p_1Data[2048];
	int p_nData = 0;
	bool p_CH0 = true;

	unsigned char p_ChkSum = 0;

	enum State { STATE_IDLE, STATE_START, STATE_SIZE_H, STATE_SIZE_L, STATE_TYPE, STATE_SEQUENCE, STATE_SIDES, STATE_TIME_H, STATE_TIME_L, STATE_DATA, STATE_CHK };
	State p_state = STATE_IDLE;
};