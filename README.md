# Terminal Lifeform

**TerminalLifeform** is a terminal-native simulation about survival, entropy, and watching little digital lifeforms succeed (or fail).

**Ents live and they die.**  
**Sometimes they even can thrive.**  
**Usually, they die.**

![screenshot](docs/screenshot.png)

---

## 🧬 Features

- 🔁 Terminal UI (with color, progress bars, status indicators)
- 🧬 Object-oriented and modular design
- 🌡 Entities, parameters, and behavior all easily customizable
- 🌈 Built using [uv](https://github.com/astral-sh/uv) and `pyproject.toml` 
- ⚙️ fast, modern Python tooling
- 📈 Exponential decay with age ( non-linear )

---

## 🚀 Getting Started

### 🧰 Requirements

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) (blazing-fast Python package manager)

### Install & Run

```bash
# Clone the repo
git clone https://github.com/jtkIII/TerminalLifeform.git
cd TerminalLifeform

# Setup environment with uv
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Or, if you're using pyproject.toml directly:
uv pip install -e .

# Then run
python src/main.py
````

---

### 📎 Latest List

- ✅ `docs/screenshot.png`
- ✅ `added requirements.txt` for users who don't use `uv` 
- ✅ Mentioned `uv` in `pyproject.toml`'s `[tool]` section


## 🛠 Roadmap Ideas

* [ ] Entity evolution
* [ ] Save/load state
* [ ] Visualization or external UI (textual? curses? pygame?)
* [ ] Entity logging or journaling
* [x] Terminal-only chaos engine


## 🔸 Details of Exponential decay with age:

### 🔍 Behavior of `health_change -= 0.01 * (entity.age ** 1.2)`

| Age | `age * 0.01` (linear) | `0.01 * age^1.2` (nonlinear) |
| --- | --------------------- | ---------------------------- |
| 10  | 0.10                  | 0.16                         |
| 25  | 0.25                  | 0.39                         |
| 50  | 0.50                  | 0.69                         |
| 75  | 0.75                  | 0.95                         |
| 100 | 1.00                  | 1.19                         |

---

### 📈 Why:

1. **Early life penalty is still low** → most new entities survive.
2. **Middle age hits faster** → starts to “cull” slower entities earlier.
3. **Old age kills faster** → leading to a **dip** in long-lived individuals.
4. **Population naturally cycles** → fewer elders = fewer potential reproducers = population waves.
5. **Reproduction pressure shifts younger** → system evolves to favor faster reproducers.

- Adds **emergent dynamics** — population pulses, generational cycles.
- Prevents “hoarding” of old, invincible entities.
- **natural lifespans**, with variability from health, energy, and resilience.

---

```python

# **More gentle aging:**
health_change -= 0.005 * (entity.age ** 1.1)

# **Harsh elder culling:**
health_change -= 0.02 * (entity.age ** 1.5)


# **Exponential death zone:**
if entity.age > 50:
    health_change -= 0.05 * (entity.age - 50) ** 2

```

---

## 📄 License
MIT – open-ended digital life is for everyone.

---

*Created by [@jtkIII](https://github.com/jtkIII). Contributions, forks, and weird extensions welcome.*
