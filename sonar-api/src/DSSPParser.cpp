#include "DSSPParser.h"

CDSSPParser::CDSSPParser() {};
CDSSPParser::~CDSSPParser() {};


// Add streamed data coming from the sonar. 
bool CDSSPParser::Add(char b) {
	switch (p_state) {
	case STATE_IDLE:
		if ((b & 0xFF) == 0xFE) {
			p_state = STATE_START;
			p_nData = 0;
			p_CH0 = true;
			p_ChkSum = 0;
		}
		p_ChkSum += b;
		break;
	case STATE_START:
		if (b == 0x05) {
			p_state = STATE_SIZE_H;
		}
		else {
			p_state = STATE_IDLE;
		}
		p_ChkSum += b;
		break;
	case STATE_SIZE_H:
		p_size = b << 8;
		p_state = STATE_SIZE_L;
		p_ChkSum += b;
		break;
	case STATE_SIZE_L:
		p_size = (p_size & 0xFF00) | (b & 0x00FF);
		p_state = STATE_TYPE;
		p_ChkSum += b;
		break;
	case STATE_TYPE:
		p_type = b;
		p_state = STATE_SEQUENCE;
		p_ChkSum += b;
		break;
	case STATE_SEQUENCE:
		p_sequence = b;
		p_state = STATE_SIDES;
		p_ChkSum += b;
		break;
	case STATE_SIDES:
		p_0Active = b & 0x01;
		p_1Active = b & 0x02;
		p_state = STATE_TIME_H;
		p_ChkSum += b;
		break;
	case STATE_TIME_H:
		p_time = b << 8;
		p_state = STATE_TIME_L;
		p_ChkSum += b;
		break;
	case STATE_TIME_L:
		p_time = (p_time & 0xFF00) | b;
		p_state = STATE_DATA;
		p_ChkSum += b;
		break;
	case STATE_DATA:
		p_ChkSum += b;
		if (p_0Active && p_1Active) {
			if (p_CH0) {
				p_0Data[p_nData / 2] = b;
			}
			else {
				p_1Data[(p_nData / 2)] = b;
			}
			p_CH0 = !p_CH0;
		}
		else if (p_0Active) {
			p_0Data[p_nData] = b;
		}
		else if (p_1Active) {
			p_1Data[p_nData] = b;
		}
		if (p_nData > p_size - 6) {
			p_state = STATE_CHK;
			if (p_0Active && p_1Active) {
				p_nData = (p_nData / 2) + 1;
			}
			else {
				p_nData++;
			}
		}
		else {
			p_nData++;
		}
		break;
	case STATE_CHK:
		p_state = STATE_IDLE;
		if (p_ChkSum == b) {
			p_ChkSum = 0;
			return true;
		}
		p_ChkSum = 0;
		break;
	}
	return false;
}


// Get data after Add() has returned true.
void CDSSPParser::GetChannelData(char*& data0, int* size0, char*& data1, int* size1) {
	data0 = p_0Data;
	data1 = p_1Data;
	if (p_0Active) {
		*size0 = p_nData;
	}
	else {
		*size0 = 0;
	}
	if (p_1Active) {
		*size1 = p_nData;
	}
	else {
		*size1 = 0;
	}
}
