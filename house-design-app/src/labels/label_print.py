import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black, white
import os
import re # Import the regular expression module

def create_labels_pdf(
    input_file_path,
    output_pdf_path="printed_labels.pdf",
    product_col_name="Product Name",
    dimensions_col_name="Dimensions",
    default_label_width_cm=4.5,
    default_label_height_cm=3.0,
    margin_left_cm=1.0,
    margin_top_cm=1.0,
    gap_x_cm=0.2,
    gap_y_cm=0.2,
    font_name="Helvetica", # Default fallback font for English
    tamil_font_name="NotoSansTamil", # Logical name for the registered Tamil font (e.g., NotoSansTamil-Regular.ttf)
    tamil_font_path=None, # Path to the .ttf file for the regular Tamil font
    font_size_product=10
):
    df = None
    try:
        if input_file_path.endswith('.xlsx'):
            df = pd.read_excel(input_file_path)
        elif input_file_path.endswith('.csv'):
            df = pd.read_csv(input_file_path, encoding='utf-8')
        elif input_file_path.endswith('.txt'):
            encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
            for enc in encodings_to_try:
                try:
                    df = pd.read_csv(input_file_path, sep='\t', encoding=enc)
                    print(f"Successfully read '{input_file_path}' with encoding: {enc}")
                    break
                except UnicodeDecodeError:
                    print(f"Failed to read with encoding: {enc}. Trying next...")
                    continue
            if df is None:
                raise ValueError("Could not read .txt file with common encodings. Please ensure it's UTF-8.")
        else:
            raise ValueError("Unsupported input file format. Use .xlsx, .txt, or .csv.")
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_file_path}'")
        return
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    if df is None or product_col_name not in df.columns or dimensions_col_name not in df.columns:
        print(f"Error: Missing required columns or failed to load DataFrame. Ensure '{product_col_name}' and '{dimensions_col_name}' exist.")
        if df is not None:
            print(f"Available columns: {df.columns.tolist()}")
        return

    df[['Label_Width_Temp', 'Label_Height_Temp']] = df[dimensions_col_name].str.split('*', expand=True).astype(float)
    df = df.sort_values(by=['Label_Width_Temp', 'Label_Height_Temp']).reset_index(drop=True)
    df = df.drop(columns=['Label_Width_Temp', 'Label_Height_Temp'])

    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    page_width_pt, page_height_pt = A4

    margin_left_pt = margin_left_cm * cm
    margin_top_pt = margin_top_cm * cm
    gap_x_pt = gap_x_cm * cm
    gap_y_pt = gap_y_cm * cm

    current_x_pos = margin_left_pt
    current_y_pos = page_height_pt - margin_top_pt
    max_height_in_row_pt = 0

    styles = getSampleStyleSheet()

    active_font_for_paragraph = font_name
    regular_tamil_font_successfully_registered = False

    print(f"Attempting to register Tamil font:")
    
    if tamil_font_path and os.path.exists(tamil_font_path):
        try:
            pdfmetrics.registerFont(TTFont(tamil_font_name, tamil_font_path))
            print(f"SUCCESS: Registered regular Tamil font: '{tamil_font_name}' from '{tamil_font_path}'")
            active_font_for_paragraph = tamil_font_name
            regular_tamil_font_successfully_registered = True
        except Exception as e:
            print(f"WARNING: Could not register regular Tamil font '{tamil_font_name}' from '{tamil_font_path}': {e}. Tamil text may not render correctly.")
    else:
        print(f"WARNING: Regular Tamil font path '{tamil_font_path}' is not valid or not provided. Tamil text will use fallback font '{font_name}'.")

    base_product_style_template = styles['Normal']
    base_product_style_template.fontSize = font_size_product
    base_product_style_template.leading = font_size_product * 1.2
    base_product_style_template.alignment = TA_CENTER
    base_product_style_template.textColor = white

    for index, row in df.iterrows():
        raw_product_name = str(row[product_col_name])
        dimensions_str = str(row[dimensions_col_name])
        
        # --- MODIFICATION START ---
        # Use regex to find English part and Tamil part in parentheses
        match = re.match(r'^(.*?)\s*(\(.*?\))$', raw_product_name)
        if match:
            english_part = match.group(1).strip()
            tamil_part_with_parentheses = match.group(2).strip()
            # Construct the string with a line break using ReportLab's RML tag <br/>
            # The <font name="..."> tag ensures the Tamil part explicitly uses the Tamil font
            # if it was registered, or the fallback otherwise.
            product_name_for_display = (
                f"{english_part}<br/>"
                f"<font name='{active_font_for_paragraph}'>{tamil_part_with_parentheses}</font>"
            )
        else:
            # If no Tamil part in parentheses is found, use the name as is
            product_name_for_display = raw_product_name
        
        print(f"Processing item: '{raw_product_name}' -> Displaying as: '{product_name_for_display}' (Dimensions: {dimensions_str})")
        # --- MODIFICATION END ---

        try:
            width_str, height_str = dimensions_str.split('*')
            label_width_cm = float(width_str)
            label_height_cm = float(height_str)
        except (ValueError, IndexError):
            print(f"Warning: Invalid dimension format '{dimensions_str}' for '{raw_product_name}'. "
                  f"Using default label size {default_label_width_cm}x{default_label_height_cm} cm.")
            label_width_cm = default_label_width_cm
            label_height_cm = default_label_height_cm

        label_width_pt = label_width_cm * cm
        label_height_pt = label_height_cm * cm

        if current_x_pos + label_width_pt > page_width_pt - margin_left_pt:
            current_x_pos = margin_left_pt
            current_y_pos -= (max_height_in_row_pt + gap_y_pt)
            max_height_in_row_pt = 0

        if current_y_pos - label_height_pt < margin_top_pt:
            c.showPage()
            current_x_pos = margin_left_pt
            current_y_pos = page_height_pt - margin_top_pt
            max_height_in_row_pt = 0

        max_height_in_row_pt = max(max_height_in_row_pt, label_height_pt)

        is_circular_label = (label_width_cm == 3.5 and label_height_cm == 3.5)
        
        if is_circular_label:
            radius_pt = label_width_pt / 2
            center_x = current_x_pos + radius_pt
            center_y = current_y_pos - radius_pt

            c.setFillColor(black)
            c.circle(center_x, center_y, radius_pt, fill=1)

            c.setStrokeColorRGB(0.5, 0.5, 0.5)
            c.circle(center_x, center_y, radius_pt, fill=0)
            
            label_render_x_start = current_x_pos
            label_render_y_start = current_y_pos - label_height_pt
            
        else:
            c.setFillColor(black)
            c.rect(current_x_pos, current_y_pos - label_height_pt, label_width_pt, label_height_pt, fill=1)

            c.setStrokeColorRGB(0.5, 0.5, 0.5)
            c.rect(current_x_pos, current_y_pos - label_height_pt, label_width_pt, label_height_pt, fill=0)

            label_render_x_start = current_x_pos
            label_render_y_start = current_y_pos - label_height_pt
        
        product_style = styles['Normal']
        product_style.fontName = active_font_for_paragraph # Ensure this is used for both English and Tamil parts by default
        product_style.bold = 0 
        product_style.fontSize = font_size_product
        product_style.leading = product_style.fontSize * 1.2
        product_style.alignment = TA_CENTER
        product_style.textColor = white

        text_padding_x = 0.2 * cm
        text_padding_y = 0.2 * cm

        available_width_for_text = label_width_pt - (2 * text_padding_x)
        available_height_for_text = label_height_pt - (2 * text_padding_y)

        # Pass the prepared string to Paragraph
        while True:
            product_paragraph = Paragraph(product_name_for_display, product_style)
            w, h = product_paragraph.wrapOn(c, available_width_for_text, available_height_for_text)

            if (w <= available_width_for_text and h <= available_height_for_text) or product_style.fontSize <= 4:
                break
            product_style.fontSize -= 0.5
            product_style.leading = product_style.fontSize * 1.2

        product_y = label_render_y_start + (label_height_pt - h) / 2
        
        product_paragraph.drawOn(c, label_render_x_start + text_padding_x, product_y)

        current_x_pos += (label_width_pt + gap_x_pt)

    c.save()
    print(f"Successfully created labels PDF: {output_pdf_path}")


if __name__ == "__main__":
    tamil_regular_font_file = "NotoSansTamil-Regular.ttf"

    input_data_file = "label_data.txt"
    output_pdf_file = "my_printed_labels_tamil_newline.pdf" # New output name for clarity

    product_name_column = "Product Name"
    dimensions_column = "Dimensions"

    create_labels_pdf(
        input_file_path=input_data_file,
        output_pdf_path=output_pdf_file,
        product_col_name=product_name_column,
        dimensions_col_name=dimensions_column,
        tamil_font_path=tamil_regular_font_file,
        tamil_font_name="NotoSansTamil",
        font_size_product=12
    )