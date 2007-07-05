#include <Python.h>
#define MARKER "\x1f"

/*
 longest_match() and longest_match_shifter()

 Returns the length of the longest common substring (LCS) in the strings
 a and b.

 Sets a_offset to the index of a where the LCS begins.
 Sets b_offset to the index of b where the LCS begins.

 If there is NO common substring, it returns 0 and sets both
 a_offset and b_offset to -1.

 The strings do not have to be equal length.

 The algorithm works by comparing one character at a time and "shifting" the
 strings so that different characters are compared. For example, given
 a="ABC" and b="DEF", picture these alignments:

                     (Shift a to the right)
    -------------------------------------------------------
    a             |  ABC            ABC             ABC
    b             |  DEF           DEF            DEF
    shift index   |  0             1              2
    possible LCS  |  3             2              1
    comparisons   |  AD, BE, CF    AE, BF         AF

                     (Shift b to the right)
    -------------------------------------------------------
                  |  ABC           ABC            ABC
                  |  DEF            DEF             DEF
    shift index   |  0             1              2
    possible LCS  |  3             2              1
    comparisons   |  AD, BE, CF    BD, CE         CD

 The algorithm short circuits based on the best_size found so far. For example,
 given a="ABC" and b="ABC", the first cycle of comparisons (AA, BB, CC) would
 result in a best_size=3. Because the algorithm starts with zero shift (i.e.,
 it starts with the highest possible LCS) and adds 1 to the shift index each
 time through, it can safely exit without doing any more comparisons.

 This algorithm is O^(m+n), where m and n are the length of the two strings.
 Due to short circuiting, the algorithm could potentially finish after the very
 first comparison. Thus, for strings of length 11 and 12, it could take
 anywhere from 1 to 23 comparisons to calculate the longest match. The
 algorithm is slowest when the LCS is smallest, and the algorithm is fastest
 when the LCS is biggest.

 longest_match_shifter() performs "one side" of the shift -- e.g., "Shift a to
 the right" in the above illustration. longest_match() simply calls
 longest_match_shifter() twice, flipping the strings.
*/

int longest_match_shifter(char* a, char* b, int a_start, int a_end, int b_start, int b_end, int best_size, int* a_offset, int* b_offset) {
    int i, j, k;
    unsigned int current_size;

    for (i = b_start, current_size = 0; i < b_end; i++, current_size = 0) { // i is b starting index.
        if (best_size >= b_end - i) break; // Short-circuit. See comment above.
        for (j = i, k = a_start; k < a_end && j < b_end; j++, k++) { // k is index of a, j is index of b.
            if (a[k] == b[j]) {
                if (++current_size > best_size) {
                    best_size = current_size;
                    *a_offset = k - current_size + 1;
                    *b_offset = j - current_size + 1;
                }
            }
            else {
                current_size = 0;
            }
        }
    }
    return best_size;
}

// a_offset and b_offset are relative to the *whole* string, not the substring
// (as defined by a_start and a_end).
// a_end and b_end are (the last index + 1).
int longest_match(char* a, char* b, int a_start, int a_end, int b_start, int b_end, int* a_offset, int* b_offset) {
    unsigned int best_size;
    *a_offset = -1;
    *b_offset = -1;
    best_size = longest_match_shifter(a, b, a_start, a_end, b_start, b_end, 0, a_offset, b_offset);
    best_size = longest_match_shifter(b, a, b_start, b_end, a_start, a_end, best_size, b_offset, a_offset);
    return best_size;
}

/*
 make_template()

 Creates a template from two strings with a given tolerance.
*/

void make_template(char* template, int tolerance, char* a, char* b, int a_start, int a_end, int b_start, int b_end) {
    int a_offset, b_offset;
    unsigned int best_size;

    best_size = longest_match(a, b, a_start, a_end, b_start, b_end, &a_offset, &b_offset);
    if (best_size == 0) {
        strcat(template, MARKER);
    }
    if (a_offset > a_start && b_offset > b_start) {
        // There's leftover stuff on the left side of BOTH strings.
        make_template(template, tolerance, a, b, a_start, a_offset, b_start, b_offset);
    }
    else if (a_offset > a_start || b_offset > b_start) {
        // There's leftover stuff on the left side of ONLY ONE of the strings.
        strcat(template, MARKER);
    }

    if (best_size > tolerance) {
        strncpy(template+strlen(template), a+a_offset, best_size);

        if ((a_offset + best_size < a_end) && (b_offset + best_size < b_end)) {
            // There's leftover stuff on the right side of BOTH strings.
            make_template(template, tolerance, a, b, a_offset + best_size, a_end, b_offset + best_size, b_end);
        }
        else if ((a_offset + best_size < a_end) || (b_offset + best_size < b_end)) {
            // There's leftover stuff on the right side of ONLY ONE of the strings.
            strcat(template, MARKER);
        }
    }
}

/* 
 PYTHON STUFF

 These are the hooks between Python and C.

 function_longest_match() is commented out, because it's not necessary to
 expose it at the Python level. To expose it, uncomment it, along with the
 appropriate line in the "ModuleMethods[]" section toward the bottom of this
 file.
*/

/*
static PyObject * function_longest_match(PyObject *self, PyObject *args) {
    int a_offset, b_offset;
    char* a;
    char* b;
    unsigned int best_size;

    if (!PyArg_ParseTuple(args, "ss", &a, &b))
        return NULL;
    best_size = longest_match(a, b, 0, strlen(a), 0, strlen(b), &a_offset, &b_offset);
    return Py_BuildValue("(iii)", best_size, a_offset, b_offset);
}
*/

static PyObject * function_make_template(PyObject *self, PyObject *args) {
    char* template;
    char* a;
    char* b;
    int tolerance;
    static PyObject* result;

    if (!PyArg_ParseTuple(args, "ssi", &a, &b, &tolerance))
        return NULL;
    template = (char *) malloc(524288 * sizeof(char)); // TODO: This is hard-coded.
    strcpy(template, "");
    make_template(template, tolerance, a, b, 0, strlen(a), 0, strlen(b));

    result = Py_BuildValue("s", template);
    free(template);
    return result;
}

static PyObject * function_marker(PyObject *self, PyObject *args) {
    return Py_BuildValue("s", MARKER);
}

static PyMethodDef ModuleMethods[] = {
    // longest_match is commented out because it's not necessary to expose it
    // at the Python level. To expose it, uncomment the following line.
/*    {"longest_match", function_longest_match, METH_VARARGS, "Given two strings, determines the longest common substring and returns a tuple of (best_size, a_offset, b_offset)."},*/
    {"make_template", function_make_template, METH_VARARGS, "Given two strings, returns a template."},
    {"marker", function_marker, METH_VARARGS, "Returns a string of the template marker."},
    {NULL, NULL, 0, NULL}        // sentinel
};

PyMODINIT_FUNC init_templatemaker(void) {
    (void) Py_InitModule("_templatemaker", ModuleMethods);
}
