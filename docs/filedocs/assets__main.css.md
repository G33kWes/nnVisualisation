# File: `assets/main.css`

- Size: 20568 bytes
- Lines: 1009
- SHA256: `7cd6f265ab9b164c571c6557097221b33aab2c9fe7841815712165f2ade33f61`

## Top of file (first lines)
```
:root {
  color-scheme: dark;
  font-family: "Inter", "Segoe UI", sans-serif;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  background: radial-gradient(circle at 20% 20%, #2d3f72, #101a33 65%);
  color: #f5f7ff;
  overflow: hidden;
}

body > canvas {
  position: fixed !important;
  inset: 0;
  width: 100vw !important;
  height: 100vh !important;
  z-index: 1 !important;
}

.overlay-2d {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 10;
  pointer-events: none;
}

.overlay-2d .container {
  pointer-events: auto;
  background: rgba(10, 16, 30, 0.88);
  border: 1px solid rgba(91, 160, 255, 0.35);
  border-radius: 18px;
  padding: 16px 18px;
  backdrop-filter: blur(18px);
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.45);
}

.grid-container {
  display: flex;
  flex-direction: column;
  gap: 14px;
  align-items: stretch;
}

.grid-interaction-row {
  display: flex;
  align-items: stretch;
  gap: 12px;
}

.grid-title {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(173, 205, 255, 0.85);
}

.grid {
  display: grid;
  grid-template-columns: repeat(28, 1fr);
  gap: 1px;
  background: rgba(18, 26, 48, 0.85);
  border-radius: 12px;
  padding: 8px;
  box-shadow: inset 0 0 12px rgba(0, 0, 0, 0.55);
  touch-action: none;
}

.grid-cell {
  width: 10px;
  height: 10px;
  border-radius: 3px;
```

## Suggested validation / test commands
- File type: .css — manual inspection suggested