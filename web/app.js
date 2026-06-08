let currentFile = null;
let currentDatasetImagePath = null;

function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(t => t.style.display = 'none');
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    document.getElementById(tabId).style.display = 'block';
    event.currentTarget.classList.add('active');
    
    // Reset state
    currentFile = null;
    currentDatasetImagePath = null;
    document.getElementById('process-btn').disabled = true;
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        currentFile = file;
        currentDatasetImagePath = null;
        
        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('original-img').src = e.target.result;
            document.getElementById('results-section').style.display = 'block';
            document.getElementById('result-img').src = '';
            document.getElementById('process-btn').disabled = false;
            resetStats();
        }
        reader.readAsDataURL(file);
    }
}

async function loadRandomValidationImage() {
    try {
        const response = await fetch('/api/dataset/validation/random');
        if (!response.ok) {
            const err = await response.json();
            alert(err.detail || "Error al cargar imagen del dataset.");
            return;
        }
        
        const data = await response.json();
        currentDatasetImagePath = data.image_path;
        currentFile = null;
        
        document.getElementById('original-img').src = data.image_b64;
        document.getElementById('results-section').style.display = 'block';
        document.getElementById('result-img').src = '';
        document.getElementById('process-btn').disabled = false;
        resetStats();
        
    } catch (error) {
        alert("Error de conexión con el servidor.");
        console.error(error);
    }
}

async function processImage() {
    const btn = document.getElementById('process-btn');
    const loader = document.getElementById('loader');
    
    btn.disabled = true;
    loader.style.display = 'block';
    
    try {
        let response;
        
        if (currentFile) {
            const formData = new FormData();
            formData.append("file", currentFile);
            
            response = await fetch('/api/predict/upload', {
                method: 'POST',
                body: formData
            });
        } else if (currentDatasetImagePath) {
            response = await fetch('/api/predict/dataset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image_path: currentDatasetImagePath })
            });
        } else {
            throw new Error("No hay imagen seleccionada.");
        }
        
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Error en el procesamiento.");
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        alert(error.message);
        console.error(error);
    } finally {
        btn.disabled = false;
        loader.style.display = 'none';
    }
}

function displayResults(data) {
    if (!data.plate_detected) {
        alert("No se detectó ninguna placa en la imagen.");
        return;
    }
    
    document.getElementById('result-img').src = data.output_image_b64 || '';
    document.getElementById('plate-text').innerText = data.plate_text || 'Desconocido';
    document.getElementById('yolo-conf').innerText = `${(data.detection_confidence * 100).toFixed(1)}%`;
    document.getElementById('ocr-conf').innerText = `${(data.ocr_confidence * 100).toFixed(1)}%`;
    
    const validSpan = document.getElementById('format-valid');
    if (data.valid_format) {
        validSpan.innerText = "Sí ✅";
        validSpan.style.color = "var(--success)";
    } else {
        validSpan.innerText = "No ⚠️";
        validSpan.style.color = "var(--danger)";
    }
}

function resetStats() {
    document.getElementById('plate-text').innerText = '-';
    document.getElementById('yolo-conf').innerText = '-';
    document.getElementById('ocr-conf').innerText = '-';
    document.getElementById('format-valid').innerText = '-';
    document.getElementById('format-valid').style.color = 'inherit';
}

// Drag and drop events
const dropZone = document.getElementById('drop-zone');
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'var(--primary)';
});
dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'rgba(255,255,255,0.2)';
});
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'rgba(255,255,255,0.2)';
    if (e.dataTransfer.files.length > 0) {
        document.getElementById('file-input').files = e.dataTransfer.files;
        handleFileSelect({ target: { files: e.dataTransfer.files } });
    }
});
