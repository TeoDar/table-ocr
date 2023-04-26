from App import HOST, PORT
import requests
import streamlit as st
from streamlit_option_menu import option_menu
import webbrowser

SERVER_URL = f'http://{HOST}:{PORT}'

if 'npage' not in st.session_state:
    st.session_state['npage'] = 0


class WebPage:
    '''
    Класс реализующий основное окно приложения
    '''

    def __init__(self) -> None:
        # Задание общих параметров сайта
        st.set_page_config(page_title='Распознавание таблиц', page_icon='📰', layout='wide', )
        # Добавление бокового меню
        with st.sidebar:
            self.draw_side_bar()
        if self.selected in 'Шаблоны':
            st.title("Создание шаблона распознавания")
            uploaded_file = None
            with st.sidebar:
                st.header('Загрузите скан:')
                uploaded_file = st.file_uploader('Только для типов [PDF] и [PNG]', type=('pdf', 'png'))
            if uploaded_file:
                self.session = requests.Session()
                self.upload(uploaded_file)
        if self.selected in 'Справка':
            webbrowser.open_new_tab('http://127.0.0.1:8000/docs')
        if self.selected in 'Связаться с разработчиком':
            webbrowser.open_new_tab('https://t.me/TeoDar')
        if self.selected in 'test':
            self.test()

    def draw_side_bar(self):
        self.selected = option_menu(
            menu_title="TABLE-OCR",
            options=["Шаблоны", "Распознавание", "Справка", "Связаться с разработчиком", "test"],
            default_index=0,
            menu_icon="table",
            icons=['border', 'eye', 'book', 'person lines fill'],
            styles={
                "container": {"background-color": "rgb(14, 17, 23)"},
                # "icon": {"color": "#ffb4b4", "font-size": "25px"},
                "nav-item": {"padding": "2px"},
                "nav-link": {"margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "gray"},
            })

    def upload(self, uploaded_file):
        file = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        with st.spinner('Загрузка файла и извлечение изображений'):
            try:
                response = self.session.post(f"{SERVER_URL}/upload_file", files=file)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                st.write(err.response.status_code, ':', err.response.json()['detail'])
                st.stop()
        col1, col2 = st.columns(2)
        file_hash: str = response.json()["file_hash"]
        extracted_images_hashes: list = response.json()["extracted_images_hashes"]
        st.write(extracted_images_hashes)
        image_button = None

        for id, img_hash in enumerate(extracted_images_hashes):
            image_link = f"{SERVER_URL}/get_image/{file_hash}/{img_hash}"
            with st.sidebar:
                with open('./App/FrontEnd/html/button.html', encoding='utf-8') as f:
                    with col1:
                        button_html = f.read().replace('src=""', f'src="{image_link}"')
                        st.markdown(button_html, unsafe_allow_html=True,)
                    with col2:
                        st.button(f'{id} страница', on_click=lambda x: self.change_image(npage=id))


    def change_image(self, npage):
        st.session_state.npage = npage
        
        st.markdown(image_style, unsafe_allow_html=True)


    def test(self):
        test_file = st.file_uploader('Только для типов [PDF] и [PNG]', type=('pdf', 'png'))
        if test_file:
            try:
                file = {"file": (test_file.name, test_file.getvalue())}
                response = self.session.post(f"{SERVER_URL}/faultreport", files=file)
                response.raise_for_status()
                st.write(response.json())
            except requests.exceptions.HTTPError as err:
                st.write(err.response.status_code, ':', err.response.json()['detail'])
        with open('./App/FrontEnd/html/test.html', encoding='utf-8') as f:
            f = f.read().replace('url()', f'url(file://localhost/C:/PROJECTS/table_ocr/App/Test/9f826a2450c8e77f6bc5a7e51fdd8c02.png)')
            st.markdown(f, unsafe_allow_html=True,)


if __name__ == "__main__":
    WebPage()
