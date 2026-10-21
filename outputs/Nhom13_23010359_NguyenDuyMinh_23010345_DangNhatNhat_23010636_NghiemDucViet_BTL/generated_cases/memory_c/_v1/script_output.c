/* Generated correction: worst-case output size, initialised index, bounded input, checked allocation. */
#include <stdlib.h>
#include <string.h>

#define INPUT_MAX 4096

char *escape_html_v1(const char *s)
{
    size_t n = strnlen(s, INPUT_MAX);
    if (n == INPUT_MAX)
        return NULL;
    char *out = malloc(n * 5 + 1);                /* "&amp;" is the longest replacement */
    if (out == NULL)
        return NULL;
    size_t j = 0;
    for (size_t i = 0; i < n; i++) {
        const char *rep = s[i] == '<' ? "&lt;" : s[i] == '>' ? "&gt;" : s[i] == '&' ? "&amp;" : NULL;
        if (rep != NULL) {
            size_t k = strlen(rep);
            memcpy(out + j, rep, k);
            j += k;
        } else {
            out[j++] = s[i];
        }
    }
    out[j] = '\0';
    return out;
}

char *demo_escape_v1(void)
{
    return escape_html_v1("<script>alert(1)</script>");
}
