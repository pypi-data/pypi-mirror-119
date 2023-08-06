// Palanteer recording library
// Copyright (C) 2021, Damien Feneyrou <dfeneyrou@gmail.com>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

// This file implements the socket connection to a program and its protocol, in a dedicated thread.

// System
#include <string.h>
#include <stdio.h>
#include <chrono>
#include <algorithm>
#include <iterator>

// Internal
#include "bsOs.h"
#include "bsVec.h"
#include "cmCnx.h"
#include "cmConst.h"
#include "cmCompress.h"

#ifndef PL_GROUP_CLIENTRX
#define PL_GROUP_CLIENTRX 0
#endif

#ifndef PL_GROUP_CLIENTTX
#define PL_GROUP_CLIENTTX 0
#endif


constexpr int SUPPORTED_MIN_PROTOCOL = 0;
constexpr int SUPPORTED_MAX_PROTOCOL = 1;

cmCnx::cmCnx(cmInterface* itf, int port) :
    _itf(itf), _port(port), _doStopThreads(0)
{
#if defined(_WIN32)
    // Windows special case: initialize the socket library
    WSADATA wsaData;
    int wsaInitStatus = WSAStartup(MAKEWORD(2,2), &wsaData);
    plAssert(wsaInitStatus==0, "Unable to initialize winsock", wsaInitStatus);
#endif

    // Reception buffer
    plAssert(_recBufferSize>=256);
    _parseTempStorage.reserve(256);
    _recBuffer = new u8[_recBufferSize];
    plAssert(_recBuffer);

    // Transmission buffer
    _txBuffer.reserve(MAX_REMOTE_COMMAND_BYTE_SIZE);
    _txBufferState.store(0);

    // Launch the threads
    _threadClientTx = new std::thread([this]{ this->runTxToClient(); });
    plAssert(_threadClientTx);
    _threadClientRx = new std::thread([this]{ this->runRxFromClient(); });
    plAssert(_threadClientRx);

    // Wait for both threads readiness
    std::unique_lock<std::mutex> lk(_threadInitMx);
    _threadInitCv.wait(lk, [this] { return _txIsStarted && _rxIsStarted; });
}


cmCnx::~cmCnx(void)
{
    _doStopThreads.store(1);
    _threadWakeUpCv.notify_one(); // Breaks the client tx loop
    _threadClientTx->join();
    _threadClientRx->join();
    delete   _threadClientTx;
    delete   _threadClientRx;
    delete[] _recBuffer;
#if defined(_WIN32)
    WSACleanup();
#endif
}


void
cmCnx::injectFile(const bsString& filename)
{
    bsString* s = _msgInjectFile.t1GetFreeMsg();
    if(!s) return;
    *s = filename;
    _msgInjectFile.t1Send();
}


// ==============================================================================================
// Transmission to client
// ==============================================================================================

bsVec<u8>*
cmCnx::getTxBuffer (void)
{
    int zero = 0;
    return _txBufferState.compare_exchange_strong(zero, 1)? &_txBuffer : 0;
 }


void
cmCnx::sendTxBuffer(void)
{
    _txBufferState.store(2);
    _threadWakeUpCv.notify_one();
}


void
cmCnx::runTxToClient(void)
{
    plDeclareThread("Client Tx");
    plgText(CLIENTTX, "State", "Start of client transmission thread");

    {
        // Notify the initialization that transmission thread is ready
        std::lock_guard<std::mutex> lk(_threadInitMx);
        _txIsStarted = true;
        _threadInitCv.notify_one();
    }

    // Loop until end of program
    while(!_doStopThreads.load()) {

        // Wait for a buffer to be sent
        std::unique_lock<std::mutex> lk(_threadWakeUpMx);
        _threadWakeUpCv.wait(lk, [this] { return _doStopThreads.load() || _txBufferState.load()==2; });
        if(_doStopThreads.load()) break; // End of program

        // Is there a connection?
        if(_clientSocket==bsSocketError) {
            _txBuffer.clear();
            _txBufferState.store(0); // Free for next command to send
            _itf->notifyCommandAnswer(plPriv::plRemoteStatus::PL_ERROR, "No socket");
            continue;
        }

        // Is control enabled? (else no need to send because the app will not listen)
        if(_tlvs.values[PL_TLV_HAS_NO_CONTROL]) {
            _txBuffer.clear();
            _txBufferState.store(0); // Free for next command to send
            _itf->notifyCommandAnswer(plPriv::plRemoteStatus::PL_ERROR, "Control is disabled on application side");
            continue;
        }

        // Sending. Loop on sending call until fully sent
        int offset = 0;
        while(offset<_txBuffer.size()) {
            int qty = send(_clientSocket, (const char*)&_txBuffer[offset], _txBuffer.size()-offset, 0);
            if(qty<=0) {
                _itf->notifyCommandAnswer(plPriv::plRemoteStatus::PL_ERROR, "Bad socket sending");
                break;
            }
            offset += qty;
        }
        _txBufferState.store(0); // Free the request buffer for the next one

    } // End of connection loop
    plgText(CLIENTTX, "State", "End of data reception thread");
}


