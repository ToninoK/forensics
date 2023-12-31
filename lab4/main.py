import os, sys, optparse
from exif import Image
import webbrowser
from PyPDF2 import PdfReader, PdfWriter

def convertGPScoordinate(coordinate, coordinate_ref):
    decimal_degrees = coordinate[0] + \
                      coordinate[1] / 60 + \
                      coordinate[2] / 3600
    
    if coordinate_ref == "S" or coordinate_ref == "W":
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

def figMetaData(file_path):
    img_doc = Image(open(file_path, "rb"))

    if not img_doc.has_exif:
        sys.exit(f"Image does not contain EXIF data.")
    else:
        print(f"Image contains EXIF (version {img_doc.exif_version}) data.")
        
    print(f"{dir(img_doc)}\n")
    return img_doc


def pdfMetaData(file_path):
    pdf_doc = PdfReader(open(path, "rb"))
    if pdf_doc.is_encrypted:
        try:
            if pdf_doc.decrypt("banana") != 1:
                print("target pdf document is encrypted")
                # sys.exit("target pdf document is encrypted")
        except:
            sys.exit("target pdf document is encrypted")

    pdfWriter = PdfWriter()
    for pageNum in range(len(pdf_doc.pages)):
        pdfWriter.add_page(pdf_doc.pages[pageNum])
    resultPdf = open('decrypted_output.pdf', 'wb')
    pdfWriter.write(resultPdf)
    resultPdf.close()


if __name__ == "__main__":
    parser = optparse.OptionParser("Usage: python <script_name> -f <file>")
    parser.add_option("-f", dest="file", type="string", help="please provide full path to the document")

    (options, args) = parser.parse_args()

    url = "http://www.google.com/maps/place"
    path = options.file
    if not path:
        print("please provide full path to the document")
        sys.exit(parser.usage)

    if any(path.endswith(ext) for ext in (".jpg", ".bmp", ".jpeg",)):
        img = figMetaData(path)
        coord_x = convertGPScoordinate(img.gps_latitude, img.gps_latitude_ref)
        coord_y = convertGPScoordinate(img.gps_longitude, img.gps_longitude_ref)
        print(f"GPS coordinates: {img.gps_latitude}, {img.gps_longitude}")
        webbrowser.open_new_tab(f"{url}/{coord_x},{coord_y}")
    elif path.endswith(".pdf"):
        pdfMetaData(path)
    else:
        print("File extension not supported/recognized... Make sure the file has the correct extension...")
