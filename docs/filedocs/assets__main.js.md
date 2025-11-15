# File: `assets/main.js`

- Size: 108289 bytes
- Lines: 2936
- SHA256: `74bd585ee55978b8ac9f7874cc718f4805a5ea635078430377385557410e16ae`

## Top of file (first lines)
```
const VISUALIZER_CONFIG = {
  weightUrl: "./exports/mlp_weights.json",
  maxConnectionsPerNeuron: 24,
  layerSpacing: 5.5,
  inputSpacing: 0.24,
  hiddenSpacing: 0.95,
  inputNodeSize: 0.18,
  hiddenNodeRadius: 0.22,
  connectionRadius: 0.005,
  connectionWeightThreshold: 0,
  showFpsOverlay: true,
  brush: {
    drawRadius: 1.4,
    eraseRadius: 2.5,
    drawStrength: 0.95,
    eraseStrength: 0.95,
    softness: 0.3,
  },
};

const MNIST_SAMPLE_MANIFEST_URL = "./assets/data/mnist-test-manifest.json";

document.addEventListener("DOMContentLoaded", () => {
  initializeVisualizer().catch((error) => {
    console.error(error);
    renderErrorMessage("Visualisierung konnte nicht initialisiert werden. Details finden Sie in der Konsole.");
  });
});

async function loadMnistTestSamples(manifestPath = MNIST_SAMPLE_MANIFEST_URL) {
  const manifestUrl = new URL(manifestPath, window.location.href);
  const manifestResponse = await fetch(manifestUrl.toString());
  if (!manifestResponse.ok) {
    throw new Error(`Konnte MNIST-Manifest nicht laden (${manifestResponse.status}).`);
  }
  const manifest = await manifestResponse.json();
  const rows = Number(manifest?.imageShape?.[0]) || 28;
  const cols = Number(manifest?.imageShape?.[1]) || 28;
  const numSamples = Number(manifest?.numSamples) || 0;
  const sampleSize = rows * cols;
  const imageFile = manifest?.image?.file;
  const labelFile = manifest?.labels?.file;
  if (!imageFile || !labelFile) {
    throw new Error("Manifest enthält keine gültigen Dateipfade für Bilder oder Labels.");
  }

  const [imageBuffer, labelBuffer] = await Promise.all([
    fetch(new URL(imageFile, manifestUrl).toString()).then((response) => {
      if (!response.ok) {
        throw new Error(`Konnte MNIST-Bilddaten nicht laden (${response.status}).`);
      }
      return response.arrayBuffer();
    }),
    fetch(new URL(labelFile, manifestUrl).toString()).then((response) => {
      if (!response.ok) {
        throw new Error(`Konnte MNIST-Labeldaten nicht laden (${response.status}).`);
      }
      return response.arrayBuffer();
    }),
  ]);

  const imageBytes = new Uint8Array(imageBuffer);
  const labelBytes = new Uint8Array(labelBuffer);
  if (numSamples <= 0) {
    if (sampleSize > 0) {
      const inferredSamples = Math.floor(imageBytes.length / sampleSize);
      if (inferredSamples <= 0) {
        throw new Error("Aus den MNIST-Bilddaten konnte keine Stichprobengröße abgeleitet werden.");
      }
      if (labelBytes.length !== inferredSamples) {
        throw new Error("Anzahl der Labels stimmt nicht mit den abgeleiteten Stichproben überein.");
      }
    } else {
      throw new Error("Manifest enthält keine gültige Stichprobengröße.");
    }
  }

  const totalSamples = numSamples > 0 ? numSamples : Math.floor(imageBytes.length / sampleSize);
  if (imageBytes.length !== totalSamples * sampleSize) {
    throw new Error("MNIST-Bilddatenlänge stimmt nicht mit der erwarteten Größe überein.");
```

## Suggested validation / test commands
- File type: .js — manual inspection suggested