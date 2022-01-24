from django.shortcuts import render          # for rendering templates
from pandas import read_excel                # for data processing
from pathlib import Path                     # for path handling
from django.contrib import messages          # for error messages

def upload_page_view(request):
    # when user upload file (post request)
    if request.method == 'POST':

        # handle empty file upload
        if(len(request.FILES) == 0):
            messages.error(request, "Please choose a file to upload!")       # create error message
            return render(request, 'parser_app/upload.html')                 # render upload page with error message

        # user actually uploaded a file
        uploaded_file = request.FILES['doc']                                 # get the uploaded file

        # handle incorrect files uploads
        if(Path(uploaded_file.name).suffix != '.xlsx'):
            messages.error(request, Path(uploaded_file.name).suffix +" is incorrect file format!")               # create error message
            return render(request, 'parser_app/upload.html')                # render upload page with error message

        # correct file uploaded, convert it to csv
        data_frame = read_excel(uploaded_file,engine='openpyxl')                              # convert the file into pandas data frame
        output_file_path = 'media/' + Path(uploaded_file.name).stem + '.csv'# get the name of the output file
        data_frame.to_csv(output_file_path, index=False)                    # Save the output file in the media folder

        # render the correct link in the upload page
        context = {
            "url" : output_file_path,                                      # pass the file link in context
            "file_name" : Path(uploaded_file.name).stem +'.csv',
        }
        return render(request,'parser_app/upload.html', context)
    
    # for get request, render the upload page
    return render(request, 'parser_app/upload.html')               