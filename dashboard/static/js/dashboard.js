// Enhanced Dashboard JavaScript with Modern Features

let currentImageIndex = 0;
let totalImages = 0;
let allImages = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadDashboardData();
    setupSectionNavigation();
    setupAutoRefresh();
});

// Setup sidebar navigation
function setupSectionNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all items
            menuItems.forEach(m => m.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Get the target section
            const targetSection = this.getAttribute('data-section');
            
            // Hide all sections
            document.querySelectorAll('.dashboard-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Show target section
            const sectionElement = document.getElementById(targetSection);
            if (sectionElement) {
                sectionElement.classList.add('active');
            }
        });
    });
    
    // Set metrics as default active
    const metricsItem = document.querySelector('[data-section="metrics"]');
    if (metricsItem) {
        metricsItem.classList.add('active');
    }
    const metricsSection = document.getElementById('metrics');
    if (metricsSection) {
        metricsSection.classList.add('active');
    }
}

// Load all dashboard data
async function loadDashboardData() {
    try {
        await Promise.all([
            loadMetrics(),
            loadStatistics(),
            loadImages()
        ]);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Load metrics
async function loadMetrics() {
    try {
        const response = await fetch('/api/metrics');
        const data = await response.json();
        
        const psnrValue = document.getElementById('psnrValue');
        const ssimValue = document.getElementById('ssimValue');
        const lastUpdated = document.getElementById('lastUpdate');
        
        if (psnrValue && ssimValue) {
            if (data.status === 'ready' && data.psnr !== null && data.ssim !== null) {
                psnrValue.textContent = typeof data.psnr === 'number' ? data.psnr.toFixed(2) : 'N/A';
                ssimValue.textContent = typeof data.ssim === 'number' ? data.ssim.toFixed(4) : 'N/A';
                
                // Update progress bars
                const psnrPercent = Math.min((data.psnr / 50) * 100, 100);
                const ssimPercent = (data.ssim * 100);
                
                const psnrBar = document.getElementById('psnrBar');
                const ssimBar = document.getElementById('ssimBar');
                if (psnrBar) psnrBar.style.width = psnrPercent + '%';
                if (ssimBar) ssimBar.style.width = ssimPercent + '%';
                
                // Update comparison section
                const compPsnr = document.getElementById('compPsnr');
                const compSsim = document.getElementById('compSsim');
                if (compPsnr) compPsnr.textContent = data.psnr.toFixed(2) + ' dB';
                if (compSsim) compSsim.textContent = data.ssim.toFixed(4);
            } else {
                psnrValue.textContent = 'N/A';
                ssimValue.textContent = 'N/A';
            }
        }
        
        if (lastUpdated && data.last_updated) {
            lastUpdated.textContent = 'Last updated: ' + new Date(data.last_updated).toLocaleString();
        }
        
    } catch (error) {
        console.error('Error loading metrics:', error);
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        
        const totalImgs = document.getElementById('totalImages');
        const lrCount = document.getElementById('lrCount');
        const srStatCount = document.getElementById('srStatCount');
        const hrCount = document.getElementById('hrCount');
        const compareCount = document.getElementById('compareCount');
        const srCount = document.getElementById('srCount');
        
        if (totalImgs) totalImgs.textContent = data.total_images || 0;
        if (lrCount) lrCount.textContent = data.total_images || 0;
        if (srStatCount) srStatCount.textContent = data.processed_images || 0;
        if (hrCount) hrCount.textContent = data.total_images || 0;
        if (compareCount) compareCount.textContent = data.total_images || 0;
        if (srCount) srCount.textContent = data.processed_images || 0;
        
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load images
async function loadImages() {
    try {
        const response = await fetch('/api/images');
        const data = await response.json();
        allImages = data.images || [];
        totalImages = allImages.length;
        
        if (totalImages > 0) {
            currentImageIndex = 0;
            displayGallery();
        }
        
    } catch (error) {
        console.error('Error loading images:', error);
    }
}

// Display gallery
function displayGallery() {
    const counter = document.getElementById('imageCounter');
    if (counter) {
        counter.textContent = `Image 1 of ${totalImages}`;
    }
    
    if (allImages.length > 0) {
        loadImage(0);
    }
}

// Load specific image
async function loadImage(index) {
    if (index < 0 || index >= totalImages) return;
    
    currentImageIndex = index;
    
    try {
        const response = await fetch(`/api/image/${index}`);
        const data = await response.json();
        
        const lrImg = document.getElementById('lrImage');
        const srImg = document.getElementById('srImage');
        const hrImg = document.getElementById('hrImage');
        const compImg = document.getElementById('compareImage');
        
        if (lrImg) lrImg.src = data.lr;
        if (srImg) srImg.src = data.sr;
        if (hrImg) hrImg.src = data.hr;
        if (compImg) compImg.src = data.comparison;
        
        // Update counter
        const counter = document.getElementById('imageCounter');
        if (counter) counter.textContent = `Image ${index + 1} of ${totalImages}`;
        
        // Update input
        const imageIndex = document.getElementById('imageIndex');
        if (imageIndex) imageIndex.value = index + 1;
        
    } catch (error) {
        console.error('Error loading image:', error);
    }
}

// Setup event listeners
function setupEventListeners() {
    // Navigation buttons
    const prevBtn = document.getElementById('prevBtn');
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            loadImage((currentImageIndex - 1 + totalImages) % totalImages);
        });
    }
    
    const nextBtn = document.getElementById('nextBtn');
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            loadImage((currentImageIndex + 1) % totalImages);
        });
    }
    
    // Image input
    const goBtn = document.getElementById('goBtn');
    if (goBtn) {
        goBtn.addEventListener('click', function() {
            const imageIndex = document.getElementById('imageIndex');
            if (imageIndex) {
                const index = parseInt(imageIndex.value) - 1;
                if (index >= 0 && index < totalImages) {
                    loadImage(index);
                } else {
                    showNotification('Invalid image number!', 'error');
                }
            }
        });
    }
    
    // Header Refresh button
    const headerRefresh = document.querySelector('.section-header .btn-outline-primary:first-child');
    if (headerRefresh) {
        headerRefresh.addEventListener('click', () => {
            loadDashboardData();
            showNotification('Dashboard refreshed!', 'success');
        });
    }
    
    // Export buttons in header
    const headerExport = document.querySelector('.section-header .btn-outline-primary:last-child');
    if (headerExport) {
        headerExport.addEventListener('click', () => {
            showNotification('Export menu opened', 'info');
        });
    }
    
    // Fullscreen button
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', toggleFullscreen);
    }
    
    // Download button
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadImages);
    }
    
    // Settings export buttons
    const exportCSVBtn = document.getElementById('exportCsvBtn');
    if (exportCSVBtn) {
        exportCSVBtn.addEventListener('click', exportCSV);
    }
    
    const exportJSONBtn = document.getElementById('exportJsonBtn');
    if (exportJSONBtn) {
        exportJSONBtn.addEventListener('click', exportJSON);
    }
}

