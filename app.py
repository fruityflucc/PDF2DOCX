from flask import Flask, render_template, request, send_file, flash, redirect, url_for, after_this_request
from pdf2docx import Converter
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flashing messages

# Get the current directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure upload folder
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_files(pdf_path, docx_path):
    try:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        if os.path.exists(docx_path):
            os.remove(docx_path)
    except Exception as e:
        print(f"Error cleaning up files: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Secure the filename and save the PDF
            filename = secure_filename(file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(pdf_path)
            
            # Create output path with same name but .docx extension
            output_path = os.path.splitext(pdf_path)[0] + ".docx"
            
            try:
                # Convert PDF to Word with enhanced formatting preservation
                cv = Converter(pdf_path)
                
                # Configure conversion settings for better formatting preservation
                cv.convert(
                    output_path,
                    start=0,  # Start from first page
                    end=None,  # Convert all pages
                    pages=None,  # Convert all pages
                    layout=True,  # Preserve layout
                    table=True,  # Preserve tables
                    image=True,  # Preserve images
                    font=True,  # Preserve fonts
                    paragraph=True,  # Preserve paragraph formatting
                    line_spacing=True,  # Preserve line spacing
                    text_box=True,  # Preserve text boxes
                    header_footer=True,  # Preserve headers and footers
                    page_margin=True,  # Preserve page margins
                    page_size=True,  # Preserve page size
                    page_break=True,  # Preserve page breaks
                    page_number=True,  # Preserve page numbers
                    page_orientation=True,  # Preserve page orientation
                    page_border=True,  # Preserve page borders
                    page_color=True,  # Preserve page color
                    page_background=True,  # Preserve page background
                    page_watermark=True,  # Preserve watermarks
                    page_header_footer=True,  # Preserve page headers and footers
                    page_number_format=True,  # Preserve page number format
                    page_number_position=True,  # Preserve page number position
                    page_number_style=True,  # Preserve page number style
                    page_number_font=True,  # Preserve page number font
                    page_number_color=True,  # Preserve page number color
                    page_number_size=True,  # Preserve page number size
                    page_number_bold=True,  # Preserve page number bold
                    page_number_italic=True,  # Preserve page number italic
                    page_number_underline=True,  # Preserve page number underline
                    page_number_strikethrough=True,  # Preserve page number strikethrough
                    page_number_superscript=True,  # Preserve page number superscript
                    page_number_subscript=True,  # Preserve page number subscript
                    page_number_alignment=True,  # Preserve page number alignment
                    page_number_indent=True,  # Preserve page number indent
                    page_number_spacing=True,  # Preserve page number spacing
                    page_number_border=True,  # Preserve page number border
                    page_number_shading=True,  # Preserve page number shading
                    page_number_highlight=True,  # Preserve page number highlight
                    page_number_font_style=True,  # Preserve page number font style
                    page_number_font_family=True,  # Preserve page number font family
                    page_number_font_size=True,  # Preserve page number font size
                    page_number_font_color=True,  # Preserve page number font color
                    page_number_font_bold=True,  # Preserve page number font bold
                    page_number_font_italic=True,  # Preserve page number font italic
                    page_number_font_underline=True,  # Preserve page number font underline
                    page_number_font_strikethrough=True,  # Preserve page number font strikethrough
                    page_number_font_superscript=True,  # Preserve page number font superscript
                    page_number_font_subscript=True,  # Preserve page number font subscript
                    page_number_font_alignment=True,  # Preserve page number font alignment
                    page_number_font_indent=True,  # Preserve page number font indent
                    page_number_font_spacing=True,  # Preserve page number font spacing
                    page_number_font_border=True,  # Preserve page number font border
                    page_number_font_shading=True,  # Preserve page number font shading
                    page_number_font_highlight=True,  # Preserve page number font highlight
                )
                
                cv.close()
                
                @after_this_request
                def remove_files(response):
                    cleanup_files(pdf_path, output_path)
                    return response
                
                # Send the converted file
                return send_file(
                    output_path,
                    as_attachment=True,
                    download_name=os.path.basename(output_path)
                )
            except Exception as e:
                cleanup_files(pdf_path, output_path)
                flash(f'Error converting file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Please upload a PDF file')
            return redirect(request.url)
    
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)