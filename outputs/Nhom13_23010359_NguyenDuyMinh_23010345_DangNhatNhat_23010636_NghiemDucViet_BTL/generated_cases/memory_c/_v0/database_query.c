/* Intentionally unsafe generated experiment for the memory study. Analysed statically, never linked or run. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *build_query_v0(const char *id)
{
    char *sql = malloc(64);
    sprintf(sql, "DELETE FROM book WHERE book_id='%s'", id); /* 34 fixed bytes + any id length into 64 */
    return sql;
}

char **fetch_titles_v0(size_t rows)
{
    char **titles = malloc(4 * sizeof *titles);
    for (size_t i = 0; i < rows; i++) {           /* rows has no upper bound, like SELECT without LIMIT */
        if (i >= 4 && i % 4 == 0)
            titles = realloc(titles, (i + 4) * sizeof *titles); /* old block lost if realloc fails */
        titles[i] = strdup("title");
    }
    return titles;
}

void free_titles_v0(char **titles, size_t rows)
{
    for (size_t i = 0; i < rows; i++)
        free(titles[i]);
    free(titles);
    free(titles);
}

char *demo_query_v0(void)
{
    return build_query_v0("1' OR '1'='1' -- padding padding padding padding");
}
