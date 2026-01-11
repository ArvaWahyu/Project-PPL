
// Logic sederhana untuk auto-submit dan markdown
function handleFileSelect() {
    const fileInput = document.getElementById('fileInput');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const form = document.getElementById('uploadForm');

    if (fileInput.files.length > 0) {
        // Tampilkan loading
        loadingOverlay.classList.remove('hidden');
        loadingOverlay.classList.add('flex');

        // Submit otomatis
        form.submit();
    }
}

// Render markdown saat halaman dimuat (jika ada hasil) dan Setup Drag & Drop
document.addEventListener('DOMContentLoaded', () => {
    // 1. Markdown Parsing
    const rawMarkdown = document.getElementById('raw-markdown');
    const targetDiv = document.getElementById('rendered-markdown');

    if (rawMarkdown && targetDiv) {
        targetDiv.innerHTML = marked.parse(rawMarkdown.textContent);
    }

    // 2. Drag and Drop Logic
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');

    if (dropZone && fileInput) {
        // Prevent default behavior (Prevent file from being opened)
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Highlight drop zone
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            dropZone.classList.add('border-herbal-500', 'bg-herbal-50');
            // Add visual helper if visual wrapper is inside
            const visualWrapper = dropZone.querySelector('div');
            if (visualWrapper) {
                visualWrapper.classList.add('border-herbal-500', 'bg-herbal-100');
            }
        }

        function unhighlight(e) {
            dropZone.classList.remove('border-herbal-500', 'bg-herbal-50');
            const visualWrapper = dropZone.querySelector('div');
            if (visualWrapper) {
                visualWrapper.classList.remove('border-herbal-500', 'bg-herbal-100');
            }
        }

        // Handle Drop
        dropZone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;

            if (files.length > 0) {
                fileInput.files = files; // Assign dropped files to input
                handleFileSelect();      // Trigger auto-submit
            }
        }
    }
});
