========================
Folder Structure Creator
========================
:Info: This is the README file for Folder Structure Creator.
:Author: David Sanchez <dvswells@gmail.com>
:Copyright: © 2021, David Sanchez
:Date: 07-09-2021
:Version: 0.1.4

.. index: README

PURPOSE
-------

A simple folder structure creator capable of interpreting a tab-delimited text file and creating the defined folder hierarchy.

INSTALLATION
------------

::

    pip install folder-structure

CLI USAGE
---------

**Run:** ``python folder_structure.cli``.

Designing the folder structure hierarchy in a text file called 'test_structure'

::

   1. Test
      1.1 Test
      1.2 Test
   2. Test
      2.1 Test
         2.1.2 Test
   3. Test
      3.1 Test

Creating the folder structure from the text file

::

    $ python folder_structure test_structure
   The folder structure will be created at C:\folder-structure\folder_structure
   Line 0
   Line 1
   Line 2
   Line 3
   Line 4
   Line 5
   Line 6
   Line 7
   Line 8
   The folder structure creation has ended successfully.

Result

.. image:: https://github.com/dvswells/folder-structure/blob/main/test_structure.PNG

COPYRIGHT
---------
Copyright © 2021, David Sanchez.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions, and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions, and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the author of this software nor the names of
   contributors to this software may be used to endorse or promote
   products derived from this software without specific prior written
   consent.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.