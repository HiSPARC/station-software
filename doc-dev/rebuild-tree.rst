Rebuilding the Development Tree
===============================

This is a complete log of building the development environment from
scratch.  Lots of third-party packages need to be installed and included
in the installer tree.

.. note:: In general, you don't need to follow these instructions to just
          start building a package.  This is only needed when you need to
          recreate the whole tree.  It is more useful as a reference when
          one wants to update a package or two with newer versions.


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

:Homepage: http://www.ni.com/
:Version: 8.2.1 (Standard download)
:Download: http://joule.ni.com/nidu/cds/view/p/id/550/lang/en
:Direct Link: http://lumen.ni.com/nicif/US/GB_NIDU/content.xhtml?du=http://joule.ni.com/nidu/cds/view/p/id/550/lang/en_US

Installation steps:

#. Complete the registration procedure or log in
#. Download and run the executable (which is a *WinZip Self-Extractor*)
#. **WinZip Self-Extractor:** Uncheck *When done unzipping open
   ``.\\setup.exe``* and click *Unzip*
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


MySQL ODBC Driver
-----------------

:Homepage: http://www.mysql.com/
:Version: 5.1.8 (x86, 32-bit, ZIP Archive, noinstall)
:Download: http://dev.mysql.com/downloads/connector/odbc/
:Direct Link: http://dev.mysql.com/get/Downloads/Connector-ODBC/5.1/mysql-connector-odbc-noinstall-5.1.8-win32.zip/from/http://ftp.gwdg.de/pub/misc/mysql/

Installation steps:

#. Unzip to ``\admin`` and rename the
   ``mysql-connector-odbc-noinstall-5.1.8-win32`` folder to
   ``odbcconnector``


OpenVPN
-------

:Homepage: http://openvpn.net/
:Version: 2.1.4
:Download: http://openvpn.net/index.php/open-source/downloads.html
:Direct Link: http://swupdate.openvpn.net/community/releases/openvpn-2.1.4-install.exe

Installation steps:

#. Download and run the installer
#. Copy the ``C:\Program Files\OpenVPN`` folder to ``\admin`` and rename
   to ``openvpn``


TightVNC
--------

:Homepage: http://www.tightvnc.com/
:Version: 1.3.10 (Complete set, no installer)
:Download: http://www.tightvnc.com/download-old.php
:Direct Link: http://www.tightvnc.com/download/1.3.10/tightvnc-1.3.10_x86.zip

Installation steps:

#. Create a ``\admin\tightvnc`` folder and unzip the download to this
   folder

.. note:: There is a new major version which would solve a lot of
          VNC-related problems.  It would be very nice to include that in
          an update.  That will be our very first admin update, however...


Windows Driver Kit (WDK)
------------------------
:Homepage: http://msdn.microsoft.com/en-us/windows/hardware/gg487428
:Version: 7.1.0
:Download: http://www.microsoft.com/downloads/en/details.aspx?displaylang=en&FamilyID=36a2630f-5d56-43b5-b996-7633f2ec14ff
:Direct Link: http://www.microsoft.com/downloads/info.aspx?na=41&SrcFamilyId=36A2630F-5D56-43B5-B996-7633F2EC14FF&SrcDisplayLang=en&u=http%3a%2f%2fdownload.microsoft.com%2fdownload%2f4%2fA%2f2%2f4A25C7D5-EFBE-4182-B6A9-AE6850409A78%2fGRMWDK_EN_7600_1.ISO

Installation steps:

#. Microsoft recommends that you download the ISO, burn it, and then
   insert it in your drive.  Alternatively, attach it to a virtual
   machine, or something similar.
#. Install the *Tools* package.

This is needed for installing the FTDI drivers.


FTDI Drivers (Communication with Electronics Box USB Chip)
----------------------------------------------------------

:Homepage: http://www.ftdichip.com/
:Version: 2.08.08 (CDM, x86 32-bit)
:Download: http://www.ftdichip.com/Drivers/VCP.htm
:Direct Link: http://www.ftdichip.com/Drivers/CDM/CDM20808.zip

Installation steps:

