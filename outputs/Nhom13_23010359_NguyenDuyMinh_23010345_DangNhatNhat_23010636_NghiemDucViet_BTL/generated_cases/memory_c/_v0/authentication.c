/* Intentionally unsafe generated experiment for the memory study. Analysed statically, never linked or run. */
#include <stdlib.h>
#include <string.h>

struct user { char name[32]; char hash[65]; };

int authenticate_v0(const char *username, const char *password, const struct user *db, size_t n)
{
    char name[32];
    char *secret = malloc(strlen(password) + 1); /* not checked for NULL */
    strcpy(secret, password);
    strcpy(name, username);                       /* no length check on a 32-byte stack buffer */
    for (size_t i = 0; i < n; i++) {
        if (strcmp(db[i].name, name) == 0)
            return strcmp(db[i].hash, secret) == 0; /* early return keeps secret allocated */
    }
    free(secret);                                 /* plaintext password freed without wiping */
    return 0;
}

int demo_login_v0(const struct user *db, size_t n)
{
    return authenticate_v0("librarian-account-with-a-very-long-name-0001", "admin", db, n);
}
