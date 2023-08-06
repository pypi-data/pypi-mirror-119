============
Installation
============

You can install Crappy on the three main OS : Windows, Mac and Linux. Note that
Crappy is developed and tested on the latest OS versions, and no particular
effort is made to ensure compatibility with previous ones. It is thus preferable
to install it on a recent and up-to-date OS version.

Requirements
------------

To install Crappy, you will need Python 3 (3.6 or higher) with the following
modules :

  - Numpy (1.19.0 or higher)

The following modules are not mandatory but will provide additional
functionalities :

  - matplotlib (1.5.3 or higher, for plotting graphs and displaying images)
  - Opencv (3.0 or higher, to perform image acquisition and analysis)
  - pyserial (To interface with serial sensors and actuators)
  - Tk (For the configuration interface of cameras)
  - Scikit-image (0.11 or higher)
  - xiApi (for Ximea cameras)
  - labjack (for Labjack support)
  - Simple-ITK (for faster image saving)
  - PyCUDA (for real-time correlation)
  - Comedi driver (for Comedi acquisition boards, Linux only)
  - PyDaqmx (for National Instrument boards, Windows only)
  - niFgen (package from National Instrument, Windows only)
  - openDAQ (for opendaq boards)

.. note::
  Knowing which modules are needed for a given setup is easy. Just write the
  script and start it, if a module is missing Crappy will simply tell you !

A. For Linux users
------------------
These steps have been tested for Ubuntu 18.04 and 20.04 but should work on other
distributions as well as long as Python 3.6 is installed.

**1.** The first step is to get the required dependencies.

**1.a.** Install the dependencies in a ``virtualenv`` (recommended) :
::

  workon myenv
  pip3 install <module>

If you're not familiar with virtual environments,
`here <https://virtualenv.pypa.io/en/latest/>`_'s more documentation.

**1.b.** Or install the required Python modules on the system :
::

  sudo apt update
  sudo apt upgrade
  sudo apt install python3-pip
  pip3 install <module>


**2.** You can now install crappy. Again, two ways to go.

**2.a.** For **regular users**, install using ``pip`` :
::

  pip3 install crappy


**2.b.** For **developers**, get the sources using ``git`` and use ``setup``
script :
::

  cd <path>
  git clone https://github.com/LaboratoireMecaniqueLille/crappy.git
  cd crappy
  sudo python3 setup.py install

If you're not familiar with ``git``, documentation can be found
`here <https://git-scm.com/doc>`_.

.. note::
  - Replace ``<module>`` by the name of the module you want to install.
  - Replace ``<path>`` by the path where you want Crappy to be located.

B. For Windows users
--------------------
These steps have been tested for Windows 8.1 and 10 but should work with other
versions as well. If you want to load C++ modules, make sure to use the x64
version of Python.

1. Install the dependencies:
::

  pip3 install <module>

This will works for most modules, but some may fail and need a wheel file
built for Windows. We had to do this for numpy (with mkl) and scikit-image.
Just find the correct version at http://www.lfd.uci.edu/~gohlke/pythonlibs/
and simply run :
::

  pip3 install wheel_file.whl

2. Also, you will need Visual C++ for Python 3.x (your version of python) in
   order to compile C++ modules.  If you want to use Ximea cameras, don't
   forget to install XiAPI and add ``c:\XIMEA\API\x64`` to your path.

3. Then you can get the source code and install it:
::

  git clone https://github.com/LaboratoireMecaniqueLille/crappy.git
  cd crappy
  setup.py install

C. For macOS users
------------------
These steps have been tested on macOS Catalina (10.15.7), but should work with
other versions as well.

1. You should install the required modules using pip.
::

  python install pip
  pip install module-name

D. Troubleshooting
------------------

The imaging module is not natively included in Tk. Some user may have to
install it manually to us the camera configuration GUI

For Ubuntu, you can do
::

  sudo apt install python3-pil.imagetk

Also, the matplotlib backend may have some troubles initializing multiple
windows on some desktop environment. It can be fixed easily by using an other
backend. Simply specify a functional backed in the grapher to fix this issue
i.e.:
::

  graph = crappy.bocks.Grapher(('t(s)', 'F(N)'), backend='TkAgg')

Or simply edit the default backend in crappy/blocks/grapher.py by replacing
None with the desired backend.
