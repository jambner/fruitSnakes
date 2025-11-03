# 🍉 FruitSnakes

A fun and enhanced take on the classic Snake game — now with **special fruits** that can **help or hurt** your snake!  
Built using Python and [pygame](https://www.pygame.org/).

---

## 🎮 Features

- **Classic snake gameplay** with arrow-key controls  
- **Three types of fruits:**
  - 🍎 **Normal Fruit** – +1 length, +1 score  
  - 🍋 **Golden Fruit** – +3 length, +5 score, temporary speed boost  
  - 🍏 **Rotten Fruit** – -1 length, -3 score, temporary slow down  
- **Dynamic difficulty:** temporary speed changes keep the game exciting  
- **Simple pixel-style graphics**  
- **Game Over screen** with final score display  

---

## 🧠 Game Rules

| Fruit Type | Effect | Score | Speed Impact |
|-------------|---------|--------|---------------|
| 🍎 Normal | +1 length | +1 | Normal |
| 🍋 Golden | +3 length | +5 | Faster (temporary) |
| 🍏 Rotten | -1 or -2 length | -3 | Slower (temporary) |

Avoid hitting the walls or your own tail — doing so ends the game!

---

## 🛠️ Installation

### 1️⃣ Requirements
Make sure you have:
- **Python 3.8+**
- **pip** (Python package manager)
- **pygame** installed

Install pygame using:
```bash
pip install pygame
