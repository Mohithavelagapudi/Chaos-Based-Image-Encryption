# 🌀 Chaos-Based Image Encryption & Secure Communication

<div align="center">

<img src="https://img.shields.io/badge/Domain-Chaos%20Cryptography-7B68EE" />
<img src="https://img.shields.io/badge/Language-Python-3776AB" />
<img src="https://img.shields.io/badge/Focus-Image%20Security-FF5722" />
<img src="https://img.shields.io/badge/Status-Research%20Prototype-00BFA6" />

</div>

> **Harnessing nonlinear dynamical systems (Arnold Cat Map & Henon Map) to achieve confusion and diffusion for robust image encryption.**

---

## ❗ Problem Statement
Modern multimedia systems demand strong protection of visual data. Conventional ciphers struggle with large, high-correlation image datasets. This project applies chaos theory to craft encryption that is:
- Highly sensitive to initial conditions (keys)
- Pseudo-random and structure-destroying
- Resistant to statistical, brute-force, and differential attacks

---

## 🔧 Core Techniques ("Tiles")
<table>
  <tr>
    <td>
      <strong>🐈 Arnold Cat Map</strong><br/>
      Periodic, fast pixel position permutation introducing strong <em>confusion</em>.<br/>
      <details>
        <summary>Formula</summary>
        
        $$
        \begin{bmatrix} x' \\ y' \end{bmatrix} =
        \begin{bmatrix} 1 & 1 \\ 1 & 2 \end{bmatrix}
        \begin{bmatrix} x \\ y \end{bmatrix} \mod N
        $$
        
        Iterated k times ⇒ key component.
      </details>
    </td>
    <td>
      <strong>🌀 Henon Map</strong><br/>
      Chaotic sequence generation for pixel value masking (XOR) → <em>confusion + diffusion</em>.<br/>
      <details>
        <summary>Formula</summary>
        
        $$
        \begin{aligned}
        x_{n+1} &= 1 - a x_n^2 + y_n \\
        y_{n+1} &= b x_n
        \end{aligned}
        $$
        Typical: \(a = 1.4,\; b = 0.3\)
      </details>
    </td>
    <td>
      <strong>🔐 Socket Framework</strong><br/>
      Client/Server transfer of encrypted payloads for network validation.<br/>
      Ensures confidentiality in transit.
    </td>
  </tr>
</table>

---

## 🧮 Methodology Snapshot
> [!TIP]
> Chaos enhances classical principles: permutation (confusion) + substitution/masking (diffusion).

### 1️⃣ Arnold Cat Map Workflow
1. Load square image (pad if needed).
2. Apply matrix transform iteratively (key-driven iteration count).
3. Output permuted image (cipher stage 1).
4. Decrypt by inverse iteration (same count).

### 2️⃣ Henon Map Workflow
1. Initialize \(x_0, y_0, a, b\) ⇒ secret key set.
2. Iterate to produce chaotic float sequence.
3. Scale & quantize to 8-bit mask array matching image dimensions.
4. XOR original / permuted image with mask ⇒ ciphertext.
5. Regenerate mask with identical key to reverse XOR.

---

## 📊 Comparative Feature Grid
| Technique | Confusion | Diffusion | Key Sensitivity | Histogram Resistance | Speed |
|-----------|-----------|-----------|-----------------|----------------------|-------|
| Arnold Cat Map | ✅ High | ⚠️ Low | ✅ High | ⚠️ Moderate | 🚀 Fast |
| Henon Map | ✅ High | ✅ High | ✅ High | ✅ Strong | ⏱️ Medium |

---

## 🔍 Observations
> [!NOTE]
> Combining both (permutation + masking) forms a hybrid cipher with layered security.
- Arnold Cat alone keeps pixel values intact ⇒ vulnerable to statistical analysis if iteration count is small.
- Henon-based XOR alters value distribution ⇒ stronger entropy & flatter histograms.
- Parameter/key perturbations (1e-12 scale) yield dramatically different outputs.

---

## 🧠 Key Insights
- Chaotic dynamics naturally embed unpredictability + sensitivity ⇒ ideal cryptographic primitives.
- Multi-map or multi-phase designs (e.g., Cat → Henon → Diffusion pass) can mitigate singular weaknesses.
- Practical for real-time (low-latency) encryption in surveillance / telemedicine when optimized.

---

## 📂 Project Structure
```
Chaos_techniques.ipynb      # Interactive exploration & prototype implementations
arnoldcat_client.py         # Client for sending encrypted images
arnoldcat_server.py         # Server receiving & decrypting images
test_images/                # Sample plaintext images
Project Report.pdf          # Extended analysis & results
```

---

## 🚀 Quick Start
```bash
# (Pseudo example – adjust to your environment)
python arnoldcat_server.py &   # Start server
python arnoldcat_client.py --image test_images/spidey.jpg --mode henon
```

---

## 🔑 Parameter & Key Considerations
| Map | Primary Secret Components | Expansion Strategy |
|-----|---------------------------|--------------------|
| Cat | Iteration count k, image size N | Combine with dynamic iteration schedule |
| Henon | a, b, x0, y0, sequence length | Derive per-session seeds via KDF |

---

## 🧪 Potential Extensions
- Hybrid multi-chaos pipeline
- GPU acceleration (NumPy → CuPy / PyTorch)
- Differential attack metrics (NPCR, UACI) integration
- Key space & entropy benchmarking

---

## 📜 Mathematical Integrity
All formulas use GitHub-compatible LaTeX blocks:
- Display: `$$ ... $$`
- Inline: `\( ... \)`

---

## ⚠️ Disclaimer
This is a research-oriented prototype. Do not deploy for production-grade security without formal cryptanalysis and hardened key management.

---

## 🤝 Contributions
Ideas, optimizations, and security reviews are welcome. Open an issue or submit a PR.

---

## 📄 License
Distributed for academic/research use. (Add explicit license file if needed.)

---

<div align="center">
Made with chaos theory 🔁 for secure pixels
</div>
