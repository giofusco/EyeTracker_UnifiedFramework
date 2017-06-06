/*
# Copyright 2017 The Smith-Kettlewell Eye Research Institute
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Giovanni Fusco - giofusco@ski.org
*/

#include <cstdio>
#include <thread>
#include <iostream>
#include <fstream>
#include <ctime>
#include <chrono>
#include <iomanip>
#ifdef _WIN32
#include "LpmsSensorI.h"
#include "LpmsSensorManagerI.h"
#endif
#ifdef __GNUC__
#include "lpsensor/LpmsSensorI.h"
#include "lpsensor/LpmsSensorManagerI.h"
#endif

class IMULogger{

    public:
        IMULogger(std::string ttyDev, std::string logfile){
            manager = LpmsSensorManagerFactory();
            lpms = manager->addSensor(DEVICE_LPMS_U2, ttyDev.c_str());
            lpms->setConfigurationPrm(PRM_SAMPLING_RATE, 400);
            lpms->setVerbose(false);
            logfilename = logfile;
            openLogFile();
            
        }
        
        ~IMULogger(){
            manager->removeSensor(lpms);
            delete manager;
        }

        void setNewLogFile(std::string logfile){
                if (log)
                    std::cerr << "!!! Stop logging before changing file \n";
                else {
                    logFile.close();
                    logfilename = logfile;
                    openLogFile();
                }
        }

        std::thread start(){
            log = true;
            return std::thread(&IMULogger::logData, this);
            
        }
        void pause() {log=false;}
        void restart() {log=true;}

    private:
        LpmsSensorManagerI* manager;
        LpmsSensorI* lpms;
        ImuData d;
        std::string logfilename;
        std::ofstream logFile;
        bool log;

        void openLogFile(){
            logFile.open (logfilename);
            if (!logFile.is_open())
                std::cerr << "!!! Error opening LogFile\n";
        }
        
        void logData(){
            //write header
            logFile << "ClockTimeStamp \t IMUTimeStamp \t EulerX \t EulerY \t EulerZ \n";
            while(log) {		 
                // Checks, if sensor is connected
                if (this->lpms->getConnectionStatus() == SENSOR_CONNECTION_CONNECTED &&
                    this->lpms->hasImuData()) {
                        auto now = std::chrono::system_clock::now();
                        auto now_micros = std::chrono::time_point_cast<std::chrono::microseconds>(now);
                        auto epoch = now_micros.time_since_epoch();
                        auto value = std::chrono::duration_cast<std::chrono::microseconds>(epoch);
                        d = lpms->getCurrentData();
                        logFile << value.count() << "\t" << std::fixed << std::setprecision(5) << d.timeStamp << "\t" << d.r[0] << " \t " << d.r[1] << " \t " << d.r[2] << "\n";
                }
            }
        }
};
