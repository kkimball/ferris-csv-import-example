Ferris Framework CSV Import Example
===================================

This is an example csv import app for the Ferris Framework.  The intent is to show a method for importing csv data to the GAE Datastore from within the Ferris Framework.

Features
========

 -- Import text from a csv file
 -- Download and import files to the Blobstore from urls in your csv file
 -- Use google.appengine.ext.deferred to tranfer processing to the task queue and avoid timeouts

Usage
=====

This is a fully working example.  To text it out set up a Ferris 2.1 installation and copy app/* into your project.

To test:

 -- Navigate to http://<IP:PORT>/documents/import_csv
 -- Browse to the included csv_testfile.csv and click submit
 -- View the imported data
 
Special Thanks
==============

This example uses code from http://d4nt.com/parsing-large-csv-blobs-on-google-app-engine/ to solve an issue with parsing csv files with newline characters