// Auto-refresh metrics every 30 seconds
function setupAutoRefresh() {
    setInterval(() => {
        loadMetrics();
        loadStatistics();
    }, 30000);
}

// Export functions
async function exportCSV() {
    try {
        const response = await fetch('/api/metrics');
        const data = await response.json();
        
        let csv = 'Metric,Value\n';
        csv += `PSNR,${data.psnr || 'N/A'}\n`;
        csv += `SSIM,${data.ssim || 'N/A'}\n`;
        csv += `Total Images,${data.total_images || 0}\n`;
        csv += `Last Updated,${data.last_updated || 'N/A'}\n`;
        
        downloadFile(csv, 'dashboard-metrics.csv', 'text/csv');
        showNotification('CSV exported successfully!', 'success');
    } catch (error) {
        showNotification('Failed to export CSV', 'error');
    }
}

async function exportJSON() {
    try {
        const response = await fetch('/api/metrics');
        const data = await response.json();
        
        const json = JSON.stringify(data, null, 2);
        downloadFile(json, 'dashboard-metrics.json', 'application/json');
        showNotification('JSON exported successfully!', 'success');
    } catch (error) {
        showNotification('Failed to export JSON', 'error');
    }
}

function downloadImages() {
    showNotification('Download feature coming soon!', 'info');
}

function toggleFullscreen() {
    const gallery = document.querySelector('.gallery-viewer');
    if (gallery) {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        } else {
            gallery.requestFullscreen().catch(err => {
                console.error(`Error attempting to enable fullscreen: ${err.message}`);
            });
        }
    }
}

// Utility functions
function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

function showNotification(message, type = 'info') {
    // Simple notification (can be enhanced with a toast library)
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        font-weight: 600;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
