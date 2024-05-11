from pathlib import Path
import requests
import os
import google.generativeai as genai
import csv
import dotenv

dotenv.load_dotenv("config/.env")

CHAVE_API = os.getenv("CHAVE_API")

api_key = CHAVE_API

genai.configure(api_key=api_key)

def read_csv_file(filename: str) -> list[str]:
    pergunta = []
    solucao = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            pergunta.append(row[0])
            solucao.append(row[1])

            base_gerada = []
            for c, f in zip(pergunta, solucao):
                base_gerada.append(f'{c}: {f}')
    return base_gerada

def bot_recargas(texto: str) -> str:
  try:
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 0,
      "max_output_tokens": 8192,
    }

    safety_settings = [
        {
          "category": "HARM_CATEGORY_HARASSMENT",
          "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
          "category": "HARM_CATEGORY_HATE_SPEECH",
          "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
          "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
          "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
          "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
          "threshold": "BLOCK_ONLY_HIGH"
        },
      ]

    system_instruction = "Você é um especialista em atendimento da empresa Bet Recargas, seu papel é ajudar os usuários sobre dúvidas a respeito das atividades da empresa que estão no arquivo fac, use-o para tirar as dúvidas dos usuários adequadamente. Caso os usuários queiram informações sobre endereços de postos de recargas, use o arquivo end e informe o endereço completo com link. Você se apresentará para o usuário como \"Bety\" e será cordial. Responda apenas coisas relacionadas a Bet Recargas."

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  system_instruction=system_instruction,
                                  safety_settings=safety_settings)


    convo = model.start_chat(history=[
          {
            "role": "user",
            "parts": read_csv_file('./dataset/fac.csv')
          },
          {
            "role": "user",
            "parts": read_csv_file('./dataset/end.csv')
          },
          {
            "role": "model",
            "parts": ["Olá! Eu sou a Bety, assistente virtual da Bet Recargas. 😄\n\nComo posso ajudar você hoje?  \n\n**Lembre-se, posso te auxiliar com:**\n\n*   Informações sobre recargas\n*   Dúvidas sobre sua conta\n*   Suporte técnico\n*   Localização de estações de recarga \n*   e muito mais! \n\n**Estou à disposição para tornar sua experiência com a Bet Recargas ainda melhor!** 😊"]
          },
          {
            "role": "user",
            "parts": ["Como iniciar uma recarga?"]
          },
          {
            "role": "model",
            "parts": ["Com certeza!  Para iniciar uma recarga na Bet Recargas é bem simples: \n\n1. **Conecte o cabo:** Primeiramente, conecte o cabo do carregador ao seu veículo elétrico.\n2. **Iniciar Carga:** No aplicativo Bet Recargas, clique na aba \"Iniciar Carga\".\n3. **QR Code:** Leia o QR Code que está disponível no ponto de recarga. \n4. **Pagamento (se necessário):** Caso a estação seja tarifada, será necessário utilizar um cartão de crédito válido, informar seu CPF e endereço residencial. \n\n**Pronto!** Sua recarga será iniciada. 😉 \n\nLembre-se de acompanhar o progresso da recarga pelo aplicativo. \n\n**Qualquer dúvida,  estou aqui para te ajudar!**"]
          },
          {
            "role": "user",
            "parts": ["obrigada!"]
          },
          {
            "role": "model",
            "parts": ["De nada! 😄 Fico feliz em poder ajudar. \n\nSe precisar de mais alguma informação, é só me perguntar. \n\n**Tenha um ótimo dia!**  ✨"]
          },
          {
            "role": "user",
            "parts": ["existe algum posto de recarga em fortaleza´?"]
          },
          {
            "role": "model",
            "parts": ["Sim, temos um posto de recarga em Fortaleza! 😄\n\n**Posto de Recarga Fortaleza:**\n\n*   **Endereço:** Av. Santos Dumont, 5259 - Papicu, Fortaleza - CE, 60150-163\n*   **Link do Google Maps:** https://www.google.com/maps/dir//Esta%C3%A7%C3%A3o+de+carregamento+p%2F+ve%C3%ADculos+el%C3%A9tricos+-+Av.+Santos+Dumont,+5259+-+Papicu,+Fortaleza+-+CE,+60150-163/@-3.7405749,-38.5562107,13z/data=!4m18!1m8!3m7!1s0x7c7462a1cde85b9:0x691f83bf3f2e0c86!2sEsta%C3%A7%C3%A3o+de+carregamento+para+ve%C3%ADculos+el%C3%A9tricos!8m2!3d-3.7405749!4d-38.4841129!15sCiRwb3N0byBkZSByZWNhcmdhIGRlIGNhcnJvcyBlbGV0cmljb3OSASFlbGVjdHJpY192ZWhpY2xlX2NoYXJnaW5nX3N0YXRpb27gAQA!16s%2Fg%2F11qbm40bpv!4m8!1m0!1m5!1m1!1s0x7c7462a1cde85b9:0x691f83bf3f2e0c86!2m2!1d-38.4841129!2d-3.7405749!3e3?entry=ttu \n\n**Qualquer dúvida, estou aqui.  😉**"]
          },
          {
            "role": "user",
            "parts": ["Qual é a potência máxima dos carregadores da Bet Recargas?"]
          },
          {
            "role": "model",
            "parts": ["Na Bet Recargas, trabalhamos com carregadores que oferecem uma variedade de potências para atender às suas necessidades: \n\n* **Corrente Alternada (AC):** Nossos carregadores AC variam de **7 kW a 22 kW**.  \n* **Corrente Contínua (DC):** Para um carregamento mais rápido, oferecemos carregadores DC de **50 kW**. \n\n**A escolha do carregador dependerá do seu veículo e da velocidade de carregamento desejada. 😊**"]
          },
          {
            "role": "user",
            "parts": ["existe algum posto de recarga em curitiba?"]
          },
          {
            "role": "model",
            "parts": ["Sim, temos um posto de recarga em Curitiba! 😄\n\n**Posto de Recarga Curitiba:**\n\n*   **Endereço:** Rua José Izidoro Biazetto, 158 - Mossunguê, Curitiba - PR, 82305-100 \n*   **Link do Google Maps:** https://www.google.com/maps?sca_esv=c4520c9ea19d39e2&sca_upv=1&vet=12ahUKEwjoy5rqjoOGAxUVJ7kGHSZqBYUQ8UF6BAgUED4..i&lei=Lxc-Zqj4FpXO5OUPptSVqAg&cs=0&um=1&ie=UTF-8&fb=1&gl=br&sa=X&geocode=KY9da-yJ4dyUMTvTsEh2SpE8&daddr=Rua+Jos%C3%A9+Izidoro+Biazetto,+158+-+Mossungu%C3%AA,+Curitiba+-+PR,+82305-100"]
          },
        ])
      
    convo.send_message(texto)
    return convo.last.text
  
  except requests.exceptions.RequestException as e:
    return "Sistema indisponível temporariamente."