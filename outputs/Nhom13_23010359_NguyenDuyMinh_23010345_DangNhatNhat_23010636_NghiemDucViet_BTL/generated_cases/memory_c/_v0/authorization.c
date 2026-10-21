/* Intentionally unsafe generated experiment for the memory study. Analysed statically, never linked or run. */
#include <stdlib.h>
#include <string.h>

struct session { char *role; int user_id; };

struct session *load_session_v0(int user_id)
{
    struct session *s = malloc(sizeof *s);
    s->user_id = user_id;                         /* malloc result not checked */
    s->role = strdup(user_id == 1 ? "admin" : "member");
    return s;
}

int authorize_v0(struct session *s, const char *action)
{
    char *role = s->role;
    if (strcmp(action, "logout") == 0)
        free(s->role);
    return strcmp(role, "admin") == 0;            /* role read after free on logout */
}

int demo_logout_v0(void)
{
    struct session *s = load_session_v0(2);
    return authorize_v0(s, "logout");             /* session never released */
}
