# Screenshots & Features

## Overview

Resume Shortlisting provides an intuitive interface for screening candidates using AI-powered resume matching. Below are the key screens and features.

## Screen 1: Landing Page

**Location**: `http://localhost:3000` (or production URL)

**Features**:
- Clean header with app branding
- Hero section explaining the solution
- Call-to-action directing to upload form

**Visual Elements**:
- FileText icon in header
- "Resume Shortlisting" title
- "AI-powered resume screening & candidate matching" subtitle
- Description: "Upload resumes and job descriptions to get instant AI-powered matching scores..."

**What Happens**:
1. User sees the landing page
2. Upload form is visible below hero section
3. User can start immediately without any additional clicks

---

## Screen 2: Resume Upload & Job Description Form

**Location**: Main area of home page

**Components**:

### Part A: Resume Upload Area
- **Drag & Drop Zone**: Gray dashed border, becomes blue on drag-over
- **Upload Icon**: Large upload icon showing current state
- **File Status**:
  - Empty: "Drag & drop a PDF resume here" with Browse button
  - Loaded: Shows filename, file size, "Change file" button
- **Accepted Formats**: PDF and DOCX files
- **Max Size**: 10 MB

```
┌─────────────────────────────────┐
│ Step 1: Upload Resume           │
├─────────────────────────────────┤
│                                 │
│      📤 Drag & drop PDF here    │
│         or click to browse      │
│                                 │
│      [Browse Files] button      │
│                                 │
└─────────────────────────────────┘
```

### Part B: Job Description Textarea
- **Label**: "Job Requirements"
- **Input**: Large textarea (200px min height)
- **Helper Text**: Character counter "XXX characters"
- **Placeholder**: "Enter the job description, required skills, qualifications..."
- **Real-time Validation**: Requires non-empty text

```
┌─────────────────────────────────┐
│ Step 2: Job Description         │
├─────────────────────────────────┤
│ Job Requirements                │
│ ┌──────────────────────────────┐│
│ │ We are looking for a Python  ││
│ │ developer with 5+ years...   ││
│ │                              ││
│ │                              ││
│ └──────────────────────────────┘│
│ 542 characters                  │
└─────────────────────────────────┘
```

### Part C: Matching Options
- **Toggle**: "Use AI semantic matching"
- **Subtitle**: "Slower but more accurate (uses BERT)"
- **Default**: Off (uses fast TF-IDF)
- **Option to Enable**: Check for BERT scoring

```
┌─────────────────────────────────┐
│ Matching Options                │
├─────────────────────────────────┤
│ ☐ Use AI semantic matching      │
│   Slower but more accurate      │
│     (uses BERT)                 │
└─────────────────────────────────┘
```

### Part D: Error Display (if any)
- **Alert Box**: Red background, rounded corners
- **Icon**: Alert circle icon
- **Messages**:
  - "Only PDF and DOCX files are supported"
  - "File exceeds 10 MB size limit"
  - "Job description must not be empty"
  - "Could not extract text from PDF"

```
┌─────────────────────────────────┐
│ ⚠️  Error                       │
│ Could not reach backend at      │
│ http://localhost:8000.          │
│ Make sure it's running and      │
│ accessible.                     │
└─────────────────────────────────┘
```

### Part E: Submit Button
- **Label**: "Analyze Resume" with arrow icon
- **State**:
  - **Disabled**: Gray, when form invalid
  - **Loading**: Shows spinner "Processing..." when API call in progress
  - **Ready**: Blue (accent color), clickable
- **Action**: Calls backend API `/score` endpoint

