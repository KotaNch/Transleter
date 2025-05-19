import os
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import pytesseract
from googletrans import Translator  # pip install googletrans==4.0.0-rc1
from fpdf import FPDF  # pip install fpdf

# Настройка путей
pdf_path = "your_book.pdf"
output_pdf_path = "translated_book.pdf"

# Шрифт для рендеринга текста в PDF (укажите путь к TTF-файлу шрифта)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Инициализация переводчика
translator = Translator()

# Конвертация PDF в изображения
pages = convert_from_path(pdf_path, dpi=300)

# Инициализация PDF-документа для вывода
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Обработка каждой страницы
for i, page_img in enumerate(pages, 1):
    print(f"Обработка страницы {i}...")

    # Распознавание текста
    text = pytesseract.image_to_string(page_img, lang="eng")

    # Перевод текста
    try:
        translated = translator.translate(text, src='en', dest='ru').text
    except Exception as e:
        translated = "[Ошибка перевода]"
        print(e)

    # Создание изображения с текстом
    img = Image.new('RGB', (2480, 3508), color='white')  # A4 300dpi
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 32)
    draw.multiline_text((100, 100), translated, font=font, fill='black', spacing=10)

    # Сохранение изображения во временный файл
    temp_img_path = f"translated_page_{i}.jpg"
    img.save(temp_img_path)

    # Добавление страницы в PDF
    pdf.add_page()
    pdf.image(temp_img_path, x=0, y=0, w=210, h=297)  # A4 размеры

    # Удаление временного изображения
    os.remove(temp_img_path)

# Сохранение PDF
pdf.output(output_pdf_path)
print(f"Переведённый PDF сохранён как: {output_pdf_path}")
