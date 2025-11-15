# File: `index.html`

- Size: 13713 bytes
- Lines: 290
- SHA256: `de4da0ffa41bd09db767495e5f624ff18e25675819a1775693c231df82dcc96d`

## Top of file (first lines)
```
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MNIST MLP – Visualisierung der Inferenz</title>
  <script type="module" crossorigin src="./assets/main.js"></script>
  <link rel="stylesheet" crossorigin href="./assets/main.css">
</head>
<body>

    <!-- 2D Grid Overlay -->
    <div id="overlay2d" class="overlay-2d">
      <div class="container">
        <div id="gridContainer" class="grid-container"></div>
      </div>
    </div>

    <!-- Reset Button -->
    <div id="resetButtonContainer" class="reset-button-container">
        <button id="resetBtn">✖</button>
    </div>

    <!-- Prediction Chart Overlay -->
    <div id="predictionOverlay" class="prediction-overlay">
        <div class="prediction-container">
            <div id="predictionChart"></div>
        </div>
        <div id="networkInfoPanel" class="network-info-panel"></div>
    </div>

    <!-- Instructions Overlay -->
    <div id="instructionsOverlay" class="instructions-overlay">
        <div class="instructions-container">
            <div class="instructions-content">
                <p><strong>Zeichnen:</strong> Auf dem Raster klicken und ziehen (Rechtsklick zum Löschen)</p>
                <p><strong>3D-Steuerung:</strong> • Linke Taste + ziehen = drehen • Rechte Taste + ziehen = verschieben • Scrollrad = zoomen</p>
            </div>
        </div>
    </div>

    <!-- Mobile Instructions Overlay -->
    <div id="mobileInstructionsOverlay" class="mobile-instructions-overlay">
        <div class="mobile-instructions-content">
            <div class="mobile-instructions-title">Touch-Steuerung</div>
            <ul class="mobile-gesture-list">
                <li><strong>Zeichnen:</strong> Tippen und auf dem Raster ziehen</li>
                <li><strong>Drehen:</strong> Mit einem Finger ziehen</li>
                <li><strong>Verschieben:</strong> Mit zwei Fingern bewegen</li>
                <li><strong>Zoomen:</strong> Finger zusammenziehen oder spreizen</li>
            </ul>
        </div>
    </div>

    <!-- Floating Controls -->
    <div class="floating-controls">
        <button
            id="advancedSettingsButton"
            class="floating-button advanced-settings-button"
            aria-haspopup="dialog"
            aria-controls="advancedSettingsModal"
            type="button"
        >
            <span>⚙</span>
        </button>
        <button
            id="infoButton"
            class="floating-button info-button"
            aria-haspopup="dialog"
            aria-controls="infoModal"
            type="button"
        >
            <span>i</span>
        </button>
    </div>

    <!-- MNIST Sample Images - Bottom Edge -->
    <div id="mnistImagesContainer" class="mnist-images-container"></div>

    <!-- Neuron Detail Panel -->
```

## Suggested validation / test commands
- Inspect in browser: open the `index.html` or render with a static server