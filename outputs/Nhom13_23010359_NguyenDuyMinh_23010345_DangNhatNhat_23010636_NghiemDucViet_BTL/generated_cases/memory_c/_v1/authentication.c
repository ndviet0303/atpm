/* Generated correction: bounded copies, checked allocation, one exit that wipes and frees. */
#include <stdlib.h>
#include <string.h>

struct user { char name[32]; char hash[65]; };

static void wipe(void *p, size_t n)
{
    volatile unsigned char *v = p; /* volatile stops the compiler from removing the stores */
    while (n--)
        *v++ = 0;
}

int authenticate_v1(const char *username, const char *password, const struct user *db, size_t n)
{
    char name[32];
    size_t ulen = strnlen(username, sizeof name);
    size_t plen = strnlen(password, 128);
    if (ulen == sizeof name || plen == 128)
        return 0;
    char *secret = malloc(plen + 1);
    if (secret == NULL)
        return 0;
    memcpy(secret, password, plen + 1);
    memcpy(name, username, ulen + 1);
    int ok = 0;
    for (size_t i = 0; i < n && !ok; i++)
        ok = strcmp(db[i].name, name) == 0 && strcmp(db[i].hash, secret) == 0;
    wipe(secret, plen + 1);
    free(secret);
    return ok;
}

int demo_login_v1(const struct user *db, size_t n)
{
    return authenticate_v1("librarian-account-with-a-very-long-name-0001", "admin", db, n);
}