#. Unpack the zip file.
#. Move the ``CDM20814_WHQL_Certified`` folder to ``\admin``.
#. Rename the folder to ``ftdi_drivers``.
#. Copy
   ``C:\WinDDK\7600.16385.1\redist\DIFx\dpinst\EngMui\x86\dpinst.exe`` to
   ``\admin\ftdi_drivers``.
#. Copy ``\admin\ftdi_drivers\i386\ftd2xx.dll`` to ``\user\hisparcdaq``.


GPS Monitor (DSPMON)
--------------------

:Homepage: http://www.trimble.com/timing/resolution-t.aspx
:Version: 1.46
:Download: http://www.trimble.com/timing/resolution-t.aspx?dtID=support
:Direct Link: http://trl.trimble.com/dscgi/ds.py/Get/File-366495/DSPMon_V1-46.exe

Installation steps:

#. Create folder ``\user\dspmon``.
#. Copy ``DSPMon_V1-46.exe`` to ``\user\dspmon``.
#. Rename file to ``DSPMon.exe``.


Nagios: Send Passive Check Results (NSCA Client)
------------------------------------------------

:Homepage: http://exchange.nagios.org/directory/Addons/Passive-Checks/NSCA-Win32-Client/details
:Version: Unknown
:Download: http://exchange.nagios.org/components/com_mtree/attachment.php?link_id=550&cf_id=29

Installation steps:

#. Unpack zip file.
#. Copy ``send_nsca_win32_bin`` folder to ``\user\hsmonitor\data``.
#. Rename folder to ``send_nsca_win32``.
#. Edit ``\user\hsmonitor\data\send_nsca_win32\send_nsca.cfg``: change
   ``encryption_method=1`` to ``encryption_method=0``.

.. note:: I'd really like to change this to something better.  Still, it is
          not as bad as it seems since everything is sent over the VPN.


Nagios: Client (NSClient++)
----------------------------

:Homepage: http://nsclient.org/nscp/
:Version: 0.3.8
:Download: http://nsclient.org/nscp/downloads
:Direct Link: http://files.nsclient.org/x-0.3.x/NSClient%2B%2B-0.3.8-Win32.zip

Installation steps:

#. Unpack zip file.
#. Enter ``NSClient++-0.3.8-Win32`` folder.
#. Copy everything, *except* ``scripts`` *folder and* ``nsci.ini`` *file*, to
   ``\admin\nsclientpp``.


Nullsoft Scriptable Install System (NSIS)
-----------------------------------------

:Homepage: http://nsis.sourceforge.net/
:Version: 2.46
:Download: http://nsis.sourceforge.net/Download
:Direct Link: http://prdownloads.sourceforge.net/nsis/nsis-2.46-setup.exe?download

Installation steps:

#. Run .exe file.
#. Perform a *Full* installation.
#. Copy ``C:\Program Files\NSIS`` to ``\bake``.
#. Rename ``NSIS`` folder to ``nsis``.


NSIS Unzip plugin (Nsisunz)
---------------------------

:Homepage: http://nsis.sourceforge.net/Nsisunz_plug-in
:Version: June 22, 2007
:Direct Link: http://saivert.com/nsis/nsisunz.7z

Installation steps:

#. Open archive.
#. Copy ``Release/nsisunz.dll`` to ``\bake\nsis\Plugins``.


NSIS XtInfoPlugin
-----------------

:Homepage: http://nsis.sourceforge.net/XtInfoPlugin_plug-in
:Version: 1.0.0.2
:Direct Link: http://nsis.sourceforge.net/mediawiki/images/1/1d/XtInfoPlugin_v_1.0.0.2.zip

Installation steps:

#. Open archive.
#. Copy ``xtInfoPlugin\xtInfoPlugin.dll`` to ``\bake\nsis\Plugins``.


NSIS Simple Service Plugin (SimpleSC)
-------------------------------------

:Homepage: http://nsis.sourceforge.net/NSIS_Simple_Service_Plugin
:Version: 1.29
:Direct Link: http://nsis.sourceforge.net/mediawiki/images/e/ed/NSIS_Simple_Service_Plugin_1.29.zip

Installation steps:

#. Open archive.
#. Copy ``SimpleSC.dll`` to ``\bake\nsis\Plugins``.