// ==============================================================================================
// Reception from client
// ==============================================================================================

#if _WIN32
#define CLOSE_SOCKET(s) closesocket(s)
#else
#define CLOSE_SOCKET(s) close(s)
#endif

void
cmCnx::dataReceptionLoop(FILE* fd)
{
    // Initialize the transport layer (reception of metadata from the client)
    bool initStatus = initializeTransport(fd);

    // Parsing failed?
    if(!initStatus) {
        _itf->log(LOG_ERROR, "Client reception: Unable to initialize the transport layer");
        plgText(CLIENTRX, "State", "Error, Unable to initialize the transport layer");
        if(fd) {
            _itf->notifyErrorForDisplay(ERROR_IMPORT, bsString("Unable to decode the file header.\nPlease check that it is a valid .pltraw file."));
        }
    }
    // Check the protocol
    else if(_tlvs.values[PL_TLV_PROTOCOL]<SUPPORTED_MIN_PROTOCOL) {
        initStatus = false;
        _itf->log(LOG_ERROR, "Client reception: the instrumentation library is too old and shall be updated");
        plgText(CLIENTRX, "State", "Error, the instrumentation library is too old and shall be updated");
        _itf->notifyErrorForDisplay(ERROR_IMPORT, bsString("The instrumentation library is too old and shall be updated"));
    }
    else if(_tlvs.values[PL_TLV_PROTOCOL]>SUPPORTED_MAX_PROTOCOL) {
        initStatus = false;
        _itf->log(LOG_ERROR, "Client reception: the instrumentation library is too recent. The server shall be updated");
        plgText(CLIENTRX, "State", "Error, the instrumentation library is too recent. The server shall be updated");
        _itf->notifyErrorForDisplay(ERROR_IMPORT, bsString("The instrumentation library is too recent. The server shall be updated"));
    }
    if(!initStatus) {
        if(fd) {
            fclose(fd);
        } else {
            CLOSE_SOCKET(_clientSocket);
            _clientSocket = bsSocketError;
        }
        return;
    }

    // Client reception loop
    if(!_itf->notifyRecordStarted(_appName, _buildName, _timeTickOrigin, _tickToNs, _tlvs)) {
        plgText(CLIENTRX, "State", "Error, Unable to begin the record");
        // Error message is already handled inside main
        if(fd) {
            fclose(fd);
        } else {
            CLOSE_SOCKET(_clientSocket);
            _clientSocket = bsSocketError;
        }
        return;
    }

    plgText(CLIENTRX, "State", "Start data reception");
    int deltaRecordFactor = fd? 5 : 1; // No need to have "real time" display when we import
    bool isRecordOk         = true;
    bool areNewDataReceived = false;
    while(!_doStopThreads.load()) {

        // Manage the periodic live display update
        bsUs_t currentTime = bsGetClockUs();
        if(areNewDataReceived && (currentTime-_lastDeltaRecordTime)>=deltaRecordFactor*cmConst::DELTARECORD_PERIOD_US) {
            if(_itf->createDeltaRecord()) {
                _lastDeltaRecordTime = currentTime;
            }
            areNewDataReceived = false;
        }

        // Read the data
        int qty;
        if(fd) {
            qty = (int)fread(_recBuffer, 1, _recBufferSize, fd);
            if(qty<=0) break;
        }
        else {
            qty = recv(_clientSocket, (char*)_recBuffer, _recBufferSize, 0);
            if((errno==EAGAIN || errno==EWOULDBLOCK) && qty<0) continue; // Timeout on reception (empty)
            else if(qty<1)                                     break;    // Client is disconnected
        }

        if(!parseTransportLayer(_recBuffer, qty)) {                      // Parse the received content
            _itf->log(LOG_ERROR, "Client reception: Error in parsing the received data");
            plgText(CLIENTRX, "State", "Error in parsing the received data");
            isRecordOk = false; // Corrupted record
            break;
        }
        else areNewDataReceived = true;
    } // End of reception loop

    plgText(CLIENTRX, "State", "End of data reception");
    _itf->notifyRecordEnded(isRecordOk);

    if(fd) {
        fclose(fd);
    }
    else {
        CLOSE_SOCKET(_clientSocket);
        _clientSocket = bsSocketError;
        _itf->log(LOG_DETAIL, "Client reception: Closed client connection");
    }
    plgText(CLIENTRX, "State", "End of recording");
}


