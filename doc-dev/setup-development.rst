Setting up a Development Environment
====================================

This document explains how to set up a development environment on a fresh
Windows installation.  For reference, :doc:`rebuild-tree` discusses
rebuilding the entire development tree from scratch.  Mind that you don't
need to do this, and if you do, you'll overwrite lots of third-party
binaries which have been committed to the repository.

Just follow these instructions and you can start building your own HiSPARC
software installation packages.


Bazaar (a Distributed Version Control System (DVCS))
----------------------------------------------------

:Homepage: http://bazaar.canonical.com/
:Version: 2.3.1 (Standalone)
:Download: http://wiki.bazaar.canonical.com/WindowsDownloads
:Direct Link: http://launchpad.net/bzr/2.3/2.3.1/+download/bzr-2.3.1-1-setup.exe

Installation steps:

#. Download and run the installer
#. **Select Components:** *A typical installation* with *Windows Shell
   Extensions (TortoiseBZR) enabled*


HiSPARC Software Checkout
-------------------------

:Direct Link: sftp://<user>@login.nikhef.nl/project/hisparc/bzr/windows-development/trunk/

Steps:

#. Run Command Prompt (Start -> Run -> ``cmd``)
#. ``bzr checkout sftp://<user>@login.nikhef.nl/project/hisparc/bzr/windows-development/trunk/ <checkout-location>``.
   Example::

    C:\Documents and Settings\David Fokkema>cd "My Documents"
    C:\Documents and Settings\David Fokkema\My Documents>mkdir HiSPARC
    C:\Documents and Settings\David Fokkema\My Documents>bzr checkout sftp://davidf@login.nikhef.nl/project/hisparc/bzr/windows-development/trunk/ HiSPARC\trunk

#. Edit ``\persistent\configuration\startup_settings.bat`` to your
   personal taste
#. You can now run ``\hisparc_cmd.bat`` if you want to start a command
   terminal with a HiSPARC detector pc environment


Notepad++ (a Source Code Editor) (Optional)
-------------------------------------------

:Homepage: http://notepad-plus-plus.org/
:Version: 5.8.5 (Installer)
:Download: http://notepad-plus-plus.org/downloads
:Direct Link: http://download.tuxfamily.org/notepadplus/5.8.5/npp.5.8.5.Installer.exe

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
