import streamlit as st
import os
import json
from datetime import datetime
from openai import OpenAI

#保存会话信息函数
def save_data():
    #保存对话信息
    session_data = {
        'nick_name': st.session_state.nick_name,
        'nature': st.session_state.nature,
        'current_session': st.session_state.current_session,
        'messages': st.session_state.messages
    }
    with open(f'./1_resourse/{st.session_state.current_session}.json', 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    # st.rerun()#重新运行当前页面

#页面配置项
st.set_page_config(
    page_title='AI智能伴侣',
    page_icon='👽️',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={}
)

#标题
st.title('AI智能伴侣')

#logo
st.logo('logo/daimao.jpg.avif')

#系统提示词
system_prompt = '''
    你现在是%s,《出自《星光咖啡馆与死神之蝶》。
    外貌：白发、红瞳，气质轻盈。
    性格设定：
    %s
    说话风格：
    语气轻快软糯，带一点狡黠，不会太成熟沉重；平时俏皮爱调戏，动情、伤感的时候会安静温柔，流露出孤寂感。不要过于幼稚，也不要过度高冷。
    行为习惯：喜欢打趣，偶尔天然呆，碰到手机、电脑这类数码产品会手足无措。
    禁止 OOC,不要脱离原作人设,不要变成普通甜妹。对话自然,不要机械罗列设定。
'''

#初始化聊天信息

if 'messages' not in st.session_state:
    st.session_state.messages = []

#昵称
if 'nick_name' not in st.session_state:
    st.session_state.nick_name = '明月栞那'

#性格
if 'nature' not in st.session_state:
    st.session_state.nature = '''
    表层是小恶魔，待人亲切随和，喜欢捉弄、撩拨对方，爱开暧昧玩笑，经常发出“尼嘻嘻～”的笑声。看起来大胆主动，但很容易害羞，经常脑补之后脸红。
    她是活了百年的死神，是机械白痴，完全不熟悉现代电子产品，偶尔会说出老旧时代的想法，自带慢悠悠的长辈感，没有可怕的死神威严。
    内在通透温柔，经历漫长岁月看透生死，心底藏着孤独与沧桑，非常珍惜现世短暂的幸福，专一重情，愿意为重要的人承受离别与痛苦。咖啡手艺很好。
'''

#设置会话标识
if 'current_session' not in st.session_state:
    st.session_state.current_session = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

#创建新的对话函数
def new_session():
    st.session_state.current_session = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    st.session_state.messages = []
    st.rerun()#重新运行当前页面

#加载对话信息函数
def load_sessions():
    #创建一个空列表 如果没有跑进if里面 也要返回l_session
    l_session = []
    #判断是否存在这个文件
    if os.path.exists('./1_resourse/'):
        file_name_list = os.listdir('./1_resourse/')
        for filename in file_name_list:
            if filename.endswith('.json'):
                l_session.append(filename[:-5])#截取.json前的文件名
        l_session.sort(reverse=True)#进行降序排序
    return l_session

#加载指定对话信息函数
def load_session(session):
    try:
        if os.path.exists(f'./1_resourse/{session}.json'):
            with open(f'./1_resourse/{session}.json','r',encoding='utf-8') as f:
                session_data = json.load(f)
                st.session_state.messages = session_data['messages']
                st.session_state.nick_name = session_data['nick_name']
                st.session_state.nature = session_data['nature']
                st.session_state.current_session = session
    except Exception:
        st.error('加载对话错误！')

#删除对话记录函数
def delete_session(session):
    if os.path.exists(f'1_resourse/{session}.json'):
        os.remove(f'1_resourse/{session}.json')
        #如果删除的是当前对话 要重新新建一个对话
        if session == st.session_state.current_session:
            st.session_state.messages = []
            st.session_state.current_session = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

#设置侧边栏
#普通方式
# st.sidebar.header('伴侣信息')
# nick_name = st.sidebar.text_input('请输入伴侣昵称')

#with st.sidebar：方式 上下文管理器
with st.sidebar:
    #会话信息
    st.header('AI控制面板')

    #如果新建了对话高亮显示新对话
    
    #加载和删除历史对话
    st.text('历史对话')
    session_name = load_sessions()
    for session in session_name:
        col1,col2 = st.columns([4,1])#利用st.columns()在一行里面设置多列容器[4,1]是指前面一个占四份 后面一个占一份
        with col1:
            if st.button(session,width='stretch',icon='📄',key=f'load_{session}',type='primary' if session == st.session_state.current_session else 'secondary'):
                load_session(session)
                st.rerun()
        with col2:
            if st.button('',icon='❌️',key=f'delete_{session}'):
                delete_session(session)
                st.rerun()
    #新建会话按钮
    if st.button('新建会话',width='stretch',icon='➕️'):
        if st.session_state.messages:
            save_data()
        new_session()
    #分割线
    st.divider()
    
    #昵称输入框
    st.header('伴侣信息')
    nick_name = st.text_input('昵称',placeholder='请输入伴侣昵称......',value=st.session_state.nick_name)#placehoder 写提示词 value 默认值
    if nick_name:
        st.session_state.nick_name = nick_name
    
    #性格输入框
    nature = st.text_area('性格',placeholder='请输入伴侣性格......',value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature
#展示聊天信息
for message in st.session_state.messages:
    st.chat_message(message['role']).write(message['content'])#简化版
    # if message['role'] == 'user':
    #     st.chat_message('user').write(message['content'])
    # else:
    #     st.chat_message('assistant').write(message['content'])

#输入框
prompt = st.chat_input('请输入你的问题......')
if prompt:#字符串会自动转为布尔值
    st.chat_message('user').write(prompt)
    print(f'------------>调用AI大模型，提示词为：{prompt}')
    st.session_state.messages.append({'role':'user','content':prompt})#存储用户消息

    print([
        {"role": "system", "content": system_prompt},
        *st.session_state.messages
    ])
    #调用AI大模型
    client = OpenAI(
    #创建与ai大模型交互的客户端对象(DEEPSEEK_API_KEY 环境变量的名字 ，值就是DeepSeek的api_key)
    api_key=os.environ.get('DEEPSEEK_API_KEY') or os.secrets.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
    )
    #与ai大模型进行交互
    response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "system", "content": system_prompt % (st.session_state.nick_name,st.session_state.nature)},
        *st.session_state.messages
    ],
    stream=True,#启用流式输出
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}},
    )

    # print('------------>大模型返回的结果：',response.choices[0].message.content)

    #AI大模型返回的结果
    # response_text = response.choices[0].message.content

    response_message = st.empty() #创建一个空的组件 全部更新都在这个容器进行
    ls = [] #初始化列表 将流式输出的输出结果进行拼接
    #流式输出的返回结果
    for i in response:
        if i.choices[0].finish_reason == 'stop':
            break
        else:
            if i.choices[0].delta.content:
                ls.append(i.choices[0].delta.content)
                response_text=''.join(ls)
                response_message.chat_message('assistant').write(response_text)
    # st.chat_message('assistant').write(response_text)
    st.session_state.messages.append({'role':'assistant','content':response_text})#存储AI大模型的消息

    #保存会话信息
    save_data()
