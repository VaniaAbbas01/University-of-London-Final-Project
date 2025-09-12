const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("audioFile");
const fileInfo = document.getElementById("fileInfo");
const fileName = document.getElementById("fileName");
const analyzeBtn = document.getElementById("analyzeBtn");
const form = document.getElementById("uploadForm");

// Drag and drop functionality
uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("dragover");
});

uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("dragover");
});

uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("dragover");

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect();
    }
});

// File selection handler
fileInput.addEventListener("change", handleFileSelect);

function handleFileSelect() {
    const file = fileInput.files[0];
    if (file) {
        fileName.textContent = `📎 ${file.name} (${formatFileSize(
            file.size
        )})`;
        fileInfo.style.display = "block";
        analyzeBtn.style.display = "inline-block";

        // Update upload area appearance
        uploadArea.style.borderColor = "#7c3aed";
        uploadArea.querySelector(".upload-text").textContent =
            "File ready for analysis!";
        uploadArea.querySelector(".upload-subtext").textContent =
            'Click "Analyze My Speech" to continue';
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

// Form submission with loading state
form.addEventListener("submit", (e) => {
    const btn = analyzeBtn;
    btn.innerHTML = "Analyzing...";
    btn.disabled = true;

    // Re-enable after 2 seconds to prevent permanent disable on error
    setTimeout(() => {
        btn.disabled = false;
        btn.innerHTML = "Analyze My Speech";
    }, 2000);
});

// Click outside to reset if no file selected
uploadArea.addEventListener("click", (e) => {
    if (e.target === uploadArea || e.target.closest(".upload-area")) {
        fileInput.click();
    }
});


/* transcription page JavaScript */
const textarea = document.getElementById("transcription");
const charCount = document.getElementById("charCount");
const transcriptionForm = document.getElementById("transcriptionForm");
const confirmBtn = document.getElementById("confirmBtn");
const loadingOverlay = document.getElementById("loadingOverlay");

// Character counter
function updateCharCount() {
    const count = textarea.value.length;
    charCount.textContent = count.toLocaleString();

    // Color coding based on length
    if (count < 100) {
        charCount.style.color = "#ff6b6b";
    } else if (count < 500) {
        charCount.style.color = "#ffd93d";
    } else {
        charCount.style.color = "#6bcf7f";
    }
}

// Initialize character count
updateCharCount();
textarea.addEventListener("input", updateCharCount);

// Auto-resize textarea
textarea.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = Math.max(300, this.scrollHeight) + "px";
});

// Form submission with loading state
transcriptionForm.addEventListener("submit", function (e) {
    if (textarea.value.trim().length < 10) {
        e.preventDefault();
        alert(
            "Please ensure your transcription has at least 10 characters for meaningful analysis."
        );
        return;
    }

    // Show loading overlay
    loadingOverlay.style.display = "flex";
    confirmBtn.innerHTML = "<span>⏳</span> Analyzing...";
    confirmBtn.disabled = true;

    // Update progress bar
    const progressFill = document.querySelector(".progress-fill");
    progressFill.style.width = "100%";
});

// Go back function
function goBack() {
    if (
        confirm(
            "Are you sure you want to go back? Any changes to the transcription will be lost."
        )
    ) {
        window.history.back();
    }
}

// Keyboard shortcuts
document.addEventListener("keydown", function (e) {
    // Ctrl/Cmd + Enter to submit
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        form.submit();
    }

    // Escape to go back
    if (e.key === "Escape") {
        goBack();
    }
});

// Auto-save to localStorage (optional feature)
let saveTimeout;
textarea.addEventListener("input", function () {
    clearTimeout(saveTimeout);
    saveTimeout = setTimeout(() => {
        localStorage.setItem(
            "speakeasy_transcription_backup",
            textarea.value
        );
    }, 1000);
});

// Restore from localStorage if available
window.addEventListener("load", function () {
    const backup = localStorage.getItem("speakeasy_transcription_backup");
    if (backup && !textarea.value.trim()) {
        if (
            confirm(
                "We found a saved transcription. Would you like to restore it?"
            )
        ) {
            textarea.value = backup;
            updateCharCount();
        }
    }
});

// Clear backup on successful submission
transcriptionForm.addEventListener("submit", function () {
    localStorage.removeItem("speakeasy_transcription_backup");
});

// Animate progress bar on load
window.addEventListener("load", function () {
    setTimeout(() => {
        document.querySelector(".progress-fill").style.width = "75%";
    }, 500);
});