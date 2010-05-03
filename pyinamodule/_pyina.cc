// Patrick Hung & Mike McKerns
// California Inst. of Tech.

#include <mpi.h>
#include <typeinfo>
#include <Python.h>
#include "mpi/Communicator.h"
#include "mpi/Group.h"
#include <iostream>

using namespace mpi;

#include "journal/debug.h"

#define JINFO info << journal::at(__HERE__)

// Templated destructor
template <typename T>
static void destrT(void *ptr) {
    journal::debug_t info("pyina.fini");
    JINFO << "destructor called for type: " << typeid(T).name() 
          << journal::endl;
    T * v = static_cast<T *>(ptr);
    delete v;
    return;
}

static PyObject *_pyinaError;

PyDoc_STRVAR(
    module_doc,
    "_pyina -- C++ extension module for pathos mpi communicators\n"
    );

PyDoc_STRVAR(hello_doc, "For sanity checks.");
static PyObject *
_pyina_hello(PyObject *self, PyObject *args)
{
    return PyString_FromString("pyina says Hello.");
}

PyDoc_STRVAR(test_doc, "Trying to receive an MPI Communicator object defined by the pythia mpi module");
static PyObject *
_pyina_test(PyObject *self, PyObject *args)
{
    journal::debug_t info("pyina.test");

    PyObject * py_comm;

    int ok = PyArg_ParseTuple(args, "O:test", &py_comm);
    if (!ok) {
        return 0;
    }

    if (!PyCObject_Check(py_comm)) {
        PyErr_SetString(PyExc_TypeError, "Expecting a CObject as argument 0");
        return 0;
    } 

    // get the communicator
    Communicator * comm = (Communicator *) PyCObject_AsVoidPtr(py_comm);

    // on null communicator
    if (!comm) {
        JINFO << "Null Communicator received" << journal::endl;
        Py_RETURN_NONE;
    }

    // test
    MPI_Comm h = comm->handle();

    // testing
    Group * newGroup = Group::group(*comm);

    void (*fp)(void *) = destrT< Group >;
    return PyCObject_FromVoidPtr(newGroup, fp);
}

PyDoc_STRVAR(commDup_doc, 
             "Bindings for MPI_Comm_dup. \n"
             "debuginfo is journal.debug(\"pyina.commDup\")\n");
             
static PyObject *
_pyina_commDup(PyObject *self, PyObject *args)
{
    journal::debug_t info("pyina.commDup");

    PyObject * py_comm;

    int ok = PyArg_ParseTuple(args, "O:commDup", &py_comm);
    if (!ok) {
        return 0;
    }

    if (!PyCObject_Check(py_comm)) {
        PyErr_SetString(PyExc_TypeError, "Expecting a CObject as argument 0");
        return 0;
    } 

    // get the communicator
    Communicator * comm = (Communicator *) PyCObject_AsVoidPtr(py_comm);

    // on null communicator
    if (!comm) {
        JINFO << "Null Communicator received" << journal::endl;
        Py_RETURN_NONE;
    }

    // test
    MPI_Comm h = comm->handle();

    MPI_Comm dupcomm;
    MPI_Comm_dup(h, &dupcomm);

    Communicator * newcomm = new Communicator(dupcomm);

    void (*fp)(void *) = destrT< Communicator >;
    return PyCObject_FromVoidPtr(newcomm, fp);
}


PyDoc_STRVAR(sendString_doc, 
             "Exactly the same as sendString from pyre's mpi module \n"
             "debuginfo is journal.debug(\"pyina.sendString\")\n");
static PyObject *
_pyina_sendString(PyObject *self, PyObject *args)
{
    int tag;
    int len;
    int peer;
    char * str;
    PyObject * py_comm;

    int ok = PyArg_ParseTuple(args, "Oiis#:sendString", &py_comm, &peer, &tag, &str, &len);

    if (!ok) {
        return 0;
    }

    // get the communicator
    Communicator * comm = (Communicator *) PyCObject_AsVoidPtr(py_comm);

    // on null communicator
    if (!comm) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    // dump arguments
    journal::debug_t info("pyina.sendString");
    JINFO << "peer={" << peer
          << "}, tag={" << tag
          << "}, string={" << str << "}@" << len
          << journal::endl;

    // send the length of the string
    int status = MPI_Send(&len, 1, MPI_INT, peer, tag, comm->handle());

    // send the data (along with the terminating null)
    status = MPI_Send(str, len+1, MPI_CHAR, peer, tag, comm->handle());

    // return
    Py_INCREF(Py_None);
    return Py_None;
}



PyDoc_STRVAR(receiveString_doc, 
             "new receive String\n"
             "debuginfo is journal.debug(\"pyina.receiveString\")\n");