NSIS Simple Firewall Plugin (SimpleFC)
--------------------------------------

:Homepage: http://nsis.sourceforge.net/NSIS_Simple_Firewall_Plugin
:Version: 1.18
:Direct Link: http://nsis.sourceforge.net/mediawiki/images/6/67/NSIS_Simple_Firewall_Plugin_1.18.zip

Installation steps:

#. Open archive.
#. Copy ``SimpleFC.dll`` to ``\bake\nsis\Plugins``.


NSIS Access Control Plugin
--------------------------

:Homepage: http://nsis.sourceforge.net/AccessControl_plug-in
:Version: January 23, 2008
:Direct Link: http://nsis.sourceforge.net/mediawiki/images/4/4a/AccessControl.zip

Installation steps:

#. Open archive.
#. Copy ``AccessControl\Plugins\*.dll`` to ``\bake\nsis\Plugins``.


Python
------

:Homepage: http://python.org/
:Version: 2.7.1
:Download: http://www.python.org/download/
:Direct Link: http://www.python.org/ftp/python/2.7.1/python-2.7.1.msi

Installation steps:

#. Install *Just for me* (this makes it easier to redistribute the
   package).


Python for Windows Extensions (pywin32)
---------------------------------------

:Homepage: http://sourceforge.net/projects/pywin32/
:Version: Build 216
:Download: http://sourceforge.net/projects/pywin32/files/pywin32/
:Direct Link: http://sourceforge.net/projects/pywin32/files/pywin32/Build216/pywin32-216.win32-py2.7.exe/download

Installation steps:

#. Default installation.


Windows Management Instrumentation for Python (Python-WMI)
----------------------------------------------------------

:Homepage: http://timgolden.me.uk/python/wmi/index.html
:Version: 1.4.6
:Download: http://timgolden.me.uk/python/wmi/index.html#where-do-i-get-it
:Direct Link: http://timgolden.me.uk/python/downloads/WMI-1.4.6.win32.exe

Installation steps:

#. Default installation.


MySQL for Python (MySQLdb)
--------------------------

:Homepage: http://www.lfd.uci.edu/~gohlke/pythonlibs/
:Version: 1.2.3
:Download: http://www.lfd.uci.edu/~gohlke/pythonlibs/

.. note:: Since I don't own Microsoft Visual Studio, I can't compile the
          MySQL extension module myself.  If you *do* own MSVC, you might
          be able to compile and run the official package from
          http://pypi.python.org/pypi/MySQL-python/.

Installation steps:

#. Default installation.


Finishing Python Installation
-----------------------------

Steps:

#. Copy ``C:\Python27`` to ``\user``.
#. Rename ``Python27`` folder to ``python``.

Unfortunately, the world of Windows is complex.  The world of Windows
compilers is even more complex.  You can't use binaries (executables or
DLLs) from different compilers or even compiler versions together.  For
instance, you can't import a Python module containing compiled code when
it is compiled with a different compiler than Python itself.  Since
Windows installations commonly don't *have* a compiler, this can be a pain
and breaks installers.  What's more: compile code with Microsoft Visual
C++ and install it on a machine *without* Microsoft Visual C++ and it may
not work out of the box.  For instance, try this::

    >>> import _tkinter
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ImportError: DLL load failed: This application has failed to start
    because the application configuration is incorrect. Reinstalling the
    application may fix this problem.
    >>> import win32api
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ImportError: DLL load failed: The specified module could not be found.

This not only happens with Tkinter and PyWin32, but also with several
other packages that are used by the HiSPARC software.  Just trying to
import _tkinter is an easy check to see if things are ok.  For Python
2.7.1, the error can be resolved by installing the Microsoft Visual C++
2008 Redistributable package.  Don't try another version, it won't work.
Alternatively, you can fix the python installation by copying a few files
around.  This is much easier to do.

Steps (continued):

#. Copy ``msvcr90.dll`` and ``Microsoft.VC90.CRT.manifest`` to
   ``\user\python\DDLs``.
#. Copy contents of ``\user\python\Lib\site-packages\pywin32_system32`` to
   ``\user\python``.

Now try::

    >>> import _tkinter
    >>> import win32api
