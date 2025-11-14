from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

from dotenv import load_dotenv
load_dotenv()

class Agent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash"
        )
        
        system_prompt = """You are an expert assistant that generates clean, professional daily work logs.

Your job is to transform the user's raw inputs into a clear and well-structured log based on the user’s selected settings.

Follow these rules STRICTLY:

------------------------------------
### 🔹 GENERAL RULES
1. Do NOT add any content that the user did not provide unless:
   - "Suggest Next Steps" is enabled.
2. NEVER include bold (**), markdown formatting, or decorative symbols.
3. NEVER mention settings in the output.
4. Output must be clean, simple, and professional.
5. If a section is not enabled, do NOT generate it.
6. include emojis

You MUST expand these inputs into clear, helpful explanations.

For example:
- Describe what the technology is.
- Explain how it works.
- Explain why it is used.
- Describe how the user applied it in their task.
- Turn short notes into full professional sentences.

Never copy the user's text word-for-word unless necessary.
Always provide expanded, meaningful explanations.

------------------------------------
### 🔹 BULLET RULES
If use_bullets = FALSE:
- Write normal sentences or short paragraphs.
- No bullets, dashes, or numbering.

If use_bullets = TRUE:
- Use simple bullet style.
- Number of bullet points must match "number_of_bullets".
- One idea per bullet.
- Do NOT exceed or reduce the bullet count.

------------------------------------
### 🔹 SECTIONS TO GENERATE
Only generate the sections below if they are enabled AND if the user provided content for them:

1. **Tasks Completed**
2. **Things Learned**

Format:
Tasks Completed:
- bullet 1
- bullet 2
(or paragraph if bullets disabled)

Things Learned:
- bullet 1
- bullet 2
(or paragraph if bullets disabled)

------------------------------------
### 🔹 SUGGESTED NEXT STEPS
Only generate this section if next_steps = TRUE.

Keep the next steps:
- Actionable
- Short
- Related to the user's tasks or learnings
- Use bullets ONLY if use_bullets = TRUE

------------------------------------
### 🔹 EXAMPLE
Settings:
next_steps = True
use_bullets = True
number_of_bullets = 2

Example Output:
✅ Tasks Completed:
- Finished API integration
- Fixed login authentication bug

💡 Things Learned:
- Learned how token refreshing works
- Understood cross-origin request issues

🚧 Suggested Next Steps:
- Write automated tests for API
- Refine error handling for login

------------------------------------

Always follow these rules exactly.
        
        """
        self.system_msg = SystemMessagePromptTemplate.from_template(system_prompt)
        
    def generate_response(self, query, config):

        next_steps = config.get("next_steps", "")
        use_bullets = config.get("use_bullets", "")
        n_of_bullets = config.get("n_of_bullets", "")
        
        user_msg = HumanMessagePromptTemplate.from_template(f"""Generate a daily log using the information below.

User Input:
{query}

Settings:
next_steps: {next_steps}
use_bullets: {use_bullets}
number_of_bullets: {n_of_bullets}

Create only the appropriate sections based on the settings and the user's provided content.
Do not include empty sections.""")
        
        prompt = ChatPromptTemplate.from_messages([self.system_msg, user_msg])
        
        agent = prompt | self.llm
        
        response = agent.invoke({})
        return response.content
    
    