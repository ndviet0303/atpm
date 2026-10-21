/* Intentionally unsafe generated experiment for the memory study. Analysed statically, never linked or run. */
#include <stdlib.h>
#include <string.h>

char *escape_html_v0(const char *s)
{
    size_t n = strlen(s);
    char *out = malloc(n + 1);                    /* "<" grows to 4 bytes, buffer sized for 1 */
    size_t j;                                     /* never initialised */
    for (size_t i = 0; i < n; i++) {
        if (s[i] == '<') {
            memcpy(out + j, "&lt;", 4);
            j += 4;
        } else {
            out[j++] = s[i];
        }
    }
    out[j] = '\0';
    return out;
}

char *demo_escape_v0(void)
{
    return escape_html_v0("<script>alert(1)</script>");
}
