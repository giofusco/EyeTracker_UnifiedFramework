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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <thread>         // std::thread
#include "./include/IMULogger.hpp"



void error(const char *msg)
{
    perror(msg);
    exit(1);
}


//arguments: socket port, /dev/ttyUSBX, logfilename
int main(int argc, char *argv[])
{
     int sockfd, newsockfd, portno;
     socklen_t clilen;
     char buffer[256];
     std::thread logThread;
     IMULogger logger(argv[2], argv[3]);
     struct sockaddr_in serv_addr, cli_addr;
     int n;
     if (argc < 2) {
         fprintf(stderr,"ERROR, no port provided\n");
         exit(1);
     }
     sockfd = socket(AF_INET, SOCK_STREAM, 0);
     if (sockfd < 0) 
        error("ERROR opening socket");
     bzero((char *) &serv_addr, sizeof(serv_addr));
     portno = atoi(argv[1]);
     serv_addr.sin_family = AF_INET;
     serv_addr.sin_addr.s_addr = INADDR_ANY;
     serv_addr.sin_port = htons(portno);
     if (bind(sockfd, (struct sockaddr *) &serv_addr,
              sizeof(serv_addr)) < 0) 
              error("ERROR on binding");
     listen(sockfd,5);
     clilen = sizeof(cli_addr);
     newsockfd = accept(sockfd, 
                 (struct sockaddr *) &cli_addr, 
                 &clilen);
     if (newsockfd < 0) 
          error("ERROR on accept");
     bzero(buffer,256);
     
     while(1){
        n = read(newsockfd,buffer,255);
        if (n < 0) {error("ERROR reading from socket"); break;}
        else if (n>0){
            if (strcmp(buffer, "START") == 0){
                logThread = logger.start();
                n = write(newsockfd,"ACK_START",9);
                if (n < 0) {error("ERROR writing to socket"); break;}
            }
            else if (strcmp(buffer, "STOP") == 0){
                logger.pause();
                n = write(newsockfd,"ACK_STOP",8);
                if (n < 0) {error("ERROR writing to socket"); break;}
            }
            else if (strcmp(buffer, "SETFILE") == 0){
                logger.pause();
                logThread.join();
                n = write(newsockfd,"ACK_SETFILE",11);
                if (n < 0) {error("ERROR writing to socket"); break;}
                // wait for filename
                bzero(buffer,256);
                n = read(newsockfd,buffer,255);
                logger.setNewLogFile(std::string(buffer));
                //logThread = logger.start();
                bzero(buffer,256);
                n = write(newsockfd,"ACK_SETFILE_DONE",16);
                if (n < 0) {error("ERROR writing to socket"); break;}
            }
            else if (strcmp(buffer, "RESTART") == 0){
                logThread = logger.start();
                n = write(newsockfd,"ACK_RESTART",8);
                if (n < 0) {error("ERROR writing to socket"); break;}
                break;
            }
            else if (strcmp(buffer, "QUIT") == 0){
                logger.pause();
                n = write(newsockfd,"ACK_QUIT",8);
                if (n < 0) {error("ERROR writing to socket"); break;}
                break;
            }
            bzero(buffer,256);
        }
        
     }
     close(newsockfd);
     close(sockfd);
     logThread.join(); // wait for the thread to rejoin 
	
     return 0; 
}
