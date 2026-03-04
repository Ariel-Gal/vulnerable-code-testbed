#include <stdio.h>
#include <string.h>

void process_input(char *user_input) {
    char buffer[64];
    strcpy(buffer, user_input);
    printf("Processed: %s\n", buffer);
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        process_input(argv[1]);
    }
    return 0;
}