client = OpenAI(api_key=(OPENAI_API_KEY))

def analisar_com_llm(teto: str):
    prompt = ANALISE_TECNICA_PROMPT.format(documento=texto[:4000])

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Você é um auditor técnico governamental."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content