void
cmCnx::runRxFromClient(void)
{
    plDeclareThread("Client Rx");
    plgText(CLIENTRX, "State", "Start of client reception thread");

    // Creation of the TCP connection
    plgBegin(CLIENTRX, "Create the listening socket");
    bsSocket_t sockfd = (bsSocket_t)socket(AF_INET,SOCK_STREAM,0);
    if(!bsIsSocketValid(sockfd)) {
        _itf->log(LOG_ERROR, "Client reception: unable to create a socket");
        plgText(CLIENTRX, "State", "Error, unable to create");
    }

    // set socket for reuse (otherwise might have to wait 4 minutes every time socket is closed)
    int option = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, (const char*)&option, sizeof(option));

    sockaddr_in serverAddress;
    memset(&serverAddress, 0, sizeof(serverAddress));
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = htonl(INADDR_ANY);
    serverAddress.sin_port = htons(_port);

    timeval tv;
    tv.tv_sec  = 0; // Re-used both for accept and recv timeout...
    tv.tv_usec = 100000;
    setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof(tv)); // Timeout on reception. Probably do the same later with SO_SNDTIMEO

    _itf->log(LOG_INFO, "Client reception: Binding socket on port %d", _port);
    int bindSuccess = bind(sockfd, (sockaddr*)&serverAddress, sizeof(serverAddress));
    if(bindSuccess==-1) {
        _itf->log(LOG_ERROR, "Client reception: unable to bind socket");
        plgText(CLIENTRX, "State", "Error, unable to bind");
    }
    int listenSuccess = listen(sockfd, 1); // Only 1 client
    if(listenSuccess==-1) {
        _itf->log(LOG_ERROR, "Client reception: unable to listen to socket");
        plgText(CLIENTRX, "State", "Error, unable to listen");
    }
    plgText(CLIENTRX, "State", "Socket ok");
    plgEnd(CLIENTRX, "Create the listening socket");

    fd_set fds;
    struct sockaddr_in clientAddress;
    socklen_t sosize  = sizeof(clientAddress);

    {
        // Notify the initialization that reception thread is ready
        std::lock_guard<std::mutex> lk(_threadInitMx);
        _rxIsStarted = true;
        _threadInitCv.notify_one();
    }

    // Connection loop
    bool isWaitingDisplayed = false;
    if(bindSuccess!=-1 && listenSuccess!=-1) {
        _itf->log(LOG_INFO, "Client reception: Start the socket listening loop");
    } else {
        char tmpStr[256];
        snprintf(tmpStr, sizeof(tmpStr), "Unable to listen for program connections. Please check that the port %d is not already in use", _port);
        _itf->notifyErrorForDisplay(ERROR_GENERIC, tmpStr);
    }

    plgText(CLIENTRX, "State", "Start the server loop");
    while(!_doStopThreads.load()) {

        // Prevent busy-looping
        std::this_thread::sleep_for(std::chrono::milliseconds(100));

        if(!isWaitingDisplayed) {
            isWaitingDisplayed = true;
            plgText(CLIENTRX, "State", "Waiting for a client");
        }

        // Is there a file injection?
        bsString  injectedFilename;
        bsString* msgInjectedFilename = _msgInjectFile.getReceivedMsg();
        if(msgInjectedFilename) {
            injectedFilename = *msgInjectedFilename;
            _msgInjectFile.releaseMsg();
            // Cancel the request if a live recording is on-going
            if(bsIsSocketValid(_clientSocket)) injectedFilename.clear();
        }

        // If yes, process it
        if(!injectedFilename.empty()) {
            plgScope(CLIENTRX, "Inject file");

            // Open the filename
            _itf->log(LOG_INFO, "Start importing file %s", injectedFilename.toChar());
            FILE* fd = fopen(injectedFilename.toChar(), "rb");
            if(!fd) {
                plgText(CLIENTRX, "State", "Error, Unable to open the injected file");
                _itf->notifyErrorForDisplay(ERROR_IMPORT, bsString("Unable to open the file: ")+injectedFilename);
                continue;
            }

            // Process the file
            dataReceptionLoop(fd);

            // The import is finished, back to the main loop
            continue;
        }

        // Wait for a client program
        FD_ZERO(&fds);
        FD_SET(sockfd, &fds);
        plgBegin(CLIENTRX, "Check socket activity");
        int selectRet = select(sockfd+1, &fds, NULL, NULL, &tv);
        plgEnd(CLIENTRX, "Check socket activity");
        if(selectRet==0) {
            continue;
        }
        if(selectRet==-1 || !FD_ISSET(sockfd, &fds)) {
            _itf->log(LOG_WARNING, "Client reception: failed to set the socket timeout");
            plgText(CLIENTRX, "State", "Error, failed to set the timeout");
        }
        _clientSocket = (bsSocket_t)accept(sockfd, (sockaddr*)&clientAddress, &sosize);

        // If the record processing pipeline is not available, just close the socket
        if(!_itf->isRecordProcessingAvailable()) {
            CLOSE_SOCKET(_clientSocket);
            _clientSocket = bsSocketError;
            continue;
        }

        if(bsIsSocketValid(_clientSocket)) {
            plgScope(CLIENTRX, "New client transport");
            plgData(CLIENTRX, "Socket ID", _clientSocket);
            isWaitingDisplayed = false;
            _itf->log(LOG_DETAIL, "Client reception: New connection detected");

            // Process the file
            dataReceptionLoop(0);
        }
        else {
            _itf->log(LOG_ERROR, "Client reception: Unable to connect to client");
            plgText(CLIENTRX, "State", "Error, failed to connect to client");
        }
    } // End of connection loop
    plgText(CLIENTRX, "State", "End of server loop");

    // Clean the thread
    CLOSE_SOCKET(sockfd);
    plgText(CLIENTRX, "State", "End of data reception thread");
}


