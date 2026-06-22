from flask import Flask, render_template, jsonify, send_file
import os
import json
import glob
from pathlib import Path
import numpy as np
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__, template_folder='templates', static_folder='static')

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')


def _list_png_files(category):
    category_dir = os.path.join(RESULTS_DIR, category)
    if not os.path.isdir(category_dir):
        return []
    return sorted(glob.glob(os.path.join(category_dir, '*.png')))


def _image_count(category):
    return len(_list_png_files(category))


def _image_url(category, filename):
    return f'/api/image-file/{category}/{filename}'

@app.route('/')
def index():
    """Serve the modern dashboard page"""
    return render_template('index_modern.html')

@app.route('/api/metrics')
def get_metrics():
    """Get overall metrics (PSNR, SSIM) from results"""
    try:
        metrics = {
            'psnr': 'N/A',
            'ssim': 'N/A',
            'total_images': 0,
            'last_updated': 'N/A',
            'status': 'waiting'
        }
        
        # Parse metrics from a metrics file if it exists
        metrics_file = os.path.join(RESULTS_DIR, 'metrics.json')
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                loaded_metrics = json.load(f)
                metrics.update(loaded_metrics)
                metrics['status'] = 'ready'
        else:
            # Calculate from image counts
            sr_images = glob.glob(os.path.join(RESULTS_DIR, 'sr', '*.png'))
            metrics['total_images'] = len(sr_images)
            metrics['message'] = 'Run inference first: python3 inference/test.py'
            if sr_images:
                metrics['status'] = 'images_found_no_metrics'
            else:
                metrics['status'] = 'no_data'
        
        return jsonify(metrics), 200
    except Exception as e:
        print(f"Error getting metrics: {e}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/images')
def get_images():
    """Get list of all result images"""
    try:
        category_files = {
            category: _list_png_files(category)
            for category in ['lr', 'sr', 'hr', 'compare']
        }

        total_images = max((len(files) for files in category_files.values()), default=0)
        images = []

        for index in range(total_images):
            image_set = {'index': index}
            for category, files in category_files.items():
                if index < len(files):
                    filename = os.path.basename(files[index])
                    image_set[category] = {
                        'filename': filename,
                        'url': _image_url(category, filename)
                    }
                else:
                    image_set[category] = None

            primary = image_set.get('lr') or image_set.get('sr') or image_set.get('hr') or image_set.get('compare')
            image_set['name'] = primary['filename'] if primary else f'image_{index + 1:04d}.png'
            images.append(image_set)

        return jsonify({
            'images': images,
            'total_images': total_images,
            'category_counts': {
                'lr': len(category_files['lr']),
                'sr': len(category_files['sr']),
                'hr': len(category_files['hr']),
                'compare': len(category_files['compare'])
            }
        }), 200
    except Exception as e:
        print(f"Error getting images: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/image/<category>/<filename>')
def get_image(category, filename):
    """Serve a specific image"""
    try:
        if category not in ['sr', 'lr', 'hr', 'compare']:
            return jsonify({'error': 'Invalid category'}), 400
        
        image_path = os.path.join(RESULTS_DIR, category, filename)
        
        if not os.path.exists(image_path):
            return jsonify({'error': 'Image not found'}), 404
        
        # Convert to base64 for display
        with Image.open(image_path) as img:
            img_io = BytesIO()
            img.save(img_io, format='PNG')
            img_io.seek(0)
            img_base64 = base64.b64encode(img_io.getvalue()).decode()
        
        return jsonify({'image': f'data:image/png;base64,{img_base64}'}), 200
    except Exception as e:
        print(f"Error getting image: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics')
def get_statistics():
    """Get overall project statistics"""
    try:
        stats = {
            'total_sr_images': _image_count('sr'),
            'total_lr_images': _image_count('lr'),
            'total_hr_images': _image_count('hr'),
            'total_comparisons': _image_count('compare'),
            'total_images': max(_image_count('lr'), _image_count('sr'), _image_count('hr'), _image_count('compare')),
            'model_name': 'CGA Model',
            'dataset': 'Satellite Images',
            'scale_factor': '4x'
        }

        return jsonify(stats), 200
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/image/<int:idx>')
def get_image_by_index(idx):
    """Get URLs to all four images for a specific index"""
    try:
        # Get list of all images to find the actual filename
        lr_images = sorted(glob.glob(os.path.join(RESULTS_DIR, 'lr', '*.png')))
        
        if idx < 0 or idx >= len(lr_images):
            return jsonify({'error': 'Image index out of range'}), 404
        
        # Get the actual filename from the LR directory
        lr_file = os.path.basename(lr_images[idx])
        
        images = {}
        
        # Return URLs instead of base64 encoded data
        for category in ['lr', 'sr', 'hr', 'compare']:
            category_dir = os.path.join(RESULTS_DIR, category)
            
            # Try exact match first
            image_path = os.path.join(category_dir, lr_file.replace('lr_', category + '_'))
            
            # If not found, try to find any file at this index position
            if not os.path.exists(image_path):
                category_images = sorted(glob.glob(os.path.join(category_dir, '*.png')))
                if idx < len(category_images):
                    image_path = category_images[idx]
                    image_name = os.path.basename(image_path)
                else:
                    # Placeholder if category doesn't have this image
                    image_path = None
                    image_name = None
            else:
                image_name = os.path.basename(image_path)
            
            if image_path and os.path.exists(image_path) and image_name:
                # Return a URL to serve the image
                images[category] = f'/api/image-file/{category}/{image_name}'
            else:
                images[category] = None
        
        return jsonify({
            'lr': images.get('lr'),
            'sr': images.get('sr'),
            'hr': images.get('hr'),
            'comparison': images.get('compare')
        }), 200
    except Exception as e:
        print(f"Error getting image by index: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/image-file/<category>/<filename>')
def get_image_file(category, filename):
    """Serve an image file directly"""
    try:
        if category not in ['sr', 'lr', 'hr', 'compare']:
            return jsonify({'error': 'Invalid category'}), 400
        
        image_path = os.path.join(RESULTS_DIR, category, filename)
        
        if not os.path.exists(image_path):
            return jsonify({'error': 'Image not found'}), 404
        
        # Serve the file directly
        return send_file(image_path, mimetype='image/png')
    except Exception as e:
        print(f"Error serving image file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download/<category>/<filename>')
def download_image(category, filename):
    """Download an image file with proper filename"""
    try:
        if category not in ['sr', 'lr', 'hr', 'compare']:
            return jsonify({'error': 'Invalid category'}), 400
        
        image_path = os.path.join(RESULTS_DIR, category, filename)
        
        if not os.path.exists(image_path):
            return jsonify({'error': 'Image not found'}), 404
        
        # Serve the file with download headers
        return send_file(
            image_path,
            as_attachment=True,
            download_name=f'{category}_{filename}',
            mimetype='image/png'
        )
    except Exception as e:
        print(f"Error downloading image: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sample-comparison/<int:idx>')
def get_sample_comparison(idx):
    """Get a specific comparison with all four images"""
    try:
        comparison = {
            'idx': idx,
            'images': {}
        }
        
        filename = f'{idx:04d}.png'
        for category in ['lr', 'sr', 'hr', 'compare']:
            image_path = os.path.join(RESULTS_DIR, category, filename)
            if os.path.exists(image_path):
                with Image.open(image_path) as img:
                    img_io = BytesIO()
                    img.save(img_io, format='PNG')
                    img_io.seek(0)
                    img_base64 = base64.b64encode(img_io.getvalue()).decode()
                    comparison['images'][category] = f'data:image/png;base64,{img_base64}'
        
        return jsonify(comparison), 200
    except Exception as e:
        print(f"Error getting comparison: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
