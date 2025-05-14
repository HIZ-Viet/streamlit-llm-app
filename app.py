import streamlit as st
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

# 環境変数をロード
load_dotenv()

# Streamlitアプリの設定
st.title("LLMを使った専門家質問アプリ")
st.write("""
このアプリでは、以下の5つの専門家に質問できます：
1. **physical properties**: 金属元素の物理的・化学的性質について
2. **reaction**: 金属元素の化学反応について
3. **material**: E-スクラップや電子デバイス部品の材質について
4. **law**: 輸出入や環境法に関する法律について
5. **market**: ベトナムにおける市場動向について
""")

# LangChainの設定
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

# 各専門家のプロンプトテンプレート
prompt_infos = [
    {
        "name": "physical properties",
        "description": "金属元素の物理的・化学的性質についての専門家です",
        "prompt_template": """
        あなたは金属元素の物理的・化学的性質についての専門家です。
        質問：{input}
        """
    },
    {
        "name": "reaction",
        "description": "金属元素の酸化、還元、錯体形成などの化学反応についての専門家です",
        "prompt_template": """
        あなたは金属元素の酸化、還元、錯体形成などの化学反応についての専門家です。
        質問：{input}
        """
    },
    {
        "name": "material",
        "description": "E-スクラップや電子デバイス部品の材質についての専門家です",
        "prompt_template": """
        あなたはE-スクラップや電子デバイス部品の材質についての専門家です。
        質問：{input}
        """
    },
    {
        "name": "law",
        "description": "輸出入や環境法に関する法律についての専門家です",
        "prompt_template": """
        あなたはE-スクラップや電子デバイス部品の輸出入に関する法律や環境法についての専門家です。
        質問：{input}
        """
    },
    {
        "name": "market",
        "description": "E-スクラップや電子デバイス部品の市場動向についての専門家です",
        "prompt_template": """
        あなたはE-スクラップや電子デバイス部品の市場動向についての専門家です。
        質問：{input}
        """
    },
]

# 入力フォームとラジオボタン
user_input = st.text_input("質問を入力してください:")
selected_expert = st.radio(
    "質問する専門家を選択してください:",
    [info["name"] for info in prompt_infos]
)

# 質問を処理する関数
def get_expert_response(input_text, expert_name):
    # 選択された専門家のプロンプトを取得
    expert_info = next(info for info in prompt_infos if info["name"] == expert_name)
    prompt_template = PromptTemplate(template=expert_info["prompt_template"], input_variables=["input"])
    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.run({"input": input_text})

# ボタンが押されたときの処理
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("回答を生成中..."):
            response = get_expert_response(user_input, selected_expert)
            st.success("回答:")
            st.write(response)