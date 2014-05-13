# /app/models/document.py
import csv
import mimetypes
from ferris import BasicModel
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import urlfetch
from google.appengine.api import files
from google.appengine.ext import deferred

class Document(BasicModel):
    string1 = ndb.StringProperty(required=True)
    text1 = ndb.TextProperty()
    image1 = ndb.BlobKeyProperty()

    @classmethod
    def import_rows(self, csv_file):
        blob_reader = blobstore.BlobReader(csv_file.key())
        blob_interator = BlobIterator(blob_reader) # This will remove any newline chars
        reader = csv.DictReader(blob_interator, dialect='excel', delimiter=',')
        print reader
        for row in reader:
            document = Document(string1 = row["string1"],
                                text1 = row["text1"],
                                image1 = Document.download_file(row["image1"]))
            document.put()
            
            blobstore.delete(csv_file.key()) # make sure to not leaving behind an orphan csv file
    
    @classmethod
    def import_document(self, csv_file):
        
        ndb.delete_multi(Document.query().fetch(keys_only=True)) # Uncomment to delete existing records first
        deferred.defer(self.import_rows, csv_file)

    @staticmethod
    def download_file(url):
        file_name = url.split('/')[-1]
        response = urlfetch.fetch(url)  # response.status_code == 200 
        print response.status_code, ' - ', file_name, ' - ', url
        if response.status_code == 200:
            (mimetype, _) = mimetypes.guess_type(file_name) 
            file_name = files.blobstore.create(mime_type= mimetype, _blobinfo_uploaded_filename= file_name)
            with files.open(file_name, 'a') as f:                                           
                f.write(response.content)
            files.finalize(file_name)                       
            blob_key = files.blobstore.get_blob_key(file_name)
            return blob_key
        else:
            return None

class BlobIterator:
    """Because the python csv module doesn't like strange newline chars and
    the google blob reader cannot be told to open in universal mode, then
    we need to read blocks of the blob and 'fix' the newlines as we go"""

    def __init__(self, blob_reader):
        self.blob_reader = blob_reader
        self.last_line = ""
        self.line_num = 0
        self.lines = []
        self.buffer = None
    
    def __iter__(self):
        return self
    
    def next(self):
        if not self.buffer or len(self.lines) == self.line_num:
            self.buffer = self.blob_reader.read(1048576) # 1MB buffer
            self.lines = self.buffer.splitlines()
            self.line_num = 0
            
            # Handle special case where our block just happens to end on a new line
            if self.buffer[-1:] == "\n" or self.buffer[-1:] == "\r":
                self.lines.append("")
    
        if not self.buffer:
            raise StopIteration
        
        if self.line_num == 0 and len(self.last_line) > 0:
            result = self.last_line + self.lines[self.line_num] + "\n"
        else:
            result = self.lines[self.line_num] + "\n"
    
        self.last_line = self.lines[self.line_num]
        self.line_num += 1
    
        return result