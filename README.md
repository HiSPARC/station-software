HiSPARC Station Software
========================

All software running on the HiSPARC stations is located in this
repository.  Notable exclusions: the data acquisition programs written in
LabVIEW have their own repositories.  The software responsible for
uploading event data and monitoring the station's health, as well as
connecting to the VPN network is all here.

The installer for the HiSPARC station software is built from this
repository.

The installer documentation can be found in the `doc/` subdirectory.
The documentation to set up your own development environment, as well as
the documentation that describes how the initial environment was created,
can be found in the `doc-dev/` subdirectory.

The documentation can be read online at http://docs.hisparc.nl/station-software/.


Deployment
----------

Here are the steps to create an installer executable for the HiSPARC
installer.

First it is necessary to modify some develop files. We renamed some
files to provide templates for the actual files, which have been added
to `.gitignore`, so no sensitive information is accidentally committed.

1. Copy the file `/db_buffer/buffer-develop.sql` to
   `/db_buffer/buffer.sql`. Then replace the PLACEHOLDERs with the actual
   passwords in the new file.

2. You can create the following file to override the buffer password in the
   Monitor config: `/user/hsmonitor/data/config-password.ini`. This file
   should contain the following data:

    [BufferDB]
    Password=PLACEHOLDER

3. Copy the file `/bake/nsisscripts/password-placeholder.nsh` to
   `/bake/nsisscripts/password.nsh`. Then replace the PLACEHOLDERs with the
   actual passwords in the new file.

When the password configuration is complete, run the bake script:

    bake/bake.bat

Which then runs the script `bake.py`, this then calls NSIS to compile
the installers. You will be asked to enter a version and release number
for this release.
