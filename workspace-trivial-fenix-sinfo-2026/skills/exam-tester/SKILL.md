---
name: exam-tester
description: 'Interactive chat-based exam on Fenix course material. Ingests subject content, extracts topics, generates questions dynamically, evaluates answers using the knowledge vault, and provides a final score.'
argument-hint: 'Subject or course name (e.g., "Physics 1", "Advanced Algorithms")'
user-invocable: true
---

# Exam Tester Skill (OpenClaw)

## How it works

The exam-tester skill orchestrates an interactive exam experience entirely through chat. It uses an existing knowledge table, extracts key topics, generates questions on-the-fly, evaluates user answers against the vault content, and provides a final score with topic breakdown.

**Important Note:** If the knowledge vault contains actual tests, exams, or exercises, the skill will vary values, parameters, and naming to ensure questions are not exact copies. This ensures fair testing and prevents memorization of specific examples.

### Workflow Overview

```
1. User invokes: exam-tester
   ↓
2. Agent asks: Which knowledge table should I use?
   (User specifies: e.g., "fenix-physics-1", "exam-advanced-algorithms")
   ↓
3. Agent validates table exists and extracts main topics from vault (via knowledge-query)
   ↓
4. Agent presents topics, asks user to select (chat input)
   ↓
5. Agent asks: How many questions? (user specifies in chat)
   ↓
6. For each question (loop):
   ├─ Generate question via Claude (based on topic + vault content)
   ├─ If actual test/exercise found: vary values/naming to avoid exact copy
   ├─ Present in chat, wait for user answer
   ├─ Query vault for relevant material
   ├─ Evaluate answer via Claude (compare against material)
   ├─ Show score (0-100) + explanation
   └─ Repeat for next question
   ↓
7. Final Report:
   ├─ Calculate average score
   ├─ Show breakdown by topic
   └─ Suggest areas for review
```

---

## Implementation Guide for Agent

### Phase 1: Table Selection

1. **Ask user for table name**: Present available options or ask directly.
   ```
   "Which knowledge table would you like to be tested on?
   
   (Available tables: [list if retrievable], or type the table name)"
   ```

2. **Validate table exists**:
   - Attempt to query the table for content
   - If table doesn't exist: ask user to provide correct name or check available tables
   - If table exists: proceed to phase 2

---

### Phase 2: Topic Extraction & Selection

1. **Query vault for topics**:
   - Use `knowledge-query` to ask the vault:
     ```
     "What are the main topics, chapters, or subject areas covered in this material? 
     List 5-7 key topics with brief descriptions."
     ```
   - Parse the response to extract topic names

2. **Present topics to user**:
   ```
   "Great! Here are the main topics I found in [Subject Name]:
   
   1. [Topic 1]
   2. [Topic 2]
   3. [Topic 3]
   ... (5-7 topics)
   
   Which topics would you like to be tested on?
   You can:
   - Type topic numbers separated by commas (e.g., '1,2,3')
   - Type topic names directly
   - Or say 'all' to cover all topics"
   ```

3. **Parse user selection**:
   - Accept comma-separated numbers: `1,3,5`
   - Accept topic names: `Basic Mechanics, Energy Conservation`
   - Accept 'all': use all extracted topics
   - Confirm selection back to user

---

### Phase 3: Question Configuration

1. **Ask for question count**:
   ```
   "How many questions would you like?
   
   (I'd suggest 5-10 for a quick check, or 15+ for a comprehensive exam)
   
   Enter a number:"
   ```

2. **Validate input**:
   - Accept integers between 1 and 50 (reasonable upper bound)
   - If invalid, ask again

3. **Confirm**:
   ```
   "Got it! I'll generate [N] questions on [selected topics].
   
   Let's begin. For each question, type your answer in chat. 
   I'll evaluate it immediately and show your score."
   ```

---

### Phase 4: Question Loop (Repeat for each question)

For question `i` of `total_questions`:

#### 4a. Generate Question

```python
# Prompt Claude to generate a question
prompt = f"""
Based on the following topics from a {subject} course material:
{selected_topics_text}

Generate a single exam question that:
- Is clear and focused on ONE of the selected topics
- Tests understanding, not just memorization
- Can be answered in 2-3 sentences
- Has a single, verifiable correct answer

IMPORTANT: If you find any actual tests, exams, or practice exercises in the material,
do NOT copy them exactly. Instead:
- Vary numerical values and parameters
- Use different naming conventions or examples
- Change the specific scenario or context
- Ensure the question tests the same concept but is distinctly different

Format your response as:
QUESTION: [the question text]
CORRECT_ANSWER: [brief expected answer]
"""
```

