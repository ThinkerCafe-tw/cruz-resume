# Cruz Tang - Multilingual Professional Resume

🔗 **View Online:** [https://thinkercafe-tw.github.io/cruz-resume/](https://thinkercafe-tw.github.io/cruz-resume/)

---

## 🌍 Multi-Language Support

This resume is available in **5 languages**:
- 🇹🇼 繁體中文 (Traditional Chinese) - Default
- 🇺🇸 English
- 🇯🇵 日本語 (Japanese)
- 🇰🇷 한국어 (Korean)
- 🇸🇦 العربية (Arabic) - with RTL support

Switch languages using the selector in the top-right corner.

---

## ✨ Features

### Interactive Design
- **Dark/Light Mode** - Toggle between themes
- **Scroll Progress Bar** - Track reading progress
- **Smooth Animations** - Content fades in as you scroll
- **Hover Effects** - Interactive cards and buttons

### Responsive
- Desktop optimized (1200px+)
- Tablet friendly (768px - 1200px)
- Mobile ready (<768px)
- Print optimized (for PDF export)

### Accessibility
- RTL language support (Arabic)
- High contrast text
- Semantic HTML structure
- Keyboard navigation friendly

---

## 👨‍💻 About Cruz Tang

**AI-Native Leader & System Architect**

### Career Highlights
- 🌍 Managed 300+ international team members at Topvan Group (China, Philippines, Malaysia, Vietnam, 2020-2023)
- 🗺️ Overseas experience: Dubai Business Bay (4 months), Philippines Clark (1.5 years), Makati/BGC (1 year)
- 🤖 Founded ThinkerCafe - AI education and automation solutions
- 🎓 10+ years teaching experience (資策會, 文化大學, 金融研訓院)
- 🏆 iPAS AI Application Specialist Exam Committee Member (工研院)

### Expertise
- **Operations Leadership** - International team management at scale
- **AI Implementation** - Claude API, OpenAI, LINE Bot, AI agents
- **Enterprise Automation** - RPA, workflow design, process optimization
- **Technical Training** - Translating complexity into actionable knowledge

---

## 🎯 Currently Seeking

Opportunities to work with enterprise clients on:
- AI Application Consulting
- Digital Transformation
- Solution Architecture (AI/Automation)
- Technical Project Management

**Work Arrangement:** Remote-friendly, flexible schedule
**Location:** Taipei, Taichung, Tainan, or fully remote
**Compensation:** 70K-100K TWD/month

---

## 📫 Contact

- 📧 Email: cruz@thinker.cafe
- 💼 LinkedIn: [linkedin.com/in/sulaxd](https://www.linkedin.com/in/sulaxd/)
- 🌐 Company: [thinker.cafe](https://thinker.cafe)
- 📱 Phone: +886 937 431 998

---

## 🛠️ Technical Implementation

### Built With
- Pure HTML/CSS/JavaScript (no frameworks)
- CSS Variables for theming
- Intersection Observer API for animations
- No external dependencies

### Design Philosophy
- AI-native aesthetic (dark mode first)
- Data-driven presentation (stats, metrics)
- Interactive but professional
- Minimal but powerful

### Browser Support
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

---

## 🤖 AI Translation Workflow

This project uses **AI-powered automatic translation** to maintain 5 language versions from a single source.

### How It Works

1. **Single Source of Truth**: Maintain only Traditional Chinese (zh-TW) content in `data.json`
2. **AI Translation**: Use Gemini 2.5 Flash API to translate to 4 other languages
3. **Cultural Adaptation**: Each language has custom localization prompts
4. **Automatic Deployment**: GitHub Actions workflow handles translation + commit

### Translation Pipeline

```
zh-TW (original) → Gemini API → en, ja, ko, ar → Auto-commit → Deploy
```

### Usage

#### Local Translation

```bash
# Install dependencies
cd scripts
pip install -r requirements.txt

# Set up API key
cp ../.env.example ../.env
# Edit .env and add your GEMINI_API_KEY

# Run translation
python translate.py
```

#### GitHub Actions (Automated)

1. Go to **Actions** tab
2. Select "🌐 Auto-Translate Resume"
3. Click "Run workflow"
4. Results are automatically committed

**Setup Guide**: See [.github/SETUP.md](.github/SETUP.md)

### Features

- ✅ **Localization Prompts**: Custom cultural adaptation for each language
- ✅ **Structure Validation**: Ensures translated JSON matches original structure
- ✅ **Auto Backup**: Creates timestamped backups before translation
- ✅ **Error Handling**: Individual language failures don't block others
- ✅ **Dry Run Mode**: Test translations without saving changes

### Technical Details

- **Model**: Gemini 2.5 Flash (`gemini-2.0-flash-exp`)
- **Temperature**: 0.3 (for consistency)
- **Max Tokens**: 8192
- **Cost**: Free tier (15 requests/minute)

For more details, see [scripts/README.md](scripts/README.md)

---

## 🚀 Development Roadmap

### Completed
- [x] Multi-language support (5 languages)
- [x] AI-powered auto-translation workflow
- [x] Dark/Light mode toggle
- [x] Responsive design (mobile/tablet/desktop)
- [x] Print-optimized layout

### Planned
- [ ] Analytics integration (track language/version usage)
- [ ] SEO optimization
- [ ] Open Graph tags for social sharing
- [ ] Custom domain (resume.thinker.cafe)
- [ ] Download PDF button
- [ ] Additional persona modes (Teaching, Proposal, Speaker)

---

## 📄 License

© 2025 Cruz Tang. All rights reserved.

---

Last Updated: January 2025
