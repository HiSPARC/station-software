Setting up a Development Environment
====================================

This document explains how to set up a development environment on a fresh
Windows installation.  For reference, :doc:`rebuild-tree` discusses
rebuilding the entire development tree from scratch.  Mind that you don't
need to do this, and if you do, you'll overwrite lots of third-party
binaries which have been committed to the repository.

Just follow these instructions and you can start building your own HiSPARC
software installation packages.


git (a Distributed Version Control System (DVCS))
----------------------------------------------------

:Homepage: http://git-scm.com/
:Version: 1.7.10.4 (Standalone)
:Download: http://git-scm.com/downloads
:Direct Link (win): http://git-scm.com/download/win
:Direct Link (mac): http://git-scm.com/download/mac

Installation steps:

#. Download and run the installer


HiSPARC Software Checkout
-------------------------

:Direct Link: https://github.com/HiSPARC/station-software.git
:Command Line: git clone git@github.com:HiSPARC/station-software.git
:GitHub For Windows link: github-windows://openRepo/https://github.com/HiSPARC/station-software
:GitHub For Mac link: github-mac://openRepo/https://github.com/HiSPARC/station-software

Steps:

#. Run Command Prompt (Start -> Run -> ``cmd``)
#. ``git clone git@github.com:HiSPARC/station-software.git <checkout-location>``.
   Example::

    C:\Documents and Settings\David Fokkema>cd "My Documents"
    C:\Documents and Settings\David Fokkema\My Documents>mkdir HiSPARC
    C:\Documents and Settings\David Fokkema\My Documents>git clone git@github.com:HiSPARC/station-software.git HiSPARC\trunk

#. Edit ``\persistent\configuration\startup_settings.bat`` to your
   personal taste
#. You can now run ``\hisparc_cmd.bat`` if you want to start a command
   terminal with a HiSPARC detector pc environment


Notepad++ (a Source Code Editor) (Optional)
-------------------------------------------

:Homepage: http://notepad-plus-plus.org/
:Version: 6.1.3 (Installer)
:Download: http://notepad-plus-plus.org/download/
:Direct Link: http://download.tuxfamily.org/notepadplus/6.1.3/npp.6.1.3.Installer.exe

Installation steps:

#. Download and run the installer
#. All defaults are ok
#. Navigate to a Python source file and double-click on it.
#. **Windows cannot open this file:** *Select the program from a list*
#. **Choose the program you want to use to open the file:** Select Notepad++ and click *Open*.  If Notepad++ is not in the list, click *Browse*
    #. Navigate to ``Notepad++/notepad++`` and click *Open*
    #. Select Notepad++ and click *Open*


LabVIEW Run-Time Engine
-----------------------

Although the run-time engine has already been installed, the license
requires a serial number which is *not* committed in the repository.

Installation steps:

#. Copy ``\admin\niruntimeinstaller\Bin\silent_install.txt`` to
   ``\admin\niruntimeinstaller`` and rename to ``hisparcspec.ini``
#. Edit ``hisparcspec.ini`` and enter user information (serial number)
