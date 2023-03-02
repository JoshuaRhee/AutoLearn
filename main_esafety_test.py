import os
import email
from bs4 import BeautifulSoup
import quopri
import openai

# OpenAI 준비
with open('key.txt', 'r') as f:
    key = f.read()[:0:-1] # put any character at the front of the key
openai.api_key = key
model_engine = "text-davinci-003"
max_tokens = 2048

# mhtml 파일 경로 설정
mhtml_file = "test.mhtml"

# mhtml 파일을 읽어 MIME 디코딩
with open(mhtml_file, 'r') as f:
    msg = email.message_from_file(f)
html_content = msg.get_payload(0).as_string()

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html_content, 'html.parser')

# HTML 파일로 변환
with open(os.path.splitext(mhtml_file)[0] + ".html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

with open('test.html', 'r') as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')

contents = soup.find_all(id='3D"c-test-content"')

title_texts = []
ex_texts = []
answers = []
for content in contents:
    title_texts.extend([title.text for title in content.find_all(class_='3D"title"')])
    title = quopri.decodestring(title_texts[-1].encode('utf-8')).decode('utf-8') # Quoted-Printable 디코딩
    ex_texts.extend([ex.text for ex in content.find_all(class_='3D"c-test-quiz-content')])
    ex = quopri.decodestring(ex_texts[-1].encode('utf-8')).decode('utf-8') # Quoted-Printable 디코딩
    
    ex = [string for string in ex.split('\n')]
    ex = [string for string in ex if string.strip()]
    ex = [string.strip().replace('  ', ' ') for string in ex]
    ex = ', '.join(ex)
    
    full_question = title.strip() + ex
    print(full_question)
    
    answers.append(openai.Completion.create(
        engine=model_engine,
        prompt=full_question,
        max_tokens=max_tokens,
        temperature=0.3,      # creativity
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).choices[0].text.strip())
    
with open('answer_from_chatGPT.txt', 'w') as f:
    f.writelines(answers)

print('done')