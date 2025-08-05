# 🐍 Snakalytics: An AI Analysis Lab for the Snake Game 
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-6E7072?style=for-the-badge&logo=pygame&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931A?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logoColor=white&cache_bust=1)
![Seaborn](https://img.shields.io/badge/Seaborn-094363?style=for-the-badge&logoColor=white&cache_bust=1)

Welcome to **Snakalytics**! A complete platform designed to train, analyze, and compare the performance of different Artificial Intelligence agents playing the classic Snake game.

This project was built for students and developers who want a practical and visual environment to learn about AI algorithms, test new strategies, and understand the nuances of machine learning through clear metrics and interactive dashboards.
<p align="center">
<img src="https://github.com/felipegluck/Snakalytics/blob/main/dashboard_exp.gif" alt="Dashboard Example" width="500"/>
</p>

## Core Concept

The Snakalytics workflow is simple and powerful:

1.  **Generate Data:** Use the fake data generator (`gen_fake_data.py`) to instantly populate the dashboard, or play the game yourself (`snake_game.py`) to create a record of your own matches. The ultimate goal is to adapt `snake_game.py` to be controlled by your own AI agents.
2.  **Collect Stats:** Every completed game automatically saves its statistics (score, moves, time) to `.json` files.
3.  **Analyze & Compare:** Launch the interactive dashboard (`dashboard.py`) to load data from multiple agents, visualize learning curves, compare score distributions, and rank performance with advanced metrics.

---

## ✨ Key Features

Snakalytics comes with a suite of tools to accelerate your development and analysis cycle:

* **Interactive Dashboard:** A web interface built with Streamlit for intuitive and visual analysis.
* **Clear Learning Curve:** Visualize the performance evolution of agents over time with a rolling average to smooth out noise and identify real trends.
* **Detailed Statistical Analysis:** Use box plots and histograms to understand the consistency, variability, and score distribution of each agent.
* **Quantitative Performance Metrics:**
    * **Average Score:** The agent's overall performance.
    * **Consistency (Standard Deviation):** How predictable the agent's results are. Lower is better.
    * **Learning Rate (Slope):** The slope of the learning curve, indicating how quickly the agent improves.
    * **Efficiency Metric (Cost per Point):** Measures how many games an agent needs to reach a proficiency threshold, weighted by its average score.
* **Agent Ranking:** A dynamic leaderboard that ranks agents based on different strategies (Balanced, Max Performance, Fast Learner), allowing for a quick assessment of the best agent for each scenario.
* **Customizable Environment:** Filter agents, adjust the rolling average window, and set proficiency thresholds to focus your analysis on what matters most.
---

## 🚀 Getting Started

Get your analysis lab running in just a few commands.

1.  **Clone the Repository:**
    ```sh
    git clone [https://github.com/YOUR-USERNAME/snakalytics.git](https://github.com/YOUR-USERNAME/snakalytics.git)
    cd snakalytics
    ```

2.  **(Recommended) Create a Virtual Environment:**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

---

## How to Use
> **Note:** Run these commands from the root directory of your project.
<br/>

**Option A: Generate Sample Data (Quick Start)**

Run the `gen_fake_data.py` script to instantly create multiple statistics files (`.json`). This is ideal for testing the dashboard without needing to play the game.

```sh
python gen_fake_data.py
```
**Option B: Play the Game or Run an AI**

Run the Pygame client to play the game yourself or to run an AI model. Each completed game will automatically save its data (score, moves, time) to the `game_stats.json` file.

```sh
python snake_game.py
```

Tip: Rename the game_stats.json file (e.g., stats_my_ai_v1.json) to compare different agents on the dashboard.

**Option C: Analyze the Results on the Dashboard**

With one or more statistics files (.json) in your folder, launch the interactive dashboard with the following command.
```sh
streamlit run dashboard.py
```

---
## Understanding the Dashboard

* **📈 Learning Curve:** This chart shows the rolling average score for each agent. An upward-trending line indicates that the agent is learning and improving over time. Compare the slopes to see which agent learns fastest.
* **📊 Score Distribution:** The **Box Plot** shows the median and consistency, while the **Histogram** displays the most frequent scores. Peaks and boxes further to the right indicate superior performance.
* **🏆 Performance Leaderboard:** This table summarizes key metrics and normalizes them to create a **Weighted Final Score**. Use the presets ("Max Performance," "Fast Learner") to re-rank the agents and discover which one excels under each strategy.
---
## 🧠 Key Technical Learnings

This project was an exercise in building a full-stack data application, from backend logic to a front-end interface.

* **Weighted Ranking Algorithm:** Designed and implemented a custom scoring algorithm that normalizes multiple metrics (score, consistency, etc.) and applies user-selected weights for flexible agent ranking.
* **Interactive Data Visualization:** Built a dynamic dashboard with `Streamlit`, using components like sliders, tabs, and real-time plot updates to create a responsive user experience.
* **Statistical Analysis with Scikit-learn:** Leveraged `Scikit-learn`'s linear regression models to programmatically calculate and display the learning rate (slope) for each agent.
* **Robust Game State Logic:** Engineered a pause-aware timer in `Pygame` that accurately tracks elapsed game time by isolating and subtracting paused intervals.
* **Defensive Dashboard Programming:** Implemented data validation and helper functions (`safe_normalize`, `@st.cache_data`) to handle edge cases like empty datasets, prevent errors, and ensure a performant UI.
* **Procedural Data Simulation:** Used Python's `random` library to generate realistic test data that simulates different AI "personalities" (e.g., aggressive vs. cautious).

---
## 🔮 Future Development

The current platform is a solid foundation. The roadmap is focused on integrating real intelligence and improving usability.

* [ ] **Implement Baseline AI:** Integrate a classic reinforcement learning algorithm (e.g., Q-learning) to serve as a benchmark agent.
* [ ] **Create an Agent API:** Develop a simple class interface so users can easily "plug in" their own AI models for evaluation.
* [ ] **Add File Uploads:** Allow users to upload their own `stats.json` files directly to the Streamlit dashboard.
* [ ] **Enhance Game Environment:** Add UI controls to the Pygame client to change game speed and board size.
* [ ] **Package for PyPI:** Package the project for easy installation via `pip install snakalytics`.
* [ ] **Enhance Game Visual:** Implement a more visually attractive snake game in `snake_game.py`.
---
## How to Contribute

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## License [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
Distributed under the MIT License. See `LICENSE.txt` for more information.