- Call Claude API with the prompt
- Extract: `QUESTION` and `CORRECT_ANSWER`
- Store `CORRECT_ANSWER` for later evaluation

#### 4b. Present Question

```
"Question {i}/{total_questions}:

{QUESTION}

(Type your answer below)"
```

#### 4c. Collect User Answer

- Wait for user to type their answer in chat
- Capture the full response

#### 4d. Evaluate Answer

1. **Query vault for relevant content**:
   ```
   knowledge-query: "What does the material say about [question_topic]? 
   Provide the most relevant passage or explanation."
   ```
   - Captures relevant material from vault

2. **Score the answer via Claude**:
   ```python
   prompt = f"""
   A student was asked: "{QUESTION}"
   
   The correct answer based on course material is:
   "{CORRECT_ANSWER}"
   
   The student answered:
   "{USER_ANSWER}"
   
   Relevant material from the course:
   "{VAULT_CONTENT}"
   
   Evaluate the student's answer:
   1. Is it correct? (yes/no)
   2. What is the score? (0-100, where 100 is perfect)
   3. Provide brief feedback (1-2 sentences explaining why)
   
   Format:
   CORRECT: [yes/no]
   SCORE: [0-100]
   FEEDBACK: [explanation]
   """
   ```
   - Call Claude API
   - Extract: `CORRECT`, `SCORE`, `FEEDBACK`
   - Store `SCORE` for final tally

3. **Show feedback to user**:
   ```
   "Answer: {USER_ANSWER}
   
   {FEEDBACK}
   
   Score: {SCORE}/100
   
   Running score: {CUMULATIVE_SCORE}/{i*100}"
   ```

---

### Phase 5: Final Report

After all questions are answered:

1. **Calculate results**:
   - Average score: `sum(all_scores) / total_questions`
   - Breakdown by topic (if tracking which question was on which topic)

2. **Present report**:
   ```
   "🎯 Exam Complete!
   
   Final Score: {AVERAGE}/100
   
   Breakdown by Topic:
   - Topic 1: {avg_score}
   - Topic 2: {avg_score}
   - ...
   
   Performance Summary:
   - 90-100: Excellent! You've mastered this material.
   - 80-89: Very good. Consider reviewing [weak topic] for full mastery.
   - 70-79: Decent understanding. Review [weak topics] more thoroughly.
   - 60-69: Passing, but there's room for improvement. Focus on [weak topics].
   - <60: Significant gaps. Review the material and retake the exam.
   
   Areas to focus on:
   [Topics with lowest average scores]
   "
   ```

---

## Key Implementation Details

### Table Selection
- User specifies the knowledge table name when invoking the skill
- Skill validates that the table exists before proceeding
- Skill assumes the table has already been created (via fenix-browser, knowledge-ingest, or other ingestion tools)
- Tables are managed by the user—skill does not create or delete them

### Question Variation (Important for Fair Testing)
- If actual tests, exams, or practice exercises are found in the knowledge vault:
  - **Vary numerical values**: Change numbers, percentages, quantities
  - **Change naming**: Use different names, variable names, entity names
  - **Alter context**: Change the scenario, real-world example, or application
  - **Test same concept**: Ensure the underlying concept/skill tested is identical
- This prevents students from simply memorizing specific examples from the material
- Ensures questions test conceptual understanding, not rote memorization

### Vault Querying for Answers
- Always query the vault for relevant material when evaluating answers
- This ensures scoring is grounded in the actual course content, not just Claude's general knowledge
- Improves fairness and accuracy

### Claude Prompts Required
1. **Topic extraction** — Extract 5-7 main topics from material
2. **Question generation** — Generate exam question on selected topic (with value/naming variation if needed)
3. **Answer evaluation** — Compare user answer against correct answer + material

### Error Handling
- If table doesn't exist: ask user to verify name or list available tables
- If vault query returns empty: warn user material may be incomplete
- If Claude calls fail: ask user to rephrase or try again
- If user input is invalid: provide clear guidance and ask again

---

## Notes

- **Pre-existing tables**: The skill requires a knowledge table to already exist (created via fenix-browser or other ingestion tools)
- **Fair question generation**: When questions resemble actual tests/exercises in the material, the skill varies values and naming to prevent exact copying
- **Vault-grounded evaluation**: All answer evaluation is grounded in the vault content, ensuring fairness and accuracy
- **Dynamic generation**: Questions are generated fresh each time based on the material, allowing multiple attempts without repetition
- **Chat-native**: All interaction happens conversationally in the OpenClaw chat interface
- **User-owned tables**: Tables persist between sessions; users manage table lifecycle independently