```
Button States:

[Disabled]        [Loading]           [Ready]
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Analyze      │  │ ⟳ Processing │  │ Analyze      │
│ Resume →     │  │ ...           │  │ Resume →     │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## Screen 3: Results Display Page

**Location**: `/results` (after form submission)

**Displays**: Real-time data from backend

### Part A: Candidate Summary Card

**Layout**: Header with badge

```
┌──────────────────────────────────────┐
│ 👤 john-doe.pdf                   ✅ │
│ Resume Scoring Summary          RECOMMENDED │
│                                      │
│ Overall Match Score                  │
│ ████████████████░░ 78.5%  GREEN      │
│                                      │
│ This candidate shows strong alignment│
│ with the job requirements...         │
│                                      │
│ Analyzed using: BERT+TFIDF method    │
└──────────────────────────────────────┘
```

**Data Displayed**:
- Resume filename (extracted from upload)
- Match score (0-100%, color-coded)
- Progress bar (width = score percentage)
- Decision badge:
  - ✅ Green "Recommended" (score ≥ 70%)
  - ❌ Red "Below Threshold" (score < 70%)
- Interpretation text
- Method used

**Color Coding**:
- 🟢 Green: 85-100% (Excellent match)
- 🟡 Yellow: 70-84% (Good match)
- 🔴 Red: Below 70% (Poor match)

### Part B: Key Metrics Grid (2 columns)

**Left Card**: Skills Matched

```
┌─────────────────────┐
│ 💻 Skills Matched   │
├─────────────────────┤
│ 5                   │
│                     │
│ [python] [fastapi]  │
│ [sql] [docker]      │
│ [aws]               │
└─────────────────────┘
```

**Right Card**: Experience

```
┌─────────────────────┐
│ 📅 Experience       │
├─────────────────────┤
│ 5.0                 │
│                     │
│ years estimated     │
│ from resume         │
└─────────────────────┘
```

### Part C: Top Job Keywords

**Display**: Pill-shaped badges with important keywords

```
┌──────────────────────────────────────┐
│ Top Job Keywords                     │
│ Important keywords ranked by         │
│ importance                           │
├──────────────────────────────────────┤
│ [python] [fastapi] [machine]         │
│ [learning] [sql] [docker]            │
│ [kubernetes] [rest] [api]            │
└──────────────────────────────────────┘
```

### Part D: Analysis Details

**Table**: Statistics and metadata

```
┌──────────────────────────────────────┐
│ Analysis Details                     │
│ Resume and Job Description Stats    │
├──────────────────────────────────────┤
│ Resume Characters:      3,421        │
│ Job Description:        541          │
│ Matching Algorithm:     BERT+TFIDF   │
└──────────────────────────────────────┘
```

---

## Feature Highlights

### 1. Drag & Drop Upload
- **Interaction**: Click or drag file to upload area
- **Feedback**: Visual highlight on drag-over
- **Validation**: Real-time file type and size checks
- **UX**: Clear error messages if invalid

### 2. Real-Time Form Validation
- **Resume**: PDF/DOCX, < 10MB, starts with %PDF
- **Job Description**: Non-empty, trimmed
- **Button**: Disabled until both valid
- **Error Display**: Red alert box with specific message

### 3. Loading States
- **Button**: Shows spinner during API call
- **Progress**: Visual feedback (prevents double-submission)
- **Error Handling**: Catches and displays API errors

### 4. Results Visualization
- **Score Bar**: Animated progress bar with percentage
- **Color Coding**: Visual indicators for match quality
- **Badges**: Skills shown as interactive badges
- **Cards**: Organized information in card layout

### 5. Skill Detection
- **Automatic**: Detects 20+ technical skills
- **Matching**: Shows only skills in both resume and job
- **Display**: Badges with skill names
- **Count**: Total skills matched shown prominently

### 6. Experience Extraction
- **Smart Detection**: Regex patterns + keyword heuristics
- **Display**: Estimated years prominently shown
- **Accuracy**: Works with resume formats

### 7. Matching Methods
- **TF-IDF**: Default, fast (< 1 second)
- **BERT**: Optional, accurate (3-5 seconds)
- **Toggle**: User can choose speed vs accuracy
- **Auto-Fallback**: Graceful fallback if BERT unavailable

### 8. Recommendation Logic
- **Threshold**: 70% score
- **Recommended**: Green badge, positive feedback
- **Below Threshold**: Red badge, suggestions to consider
- **Transparent**: Shows methodology and confidence

---

## User Flows

### Happy Path (Successful Match)

```
1. User lands on home page
2. Drags resume.pdf to upload zone
3. Sees: "resume.pdf (45.2 KB)" confirmation
4. Types job description (500+ characters)
5. Clicks "Analyze Resume"
6. Sees: Loading spinner for 1-2 seconds
7. Redirected to /results
8. Sees: Match score 78.5% with ✅ Recommended
9. Views: Skills matched, experience, keywords
10. Makes hiring decision ✓
```

### Error Handling (Invalid File)

```
1. User tries to upload .txt file
2. Error: "Only PDF and DOCX files are supported"
3. Button stays disabled (red border on error)
4. User uploads correct .pdf file
5. Error clears, button enables
6. Continues with form ✓
```

### Alternative Path (BERT Matching)

```
1. User checks "Use AI semantic matching"
2. Checkbox shows enabled state
3. Submits form
4. Sees: "Processing..." (3-5 seconds, longer than usual)
5. Results show: method_used = "bert+tfidf"
6. Potentially higher/different score than TF-IDF
7. Views detailed semantic matching results ✓
```

---

## Responsive Design

### Desktop (1024px+)
- Side-by-side cards (2-column grid)
- Full-width form
- Horizontal layout for metrics

### Tablet (768px - 1024px)
- Single column with spacing
- Responsive cards
- Touch-friendly buttons

### Mobile (< 768px)
- Stacked layout
- Full-width inputs
- Large touch targets (48px minimum)
- Optimized spacing

---

## Accessibility Features

- ✅ Semantic HTML (`<form>`, `<label>`, `<button>`)
- ✅ ARIA labels on icons
- ✅ Color + text for status (not color-only)
- ✅ Keyboard navigation support
- ✅ Focus indicators on buttons
- ✅ Alt text on images/icons
- ✅ High contrast colors (WCAG AA)

---

## Performance Metrics

**Frontend Load Time**:
- Initial page load: ~1-2 seconds
- API request: ~200-500ms (TF-IDF) or 3-5s (BERT)
- Results display: Instant

**Backend Response**:
- Text extraction: ~50-100ms
- TF-IDF scoring: ~50-100ms
- BERT scoring: ~3-5 seconds (CPU)
- Total API latency: ~100ms - 5s

---

## Next Steps for Users

1. **Try the App**: Upload your own resume + job description
2. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) to go live
3. **Customize**: Edit skill detection in `backend/services/ml_logic.py`
4. **Enhance**: Add features like batch processing, history, etc.
5. **Monitor**: Track performance with Vercel + Render analytics

---

**Ready to screen resumes?** Start at http://localhost:3000 or deploy to production! 🚀
