/* global elements */
const form = document.getElementById('detect-form');
const textInput = document.getElementById('text-input');
const submitBtn = document.getElementById('submit-btn');

const resultSection = document.getElementById('result-section');
const resultCard = document.getElementById('result-card');
const resultIcon = document.getElementById('result-icon');
const resultLabel = document.getElementById('result-label');
const meterFill = document.getElementById('meter-fill');
const meterValue = document.getElementById('meter-value');
const confidenceValue = document.getElementById('confidence-value');

const errorSection = document.getElementById('error-section');
const errorMessage = document.getElementById('error-message');

function showError(msg) {
  resultSection.classList.add('hidden');
  errorMessage.textContent = msg;
  errorSection.classList.remove('hidden');
}

function showResult(data) {
  errorSection.classList.add('hidden');

  const isRumor = data.label === 'rumor';
  const pct = Math.round(data.rumor_probability * 100);

  resultCard.className = 'result-card ' + (isRumor ? 'rumor' : 'not-rumor');
  resultIcon.textContent = isRumor ? '⚠️' : '✅';
  resultLabel.textContent = isRumor ? 'Likely a Rumor' : 'Likely Factual';
  meterFill.style.width = pct + '%';
  meterValue.textContent = pct + '%';
  confidenceValue.textContent = Math.round(data.confidence * 100) + '%';

  resultSection.classList.remove('hidden');
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const text = textInput.value.trim();
  if (!text) {
    showError('Please enter some text before analyzing.');
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = 'Analyzing…';

  try {
    const response = await fetch('/api/detect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      showError(err.detail || `Server error (${response.status}). Please try again.`);
      return;
    }

    const data = await response.json();
    showResult(data);
  } catch (err) {
    showError('Network error. Please check your connection and try again.');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Analyze';
  }
});
