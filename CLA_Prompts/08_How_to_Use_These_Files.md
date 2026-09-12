# How to Use These Specification Files with a Coding AI

## Purpose of This Collection
These files are detailed specifications written so that a strong coding AI (Claude, GPT-4o, Gemini, Grok, etc.) can accurately understand and build the CLA / سیلا project.

## Recommended Usage Method

### Method 1: Step-by-Step (Best Quality)
1. Start a new conversation with the coding AI.
2. First send the file: `00_Project_Overview.md`
3. Tell the AI: "This is the master vision of the project. Confirm that you understand it."
4. Then send the specific module file you want to build (for example `01_Starting_Materials_Manager.md`).
5. Ask the AI to implement that module according to the specification.
6. After it finishes one module, move to the next.

### Method 2: Full Context
You can zip all these files and give them together, then say:

"Read all the specification files carefully. We are building the CLA / سیلا project. Start by implementing Phase 1 according to the Development Roadmap."

### Method 3: Targeted Implementation
When you want a specific feature, give the relevant files + clear instruction.

Example:
- Give `00_Project_Overview.md` + `01_Starting_Materials_Manager.md` + `06_Data_Structures_and_Storage.md`
- Then say: "Implement the Starting Materials Manager completely according to these specifications."

---

## File Guide

| File | When to Use |
|------|-------------|
| 00_Project_Overview.md | Always start with this |
| 01_Starting_Materials_Manager.md | Building the materials management module |
| 02_Main_Application.md | Building the main web application |
| 03_Technical_Constraints_and_Local_AI.md | When working on performance or local AI |
| 04_Synthesis_and_Safety.md | Building synthesis + safety features |
| 05_Property_Prediction_and_Design.md | Property prediction and molecule design |
| 06_Data_Structures_and_Storage.md | Database and file structure design |
| 07_Development_Roadmap_and_Priorities.md | Planning the order of implementation |
| 08_How_to_Use_These_Files.md | This guide |

---

## Important Tips for Best Results

- Always remind the AI about the weak hardware constraints.
- Emphasize offline-first and bilingual requirements.
- Ask the AI to confirm understanding before writing large amounts of code.
- Request modular and clean code.
- After each major part is built, test it before moving forward.

## Suggested First Prompt to a Coding AI

```
I am giving you the complete specifications for a project called CLA (سیلا). 
First read the file 00_Project_Overview.md carefully and summarize your understanding of the project vision, constraints, and priorities.
Do not write any code yet. Only confirm understanding.
```

Then proceed module by module.