bool
cmCnx::initializeTransport(FILE* fd)
{
    plgScope(CLIENTRX, "initializeTransport");
    plAssert((!bsIsSocketValid(_clientSocket) && fd) || (bsIsSocketValid(_clientSocket) && !fd)); // Not both at the same time
    // We wait for the following informations
    //  - 8B: Magic (8 bytes). Check the connection type
    //  - 4B: 0x12345678 sent as a u32, in order to detect the endianness (required for data reception)
    //  - 4B: TLV total size. So first reception shall be 16 bytes, then second reception is the TLV total size
    //  - then TLVs, with the structure: type 2B, length 2B, length padded to 4B alignment (all in big endian)
    //  - Shall include the TLVs "protocol number" (first), "clock info" (origin + event tick to nanosecond) and the "application name" (zero terminated)
    //    Other TLVs are optional

    bsVec<u8> header; header.reserve(256);
    memset(&_tlvs, 0, sizeof(_tlvs));
    _timeTickOrigin = 0;
    _tickToNs       = 1.;
    _appName.clear();
    _buildName.clear();
    _lastDeltaRecordTime = bsGetClockUs();
    resetParser();

    // Read 16 first bytes
    int expectedHeaderSize = 16;
    if(fd) {
        header.resize(expectedHeaderSize);
        int qty = (int)fread(&header[0], 1, expectedHeaderSize, fd);
        header.resize(bsMax(qty, 0));
    } else {
        int remainingTries = 5; // 5 seconds total timeout to get the header
        while(remainingTries>0 && !_doStopThreads.load() && header.size()<expectedHeaderSize) {
            int qty = recv(_clientSocket, (char*)_recBuffer, expectedHeaderSize-header.size(), 0);
            if((errno==EAGAIN || errno==EWOULDBLOCK) && qty<0) {
                --remainingTries;
                continue; // Timeout on reception (empty)
            }
            else if(qty<1) break; // Client is disconnected
            else std::copy(_recBuffer, _recBuffer+qty, std::back_inserter(header));
        }
    }

    // Analyse the first chapter of the header
    if(header.size()!=expectedHeaderSize) {
        _itf->log(LOG_ERROR, "Client did not send the full connection establishment header.");
        plgText(CLIENTRX, "State", "Error, first part of the header not received");
        return false;
    }
    if(strncmp((char*)&header[0], "PL-MAGIC", 8)) {
        _itf->log(LOG_ERROR, "Client sent bad connection identifier (probably not a Palanteer client)");
        plgText(CLIENTRX, "State", "Error, magic not matching");
        return false;
    }
    if(*((u32*)&header[8])!=0x12345678 && *((u32*)&header[8])!=0x78563412) {
        _itf->log(LOG_ERROR, "Client sent unexpected endianness detection string value");
        plgText(CLIENTRX, "State", "Error, endianness detection is not matching");
        return false;
    }
    _recordToggleBytes = (*((u32*)&header[8])==0x78563412);
    int totalTlvLength = (header[12]<<24) | (header[13]<<16) | (header[14]<<8) | header[15];
    if(totalTlvLength>_recBufferSize) {
        _itf->log(LOG_ERROR, "Client sent corrupted header element length");
        plgText(CLIENTRX, "State", "Error, unrealistic header TLV length");
        return false;
    }

#define CHECK_TLV_PAYLOAD_SIZE(expectedSize, name)                      \
    if(tlvLength!=expectedSize) {                                       \
        _itf->log(LOG_ERROR, "Client send a corrupted " name " TLV");   \
        plgText(CLIENTRX, "State",  "ERROR: corrupted " name " TLV");   \
        return false;                                                   \
    }

    // Read the TLVs
    header.clear();
    if(fd) {
        header.resize(totalTlvLength);
        int qty = (int)fread(&header[0], 1, totalTlvLength, fd);
        header.resize(bsMax(qty, 0));
    } else {
        int remainingTries = 3; // 3 second total timeout to get the header
        while(remainingTries>0 && !_doStopThreads.load() && header.size()<totalTlvLength) {
            int qty = recv(_clientSocket, (char*)_recBuffer, totalTlvLength-header.size(), 0);
            if((errno==EAGAIN || errno==EWOULDBLOCK) && qty<0) {
                --remainingTries;
                continue; // Timeout on reception (empty)
            }
            else if(qty<1) break; // Client is disconnected
            else std::copy(_recBuffer, _recBuffer+qty, std::back_inserter(header));
        }
    }

    // Analyse the received TLVs
    if(header.size()!=totalTlvLength) {
        _itf->log(LOG_ERROR, "Client did not send the header element fully");
        plgText(CLIENTRX, "State", "TLVs part of the header not fully received");
        return false;
    }
    int offset = 0;
    while(offset<=totalTlvLength-4) {
        int tlvType   = (header[offset+0]<<8) | header[offset+1];
        int tlvLength = (header[offset+2]<<8) | header[offset+3];
        if(offset+4+tlvLength>totalTlvLength) {
            _itf->log(LOG_ERROR, "Client send a corrupted header element");
            plgText(CLIENTRX, "State", "ERROR: corrupted TLV");
            return false;
        }

        switch(tlvType) {

        case PL_TLV_PROTOCOL:
            CHECK_TLV_PAYLOAD_SIZE(2, "Protocol");
            _tlvs.values[tlvType] = (header[offset+4]<<8) | (header[offset+5]<<0);
            plgData(CLIENTRX, "Protocol is", _tlvs.values[tlvType]);
            break;

        case PL_TLV_CLOCK_INFO: // Clock info TLV: origin and tick to nanosecond coefficient
            CHECK_TLV_PAYLOAD_SIZE(16, "Clock Info");
            _timeTickOrigin = (((u64)header[offset+ 4]<<56) | ((u64)header[offset+ 5]<<48) |
                               ((u64)header[offset+ 6]<<40) | ((u64)header[offset+ 7]<<32) |
                               ((u64)header[offset+ 8]<<24) | ((u64)header[offset+ 9]<<16) |
                               ((u64)header[offset+10]<< 8) |  (u64)header[offset+11]);
            {
                u64 tmp = (((u64)header[offset+12]<<56) | ((u64)header[offset+13]<<48) |
                           ((u64)header[offset+14]<<40) | ((u64)header[offset+15]<<32) |
                           ((u64)header[offset+16]<<24) | ((u64)header[offset+17]<<16) |
                           ((u64)header[offset+18]<< 8) |  (u64)header[offset+19]);
                char* tmp1 = (char*)&tmp; // Avoids a warning on strict aliasing
                _tickToNs  = *(double*)tmp1;
            }
            _tlvs.values[tlvType] = (u64)(1000.*_tickToNs); // Pico second, as precision can be deep
            plgData(CLIENTRX, "Time tick origin is", _timeTickOrigin);
            plgData(CLIENTRX, "Time tick unit is",   _tickToNs);
            break;

        case PL_TLV_APP_NAME:
            // Get the application name
            _appName = bsString((char*)&header[offset+4], (char*)(&header[offset+4]+tlvLength));
            if(!_appName.empty() && _appName.back()==0) _appName.pop_back();
            // Filter out the problematic characters
            {
                int i=0;
                for(u8 c : _appName) {
                    if(c<0x1F || c==0x7F || c=='"' || c=='*' || c=='/' || c=='\\' ||
                       c==':' || c=='<' || c=='>' || c=='^' || c=='?' || c=='|') continue;
                    _appName[i++] = c;
                }
                _appName.resize(i);
                _appName.strip();
            }
            // Some logging
            _itf->log(LOG_DETAIL, "Application name is '%s'", _appName.toChar());
            plgData(CLIENTRX, "Application name", _appName.toChar());
            break;

        case PL_TLV_HAS_BUILD_NAME:
            // Get the build name
            _buildName = bsString((char*)&header[offset+4], (char*)(&header[offset+4]+tlvLength));
            if(!_buildName.empty() && _buildName.back()==0) _buildName.pop_back();
            _itf->log(LOG_DETAIL, "Build name is '%s'", _buildName.toChar());
            plgData(CLIENTRX, "Build name", _buildName.toChar());
            break;

        case PL_TLV_HAS_EXTERNAL_STRING:
            CHECK_TLV_PAYLOAD_SIZE(0, "External String Flag");
            _tlvs.values[tlvType] = 1;
            plgText(CLIENTRX, "State", "External String Flag set");
            break;

        case PL_TLV_HAS_SHORT_STRING_HASH:
            CHECK_TLV_PAYLOAD_SIZE(0, "Short String Hash Flag");
            _tlvs.values[tlvType] = 1;
            plgText(CLIENTRX, "State", "Short String Hash Flag set");
            break;

        case PL_TLV_HAS_NO_CONTROL:
            CHECK_TLV_PAYLOAD_SIZE(0, "No Control Flag");
            _tlvs.values[tlvType] = 1;
            plgText(CLIENTRX, "State", "No Control Flag set");
            break;

        case PL_TLV_HAS_SHORT_DATE:
            CHECK_TLV_PAYLOAD_SIZE(0, "Short Date Flag");
            _tlvs.values[tlvType] = 1;
            plgText(CLIENTRX, "State", "Short Date Flag set");
            break;

        case PL_TLV_HAS_COMPACT_MODEL:
            CHECK_TLV_PAYLOAD_SIZE(0, "Compact Model Flag");
            _tlvs.values[tlvType] = 1;
            plgText(CLIENTRX, "State", "Compact Model Flag set");
            break;

        case PL_TLV_HAS_HASH_SALT:
            CHECK_TLV_PAYLOAD_SIZE(4, "Hash Salt TLV");
            _tlvs.values[tlvType] = (header[offset+4]<<24) | (header[offset+5]<<16) | (header[offset+6]<<8) | (header[offset+7]<<0);
            plgData(CLIENTRX, "Hash salt is", _tlvs.values[tlvType]);
            break;

        default: // Just ignore unknown TLVs. Protocol compatibility is checked later
            plgData(CLIENTRX, "Skipped unknown TLV", tlvType);
        } // End of switch on TLV type

        // Jump to the next TLV
        offset += 4 + tlvLength;

    } // End of loop on initialization payload

    plgText(CLIENTRX, "State", "Transport initialized, header is ok");
    return (!_appName.empty()); // Only mandatory TLV
}


