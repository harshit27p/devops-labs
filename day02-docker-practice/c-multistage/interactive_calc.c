#include <stdio.h>

int main() {
    char student_name[50];
    int num1, num2;

    printf("Enter Student Name: ");
    if (scanf("%49s", student_name) != 1) return 1;

    printf("Enter First Integer: ");
    if (scanf("%d", &num1) != 1) return 1;

    printf("Enter Second Integer: ");
    if (scanf("%d", &num2) != 1) return 1;

    printf("\n--- Result ---\n");
    printf("DevOps Engineer: %s\n", student_name);
    printf("Calculation: %d + %d = %d\n", num1, num2, num1 + num2);

    return 0;
}
