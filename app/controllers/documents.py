# /app/controllers/documents.py
from ferris import Controller, scaffold, route
from ferris.components.upload import Upload
from app.models.document import Document

class Documents(Controller):
    class Meta:
        prefixes = ('admin',)
        components = (scaffold.Scaffolding, Upload)
    
    admin_list = scaffold.list
    admin_view = scaffold.view
    admin_add = scaffold.add 
    admin_edit = scaffold.edit
    admin_delete = scaffold.delete
    
    list = scaffold.list
    view = scaffold.view
    
    @route
    def import_csv(self):
        self.context['upload_url'] = self.components.upload.generate_upload_url(action='process_csv')         

    @route
    def process_csv(self): 
        uploads = self.components.upload.get_uploads()
        csv_file =  uploads['file'][0] # only one file should be uploaded
        if csv_file.content_type in ['text/csv', 'application/vnd.ms-excel']:
            Document.import_document(csv_file)
            return_value = "File Uploaded Successfully.  Check your Task Queue inthe Google App Engine Control Panel"
        else:
            print csv_file.content_type
            return_value = 'The file provided is not of type ''text/csv'' or ''application/vnd.ms-excel'''
        return return_value