bool
cmCnx::processNewEvents(u8* buf, int eventQty)
{
    // Direct notification
    if(!_tlvs.values[PL_TLV_HAS_COMPACT_MODEL]) {
        return _itf->notifyNewEvents((plPriv::EventExt*)buf, eventQty);
    }

    // Compact model: conversion required
    static_assert(sizeof(plPriv::EventExtCompact)==12, "Bad size of compact exchange event structure");
    static_assert(sizeof(plPriv::EventExt       )==24, "Bad size of exchange event structure");
    _conversionBuffer.resize(eventQty*sizeof(plPriv::EventExt));

    plPriv::EventExtCompact* src = (plPriv::EventExtCompact*)buf;
    plPriv::EventExt*        dst = (plPriv::EventExt*)&_conversionBuffer[0];
    for(int i=0; i<eventQty; ++i, ++src, ++dst) {
        dst->threadId = src->threadId;
        dst->flags    = src->flags;
        dst->lineNbr  = src->lineNbr;
        dst->filenameIdx = src->filenameIdx;
        int eType = src->flags&PL_FLAG_TYPE_MASK;
        if(eType!=PL_FLAG_TYPE_ALLOC_PART && eType!=PL_FLAG_TYPE_DEALLOC_PART) {
            dst->nameIdx  = src->nameIdx;
            if(eType==PL_FLAG_TYPE_CSWITCH) {
                if     (dst->nameIdx==0xFFFF) dst->nameIdx = 0xFFFFFFFF;
                else if(dst->nameIdx==0xFFFE) dst->nameIdx = 0xFFFFFFFE;
            }
        } else {
            dst->memSize = src->memSize;
        }
        dst->vU64 = src->vU32;
    }

    // Notify with the converted buffer
    // Having the processing always with the "large" event structure simplifies a lot the code
    return _itf->notifyNewEvents((plPriv::EventExt*)&_conversionBuffer[0], eventQty);
}


