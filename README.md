# ✨ Magicals — The Manimverse You’ve Always Wanted

Welcome to **Magicals**, your all-in-one creative hub where math meets motion and imagination goes viral. It’s not just a project — it’s your personal universe of AI-powered Manim magic, remix culture, and creator-driven reels that blend art, code, and storytelling.

## 🌈 What Is Magicals?

Magicals is a **community platform for Manim creators** — think of it as the TikTok of mathematical animation, but smarter and actually useful. Users can upload, edit, and share their Manim projects (aka *Magicals*), each consisting of a video and the source code that made it. Every Magical is a spark of creativity — remixable, likable, and fully discoverable.

Whether you’re a beginner exploring Manim or a seasoned visual storyteller, Magicals gives you a playground to experiment, collaborate, and shine.

## 🧠 Core Features

* **🎥 AI-Powered Manim Reels:** Automatically generate and render animations directly from your code.
* **🧑‍💻 Code + Video in One Magical:** Each upload stores both your source and rendered video together.
* **💾 Cloud Storage via Supabase:** Secure, scalable storage for videos, code, and profile data.
* **✨ Discover Page:** Explore trending Magicals, like, comment, and remix others’ creations.
* **📈 Creator Analytics:** Visualize engagement, watch time, and reach with gorgeous live charts.
* **👤 User Profiles:** Personal bios, profile pics, and all your published Magicals in one place.
* **🌓 Light & Dark Themes:** Smooth theme toggle for both daydreamers and night coders.
* **⚡ Real-Time Reactions:** Likes and comments update live, no refresh needed.
* **🔐 Streamlit Auth Integration:** Secure logins, signups, and sessions handled cleanly with Supabase.
* **🪄 Upload Integration:** Direct uploads from the Magical Manim desktop app — users must be signed in to post.

## 🏗️ Tech Stack

* **Frontend:** Streamlit + Tailwind-inspired custom styling
* **Backend:** Supabase (Auth + Storage + Postgres)
* **Framework:** Modular Streamlit architecture with dynamic page routing
* **Storage Buckets:**

  * `videos` (50 MB limit)
  * `code` (10 MB limit)
  * `avatars` (1 MB limit)

## 🚀 How to Run Locally

1. **Clone the repo:**

   ```bash
   git clone https://github.com/yourusername/magicals.git
   cd magicals
   ```
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
3. **Set up Supabase secrets:**
   Create a file named `.streamlit/secrets.toml` and add:

   ```toml
   [supabase]
   url = "https://YOUR-PROJECT.supabase.co"
   key = "YOUR-ANON-KEY"
   ```
4. **Run it:**

   ```bash
   streamlit run app.py
   ```

## 💡 Project Philosophy

Magicals is built on the belief that math is art — and code is expression. It’s designed to feel human, collaborative, and fluid. Every frame rendered, every like given, every Magical shared adds to a collective story of creativity in motion.

## 🧩 Modular Design

* `app.py`: The main brain connecting all modules
* `utils/`: Handles Supabase integration, theming, authentication, and storage
* `pages/`: Home, Upload, Discover, Analytics, and Profile modules
* `components/`: Cards, video displays, and UI blocks for reusability

## ❤️ Community & Contribution

We’re building a universe together. Feel free to contribute, open issues, or propose features. Creators are the heart of Magicals.

> **"Every frame you render adds a spark to the cosmos." — Team Magicals**

---

### 🌐 Live App

[magicals.streamlit.app](https://magicals.streamlit.app)

### 📬 Contact

For collabs, ideas, or feature requests, hit us up at `support@magicals.dev`

---

Built with 💜, Python, and way too much caffeine by **Soumalya**.
