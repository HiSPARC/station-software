Setting up a Development Machine
================================

* python
* pywin32, wmi, setuptools
* openvpn
* tightvnc
* hisparcdaq
* ftdi drivers
* odbc
* dspmon
* nagios NSCA + nsclient++ (push)
* NSIS

Bazaar (a Distributed Version Control System (DVCS))
----------------------------------------------------

:Homepage: http://bazaar.canonical.com/
:Version: 2.2.1-3 (Standalone)
:Download: http://wiki.bazaar.canonical.com/WindowsDownloads
:Direct Link: http://launchpad.net/bzr/2.2/2.2.1/+download/bzr-2.2.1-3-setup.exe

Installation steps:

#. Download and run the installer
#. **Select Components:** *A typical installation* with *Windows Shell
   Extensions (TortoiseBZR) enabled*


HiSPARC Software Checkout
-------------------------

:Direct Link: sftp://<user>@login.nikhef.nl/project/hisparc/bzr/windows-development/trunk/

Steps:

#. **What would you like to do?:** *Get project source from elsewhere*
   -> *Checkout*
#. *Branch source:* sftp://<user>@login.nikhef.nl/project/hisparc/bzr/windows-development/trunk/
#. *Local directory where the working tree will be created:* Use a
   directory of your choice.  Suggestion: ``My Documents/HiSPARC/trunk``
#. Click *OK*.  You will be asked for your ``login.nikhef.nl`` account
   password several times.
#. Copy ``\persistent\configuration\startup_settings_example.bat`` to
   ``\persistent\configuration\startup_settings.bat`` and edit to your
   personal taste
#. You can now run ``\hisparc_cmd.bat`` if you want to start a command
   terminal with a HiSPARC detector pc environment


Notepad++ (a Source Code Editor)
--------------------------------

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

:Homepage: http://www.ni.com/
:Version: 8.2.1 (Standard download)
:Download: http://joule.ni.com/nidu/cds/view/p/id/550/lang/en
:Direct Link: http://lumen.ni.com/nicif/US/GB_NIDU/content.xhtml?du=http://joule.ni.com/nidu/cds/view/p/id/550/lang/en_US

Installation steps:

#. Complete the registration procedure or log in
#. Download and run the executable (which is a *WinZip Self-Extractor*)
#. **WinZip Self-Extractor:** Uncheck *When done unzipping open
   ``.\setup.exe``* and click *Unzip*
#. When finished unzipping, click *Close*
#. Copy ``c:\National Instruments Downloads\LabVIEW 8.2.1\Runtime
   Engine`` to ``\admin``
#. Rename the ``\admin\Runtime Engine`` folder to
   ``\admin\niruntimeinstaller``
#. Copy ``\admin\niruntimeinstaller\Bin\silent_install.txt`` to
   ``\admin\niruntimeinstaller`` and rename to ``hisparcspec.ini``
#. Edit ``hisparcspec.ini`` and enter user information (serial number)


MySQL Community Server (a Database Server)
------------------------------------------

:Homepage: http://www.mysql.com/
:Version: 5.1.53 (x86, 32-bit, ZIP Archive, noinstall)
:Download: http://www.mysql.com/downloads/mysql/
:Direct Link: http://www.mysql.com/get/Downloads/MySQL-5.1/mysql-noinstall-5.1.53-win32.zip/from/http://mirror.leaseweb.com/mysql/

Installation steps:

#. Unzip to ``\user`` and rename the ``mysql-5.1.53-win32`` folder to
   ``mysql``
#. Copy ``\user\mysql\my-medium.ini`` to ``\user\mysql\my.ini``
#. Edit the ``my.ini`` file:
    #. **Section [mysqld]:** add ``basedir="/user/mysql/"``
    #. **Section [mysqld]:** add ``datadir=/persistent/data/mysql/"``
#. Create the ``\persistent\data`` folder
#. Move the ``\user\mysql\data`` folder to ``\persistent\data`` and
   rename to ``mysql`` (you now have a ``\persistent\data\mysql``
   folder)
#. Run ``\hisparc_cmd.bat``, navigate to ``\user\mysql\bin`` and run
   ``mysqld --console`` and keep this window open (this is the *MySQL
   Server Console*)
#. Run ``\hisparc_cmd.bat``, navigate to ``\user\mysql\bin`` and run
   ``mysql -u root`` and do:
    #. ``DROP USER '';``
    #. ``DROP USER ''@localhost;``
    #. ``SET PASSWORD FOR root@localhost = PASSWORD('<rootpassword>');``
    #. ``SET PASSWORD FOR root@127.0.0.1 = PASSWORD('<rootpassword>');``
    #. ``DROP DATABASE test;``
    #. ``QUIT;``
#. Run ``\hisparc_cmd.bat``, navigate to ``\user\mysql\bin`` and run
   ``mysql -u root -p < \buffer.sql`` and give the root password when
   prompted
#. In the *MySQL Server Console* window, press ``Control-C`` to
   correctly shutdown the server
#. In the ``\persistent\data\mysql`` folder delete the ``mysql-bin.*``
   files and any ``*.pid`` and ``*.err`` files if they exist from
   previous runs of the server