bool
cmCnx::parseTransportLayer(u8* buf, int qty)
{
    // Readability concerns
    bsVec<u8>& s = _parseTempStorage;
    int eventExtSize = _tlvs.values[PL_TLV_HAS_COMPACT_MODEL]? sizeof(plPriv::EventExtCompact) : sizeof(plPriv::EventExtFull);

    // Loop on the buffer content
    while(qty>0) {

        // Header
        if(qty>0 && _parseHeaderDataLeft>0) {
            plAssert(_parseStringLeft==0 && _parseEventLeft==0 && _parseRemoteLeft==0,
                     _parseStringLeft, _parseEventLeft, _parseRemoteLeft);
            // Read
            int usedQty = (_parseHeaderDataLeft<qty)? _parseHeaderDataLeft : qty;
            std::copy(buf, buf+usedQty, std::back_inserter(s));
            buf += usedQty;
            qty -= usedQty;
            _parseHeaderDataLeft -= usedQty;
            // Parse if header is complete
            if(_parseHeaderDataLeft==0) {
                // Magic
                plAssert(s.size()==_parseHeaderSize);
                if(s[0]!='P' || s[1]!='L') {
                    _itf->log(LOG_ERROR, "Received buffer has a corrupted header");
                    return false;
                }
                // Check the type
                plPriv::DataType dataType = (plPriv::DataType) ((s[2]<<8) | s[3]);
                if(dataType==plPriv::PL_DATA_TYPE_STRING) {
                    _parseStringLeft = (s[4]<<24) | (s[5]<<16) | (s[6]<<8) | s[7];
                }
                else if(dataType==plPriv::PL_DATA_TYPE_EVENT) {
                    _parseEventLeft  = (s[4]<<24) | (s[5]<<16) | (s[6]<<8) | s[7];
                    _isCollectionTick = true; // Notification of a collection "tick" for scripting module

                }
                else if(dataType==plPriv::PL_DATA_TYPE_EVENT_AUX) {
                    _parseEventLeft  = (s[4]<<24) | (s[5]<<16) | (s[6]<<8) | s[7];
                }
                else if(dataType==plPriv::PL_DATA_TYPE_CONTROL) {
                    _parseRemoteLeft = (s[4]<<24) | (s[5]<<16) | (s[6]<<8) | s[7];
                }
                else {
                    _itf->log(LOG_WARNING, "Client sent unknown TLV %d - ignored", (int)dataType);
                }
                s.clear();
            }
        } // End of header parsing

        // Strings
        while(qty>0 && _parseStringLeft>0) {
            plAssert(_parseHeaderDataLeft==0);
            int usedQty = 0;
            // Fill the hash
            while(usedQty<qty && s.size()<8) s.push_back(buf[usedQty++]);
            buf += usedQty;
            qty -= usedQty;
            // If the 8 bytes hash is complete
            if(s.size()>=8) {
                // Read the string content (that we add after the hash in the buffer)
                usedQty = 0;
                while(usedQty<qty && buf[usedQty]) ++usedQty;
                if(usedQty<qty) ++usedQty; // Consume the trailing zero
                std::copy(buf, buf+usedQty, std::back_inserter(s));
                buf += usedQty;
                qty -= usedQty;
                plAssert(!s.empty());
                if(s.back()==0) {
                    _parseStringLeft -= 1;
                    u64 h = (((u64)s[0])<<56) | (((u64)s[1])<<48) | (((u64)s[2])<<40) | (((u64)s[3])<<32) |
                        (((u64)s[4])<<24) | (((u64)s[5])<<16) | (((u64)s[6])<<8) | (((u64)s[7])<<0);
                    _itf->notifyNewString(bsString((char*)s.begin()+8, (char*)s.end()), h); // Store the string and the hash (first 8 bytes)
                    s.clear();
                }
            }
        } // End of string parsing

        // Events
        while(qty>0 && _parseEventLeft>0) {
            plAssert(_parseHeaderDataLeft==0);
            if(!s.empty()) {
                int usedQty = (qty>eventExtSize-s.size())? eventExtSize-s.size() : qty;
                std::copy(buf, buf+usedQty, std::back_inserter(s));
                buf += usedQty;
                qty -= usedQty;
                if(s.size()==eventExtSize) {
                    _parseEventLeft -= 1;
                    if(!processNewEvents(&s[0], 1)) return false; // Event corruption
                    s.clear();
                }
            }
            int eventQty = qty/eventExtSize;
            if(eventQty>_parseEventLeft) eventQty = _parseEventLeft;
            if(eventQty) {
                if(!processNewEvents(buf, eventQty)) return false; // Event corruption
                buf += eventQty*eventExtSize;
                qty -= eventQty*eventExtSize;
                _parseEventLeft -= eventQty;
            }
            if(qty>0 && _parseEventLeft>0) {
                plAssert(qty<eventExtSize);
                std::copy(buf, buf+qty, std::back_inserter(s));
                buf += qty;
                qty -= qty;
            }
        } // End of event parsing

        if(_isCollectionTick && _parseEventLeft==0) {
            // Notify a collection tick, once the buffer is fully parsed
            _isCollectionTick = false;
            _itf->notifyNewCollectionTick();
        }

        // Remote control
        while(qty>0 && _parseRemoteLeft>0) {
            plAssert(_parseHeaderDataLeft==0);
            int usedQty = (qty>_parseRemoteLeft)? _parseRemoteLeft : qty;
            std::copy(buf, buf+usedQty, std::back_inserter(s));
            buf += usedQty;
            qty -= usedQty;
            _parseRemoteLeft -= usedQty;
            if(_parseRemoteLeft==0) {
                _itf->notifyNewRemoteBuffer(s);
                s.clear();
            }
        } // End of remote control parsing

        if(_parseHeaderDataLeft==0 && _parseStringLeft==0 && _parseEventLeft==0 && _parseRemoteLeft==0) {
            plAssert(s.empty());
            resetParser();
        }
    } // End of loop on buffer content

    return true;
}
