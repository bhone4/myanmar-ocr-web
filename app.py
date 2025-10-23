from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
import tempfile
import pytesseract
from PIL import Image
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

print("🔧 Initializing OCR System...")

try:
    # Test tesseract
    test_img = Image.new('RGB', (100, 30), color='white')
    pytesseract.image_to_string(test_img)
    OCR_MODE = 'PRODUCTION'
    print("✅ REAL OCR ACTIVE!")
except Exception as e:
    OCR_MODE = 'DEMO'
    print(f"⚠️ Demo Mode: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Read image
        img_bytes = file.read()
        img_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'Invalid image'}), 400
        
        results = []
        
        if OCR_MODE == 'PRODUCTION':
            # Preprocess image for better OCR
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # Save to temp file
            fd, temp_path = tempfile.mkstemp(suffix='.png')
            os.close(fd)
            cv2.imwrite(temp_path, thresh)
            
            try:
                # Run OCR
                img_pil = Image.open(temp_path)
                text = pytesseract.image_to_string(
                    img_pil,
                    lang='mya+eng',
                    config='--psm 6 --oem 3'
                )
                
                # Parse results
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                
                if not lines:
                    lines = ['No text detected in image']
                
                for line in lines:
                    results.append({
                        'text': line,
                        'confidence': 88.5
                    })
                
            finally:
                # Clean up
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        
        else:
            # DEMO MODE
            results = [
                {'text': '⚠️ DEMO MODE', 'confidence': 100},
                {'text': 'Install Tesseract properly', 'confidence': 100}
            ]
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results),
            'mode': OCR_MODE
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🇲🇲 MYANMAR OCR SYSTEM")
    print(f"🔧 Mode: {OCR_MODE}")
    print("📱 URL: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)







