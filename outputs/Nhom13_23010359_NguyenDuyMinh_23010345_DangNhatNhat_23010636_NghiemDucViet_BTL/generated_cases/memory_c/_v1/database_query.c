/* Generated correction: fixed placeholder query, bounded page of rows, checked allocations, single free. */
#include <stdlib.h>
#include <string.h>

#define PAGE_ROWS 50

void free_titles_v1(char **titles, size_t rows)
{
    if (titles == NULL)
        return;
    for (size_t i = 0; i < rows; i++)
        free(titles[i]);
    free(titles);
}

char *build_query_v1(void)
{
    static const char sql[] = "DELETE FROM book WHERE book_id = ?";
    char *copy = malloc(sizeof sql);
    if (copy != NULL)
        memcpy(copy, sql, sizeof sql);
    return copy;
}

char **fetch_titles_v1(size_t rows)
{
    if (rows > PAGE_ROWS)
        rows = PAGE_ROWS;
    char **titles = calloc(rows + 1, sizeof *titles);
    if (titles == NULL)
        return NULL;
    for (size_t i = 0; i < rows; i++) {
        titles[i] = strdup("title");
        if (titles[i] == NULL) {
            free_titles_v1(titles, i);
            return NULL;
        }
    }
    return titles;
}

char *demo_query_v1(void)
{
    return build_query_v1();
}
