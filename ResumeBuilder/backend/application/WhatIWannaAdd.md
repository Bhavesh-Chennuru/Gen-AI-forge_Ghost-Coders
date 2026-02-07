# 🎓 VidyaMitra - AI-Powered Career Guidance Platform

An intelligent career agent that helps students and professionals with resume evaluation, skill assessment, personalized training plans, mock interviews, and progress tracking.

## ✨ Features

- 📄 **Resume Analyzer** - Upload and analyze resumes with AI-powered ATS scoring
- 🎯 **Skill Evaluation** - Identify skill gaps for target job roles
- 📚 **Training Plans** - Get personalized learning roadmaps
- ❓ **Quiz System** - AI-generated quizzes to test your knowledge
- 💼 **Mock Interviews** - Practice interviews with real-time AI feedback
- 📊 **Progress Dashboard** - Track your learning journey

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your-api-key-here
```

Get your free Gemini API key: https://aistudio.google.com/app/apikey

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
vidyamitra/
├── app.py                          # Main application
├── pages/                          # Individual page modules
│   ├── 1_🏠_Home.py
│   ├── 2_📄_Resume_Analyzer.py
│   ├── 3_🎯_Skill_Evaluation.py
│   ├── 4_📚_Training_Plan.py
│   ├── 5_❓_Quiz_System.py
│   ├── 6_💼_Mock_Interview.py
│   └── 7_📊_Progress_Dashboard.py
├── utils/                          # Helper functions
│   ├── gemini_ai.py
│   ├── pdf_parser.py
│   └── session_manager.py
├── requirements.txt
├── .env                           # Your API keys (create this)
└── README.md
```

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **AI**: Google Gemini 2.0 Flash Thinking
- **PDF Processing**: PyPDF2
- **Visualization**: Plotly
- **Data**: Pandas

## 📖 How to Use

1. **Upload Resume** - Start by uploading your resume in the Resume Analyzer
2. **Set Goals** - Define your target job role
3. **Evaluate Skills** - Get AI-powered skill gap analysis
4. **Follow Plan** - Access personalized training recommendations
5. **Practice** - Take quizzes and mock interviews
6. **Track Progress** - Monitor your improvement over time

## ⚙️ Configuration

All configuration is done through the `.env` file:

- `GEMINI_API_KEY` - Required for AI features
 
## 🤝 Contributing

This is a learning project. Feel free to:
- Report bugs
- Suggest features
- Improve code

## 📝 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

- Built with Streamlit
- Powered by Google Gemini AI
- Inspired by the need for accessible career guidance

---

**Built with ❤️ for students and professionals**
