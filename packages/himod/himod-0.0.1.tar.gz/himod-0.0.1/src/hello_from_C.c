#include <Python.h>


static PyObject* hello(PyObject *self, PyObject *args){
	puts("Hello_From_C!");
	Py_RETURN_NONE;
 }

static char alpha_docs[] =
    "usage: hello(noargs)\n";

/* deprecated: 
static PyMethodDef uniqueCombinations_funcs[] = {
    {"uniqueCombinations", (PyCFunction)uniqueCombinations, 
     METH_NOARGS, uniqueCombinations_docs},
    {NULL}
};
use instead of the above: */

static PyMethodDef module_methods[] = {
    {"hello", (PyCFunction) hello, 
     METH_NOARGS, alpha_docs},
    {NULL}
};


/* deprecated : 
PyMODINIT_FUNC init_uniqueCombinations(void)
{
    Py_InitModule3("uniqueCombinations", uniqueCombinations_funcs,
                   "Extension module uniqueCombinations v. 0.01");
}
*/

static struct PyModuleDef himod =
{
    PyModuleDef_HEAD_INIT,
    "hello_module_2", /* name of module */
    "usage: himod.hello(noargs)\n", /* module documentation, may be NULL */
    -1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods
};

PyMODINIT_FUNC PyInit_himod(void)
{
    return PyModule_Create(&himod);
}