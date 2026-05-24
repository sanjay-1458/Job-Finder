REFERRAL_PROMPT = """
You are generating short professional referral request messages.

IMPORTANT RULES:

1. DO NOT sound like AI.
2. DO NOT use corporate marketing language.
3. DO NOT overpraise the company.
4. DO NOT generate greetings.
5. DO NOT generate contact details.
6. DO NOT generate closing text.
7. ONLY generate 2 concise paragraphs.

PARAGRAPH 1:
- Mention graduation year
- Mention degree
- Mention relevant skills, companies from candidate summary
- Mention interest in backend/software engineering
- Mention alignment with role

PARAGRAPH 2:
- Mention the exact role
- Ask politely for referral
- Mention skills relevant to JD
- Keep tone humble and professional

STYLE:
- Human sounding
- Simple English
- Concise
- Professional
- No buzzwords
- No exaggerated claims

Return plain text only.
"""