/* Generated correction: checked allocation, read-only authorisation, one owner releases the session. */
#include <stdlib.h>
#include <string.h>

struct session { char *role; int user_id; };

struct session *load_session_v1(int user_id)
{
    struct session *s = malloc(sizeof *s);
    if (s == NULL)
        return NULL;
    s->user_id = user_id;
    s->role = strdup(user_id == 1 ? "admin" : "member");
    if (s->role == NULL) {
        free(s);
        return NULL;
    }
    return s;
}

void end_session_v1(struct session *s)
{
    if (s == NULL)
        return;
    free(s->role);
    s->role = NULL;
    free(s);
}

int authorize_v1(const struct session *s, const char *action)
{
    if (s == NULL || s->role == NULL || action == NULL)
        return 0;
    return strcmp(s->role, "admin") == 0;
}

int demo_logout_v1(void)
{
    struct session *s = load_session_v1(2);
    int allowed = authorize_v1(s, "logout");
    end_session_v1(s);
    return allowed;
}
