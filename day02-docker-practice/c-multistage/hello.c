#include <stdio.h>
#include <unistd.h>

int main() {
    printf("=========================================\n");
    printf(" CDAC PGCP-ITISS DevOps C-Microservice\n");
    printf(" Executed via Optimized Multi-Stage Build\n");
    printf("=========================================\n");

    char hostname[1024];
    gethostname(hostname, 1024);

    printf("Running on Container Hostname: %s\n", hostname);

    return 0;
}