static PyObject *
_pyina_receiveString(PyObject *self, PyObject *args)
{
    journal::debug_t info("pyina.receiveString");

    int tag;
    int peer;
    PyObject * py_comm;

    int ok = PyArg_ParseTuple(args, "Oii:receiveString", &py_comm, &peer, &tag);
    if (!ok) {
        return 0;
    }

    JINFO << "receive for peer # : " << peer << journal::endl; 

    // get the communicator
    Communicator * comm = (Communicator *) PyCObject_AsVoidPtr(py_comm);

    // on null communicator
    if (!comm) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    // receive the length
    int len;
    MPI_Status status;
    MPI_Recv(&len, 1, MPI_INT, peer, tag, comm->handle(), &status);

    int sender0 = status.MPI_SOURCE;

    // receive the data, not from "peer," but from the actual sender
    // these two send/receives are always paired
    char * str = new char[len+1];
    MPI_Recv(str, len+1, MPI_CHAR, sender0, tag, comm->handle(), &status);

    int sender = status.MPI_SOURCE;
    int anstype = status.MPI_TAG;
    //if (len < 50) {
    //    std::cout << "\nstr[" << len << "]: {" << str << "}" << std::endl;
    //    std::cout << "senders: " << sender0 << " : " << sender << std::endl;
    //}

    PyObject *t;
    t = PyDict_New();
    PyDict_SetItemString(t, "MPI_SOURCE", PyInt_FromLong(sender));
    PyDict_SetItemString(t, "MPI_TAG", PyInt_FromLong(anstype));
    PyDict_SetItemString(t, "MPI_ERROR", PyInt_FromLong(status.MPI_ERROR)); 

    // dump message
    JINFO << "peer={" << peer
          << "}, tag={" << tag
          << "}, sender={" << sender
          << "}, ans tag={" << anstype
          << "}, string={" << str << "}@" << len
          << journal::endl;
    
    // build the return value
    PyObject *ret;
    ret = PyTuple_New(2);
    PyTuple_SetItem(ret, 0, Py_BuildValue("s", str));
    PyTuple_SetItem(ret, 1, t);

    // clean up
    delete [] str;

    return ret;
}


PyDoc_STRVAR(bcastString_doc, 
             "new bcast String\n"
             "debuginfo is journal.debug(\"pyina.bcastString\")\n");
static PyObject *
_pyina_bcastString(PyObject *self, PyObject *args)
{
    journal::debug_t info("pyina.bcastString");

    int root;
    int len;
    char *str;
    PyObject * py_comm;
    
    int ok = PyArg_ParseTuple(args, "Ois#:bcastString", &py_comm, &root, &str, &len);

    if (!ok) {
        return 0;
    }
    
    JINFO << "bcast for root # : " << root 
          << " string = {" << str << "}@" << len 
          << journal::endl; 
    
    // get the communicator
    Communicator * comm = (Communicator *) PyCObject_AsVoidPtr(py_comm);
    
    // on null communicator
    if (!comm) {
        Py_RETURN_NONE;
    }

    int myid;
    MPI_Comm_rank(comm->handle(), &myid);
    
    // bcast the length of the string
    int status = MPI_Bcast( &len, 1, MPI_INT, root, comm->handle());

   
    JINFO << "myid={" << myid
          << "} got len: " << len
          << journal::endl;

    // bcast (with terminating NULL)
    PyObject * ret;
    if (myid == root) {
        status = MPI_Bcast( str, len+1, MPI_CHAR, root, comm->handle());
        ret = Py_BuildValue("s", str);
    } 
    else {
        char * buf = new char[len+1];
        status = MPI_Bcast( buf, len+1, MPI_CHAR, root, comm->handle());
        ret = Py_BuildValue("s", buf);
        delete [] buf;
    }
   
    return ret;
}

PyDoc_STRVAR(mpiconsts_doc, 
             "exports some MPI constants as a dictionary\n" );
static PyObject *
_pyina_mpiconsts(PyObject *self, PyObject *args)
{
    PyObject *t;
    t = PyDict_New();
    PyDict_SetItemString(t, "MPI_ANY_TAG", PyInt_FromLong(MPI_ANY_TAG));
    PyDict_SetItemString(t, "MPI_ANY_SOURCE", PyInt_FromLong(MPI_ANY_SOURCE));
    PyDict_SetItemString(t, "MPI_ROOT", PyInt_FromLong(MPI_ROOT)); 
    PyDict_SetItemString(t, "MPI_TAG_UB", PyInt_FromLong(MPI_TAG_UB)); 
    PyDict_SetItemString(t, "MPI_HOST", PyInt_FromLong(MPI_HOST)); 
    PyDict_SetItemString(t, "MPI_IO", PyInt_FromLong(MPI_IO)); 
    PyDict_SetItemString(t, "MPI_WTIME_IS_GLOBAL", PyInt_FromLong(MPI_WTIME_IS_GLOBAL)); 
    return t;

}



// List of functions defined in this module
struct PyMethodDef _pyina_methods[] = {

    // the core routines
    { "hello",   _pyina_hello,   1, hello_doc },
    { "test",   _pyina_test,   1, test_doc },
    { "commDup",   _pyina_commDup,   1, commDup_doc },
    { "sendString",   _pyina_sendString,   1, sendString_doc },
    { "receiveString",   _pyina_receiveString,   1, receiveString_doc },
    { "bcastString",   _pyina_bcastString,   1, bcastString_doc },
    { "mpiconsts",   _pyina_mpiconsts,   1, mpiconsts_doc },
    {  NULL, NULL } // sentinel

};


PyMODINIT_FUNC init_pyina(void)
{
    PyObject * m;

    // Create the module and add the functions
    m = Py_InitModule3( "_pyina", _pyina_methods, module_doc);

    _pyinaError = PyErr_NewException("_pyina.error", NULL, NULL);
    Py_INCREF(_pyinaError);
    PyModule_AddObject(m, "error", _pyinaError);


    // check for errors
    if (PyErr_Occurred()) {
        Py_FatalError("can't initialize module _pyina");
    }

    return;
}

#undef JINFO 

// end of file
