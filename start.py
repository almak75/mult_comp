

import streamlit as st
import random

import time
import pandas as pd
import os
import pickle
import datetime
import extra_streamlit_components as stx
st.set_page_config(page_title='Таблица умножения')


try:
 import cv2
 print('Поставилось')
#except:
    #print('не поставилось')
except Exception:
    traceback.print_exc()


RATING_FILE = 'comp.txt'    #здесь будем хранить данные с рейтингом
RATING_N = 30                #КОЛИЧЕСТВО ПРИМЕРОВ В РЕЙТИНОГОВОМ ТЕСТЕ
COOKI_NAME = 'pupil'
LOG_COMP = 'log_comp.txt'   #лог для ведения статистики по соревнованиям
LOG_TRAIN = 'log_train.txt'   #лог для ведения статистики по обучению
ALL_MISTAKES = 'all_mistakes.txt'  #здесь будем хранить все ошибки
NOT_SAVE_RESULTS = ['Тестовый Тест', 'Выберите..', 'Гость'] #эти результаты не надо сохранять в рейтинги

#@st.cache_data
def transliterate(name):
    slovar = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ya', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'YO',
      'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
      'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
      'Ц':'C','Ч':'CH','Ш':'SH','Щ':'SCH','Ъ':'','Ы':'y','Ь':'','Э':'E',
      'Ю':'U','Я':'YA',',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
      '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
      ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
      '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '—':''}
        
    name = ''.join([slovar.get(ch,'') for ch in name])
    return name




#@st.cache_data
def load_class():
    with open('2b.txt', 'r',encoding='utf8') as f:
        pupils = f.readlines()#список учеников
    pupils=[p.replace('\n','') for p in pupils]
    tmp = ['Выберите..']
    tmp.extend(pupils)
    return tmp

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#cls()
#print('НОВАЯ СЕССИЯ 6')
#тут у них какой то косяк, кэш не работает. Пришлось лепить костыль, чтобы за именем обращался в кэш только один раз за сессию
#@st.cache(allow_output_mutation=True)
#@st.cache_resource
def get_manager():
    return stx.CookieManager()

if 'current_user' not in st.session_state:
    cookie_manager = get_manager()
    remember_fio = cookie_manager.get(cookie = COOKI_NAME)
    if remember_fio:
        st.session_state.current_user = remember_fio
        #print('Вспоминаем на старте', remember_fio)


def set_cookies(key): #записываем в куки текущего юзера
    #print(key)
    #key = key[0]
    #cookie_manager = get_manager()
    cookie_manager = get_manager()
    #print(st.session_state[key])
    st.session_state.current_user = st.session_state[key]
    cookie_manager.set(COOKI_NAME, st.session_state[key], expires_at=datetime.datetime(year=2023, month=7, day=7))
    
if ('current_user' not in st.session_state) or (st.session_state.current_user=='Выберите..'): #
    pos = 0
    pupils = load_class()
    #print(st.session_state)
    st.header('Таблица умножения. Чемпионат 2В.')
    pupil2 = st.selectbox(':blue[Участник:]', pupils, index = pos, on_change=set_cookies, args =['pupil2'], key='pupil2')
    st.write('Вам только посмотреть? Выберите пользователя с именем "Гость"')
    st.stop()





def show_buttons():
    col1, col2, col3,col4 = st.columns(4)
    with col1:
        start = st.button('Обучение', on_click=start_test, args=current_parameters, type='secondary')
    with col2:
        if pupil != 'Выберите..':
            start_rating = st.button('Соревнование', on_click=comp_test, args=current_parameters, type='secondary')
    with col3:
        pass #планируется тест по супер сложным примерам всего класса
    with col4:
        pass #просто для выравнивания кнопок


 #Выведем тип теста, если это соревование
if 'stat' in st.session_state and st.session_state.stat['type'] == 'comp':
     st.header('Таблица умножения. Соревнование.')
elif 'stat' in st.session_state and st.session_state.stat['type'] == 'train':
    st.header('Таблица умножения. Обучение.')
else:
    st.header('Таблица умножения. Чемпионат 2В.')

##MainMenu {visibility: hidden;}
#footer {visibility: hidden;}
m = st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
div.stButton > button:first-child {
    background-color: #0099ff;
    color:#ffffff;
    height: 48px;
    font-size: 32px;
}
div.stButton > button:hover {
    background-color: #00ff00;
    color:#ff0000;
    height: 48px;
    font-size: 32px;
    }

</style>""", unsafe_allow_html=True)





def miltiplication(a,b):
    return f'{a} x {b}', a*b
def division(a,b):
    return f'{a*b} : {b}', a

def mistake_test():
   
    if not 'big_stat' in st.session_state:
        return
    df = st.session_state.big_stat
    mist = df['Ошибки'].to_list()
    mist = [tmp for tmp in mist if tmp]
    mist = ','.join(mist)
        
    mist = mist.split(',')
    ##бежим по ошибкам
    #print('mist', mist)
    new_zd = []
    for m in mist:
        if not m:
            continue
        if 'x' in m:
            func = miltiplication
        elif ':' in m:
            func = division
        m = m.replace('x','')
        m = m.replace(':','')
        m = m.replace('=','')
        
        m = m.strip()
        dig = m.split()
        #print('m',m)
        #print('dig', dig)
        if func == miltiplication:
            a = int(dig[0]) #берем первое число
            b = int(dig[1]) #берем второе число
        else: #ДЕЛЕНИЕ! беерем 2 и третье
            a = int(dig[1]) #берем второе число
            b = int(dig[0])//a #берем деление!!!!

        if mutirovat: #переставляем числа местами
            a,b = b,a 

        new_zd.append((a,b,func))
    if len(new_zd)==0:
        
        return
    random.shuffle(new_zd)  #всё перемешаем, чтоб 
    #print(new_zd)
    new_zd = list(set(new_zd))  #это чтобы убрать все дубли. Могли ошибаться на одном примере много раз, но пихать его много раз ненадо в тест
    st.session_state.zadacha = new_zd

    #t.session_state.mist = new_zd
    #return

    s = time.ctime()
    start_time = s.split()[3]
    start_time_cek =time.time()
    numbers=['тест по ошибкам']
    stat={'good':0, 'wrong':0, 'voprosov':len(new_zd), 'start_time':start_time,'start_time_cek':start_time_cek, 'mistakes':[], 'numbers':numbers, 'деление':'', 'умножение':'', 'wrong_answer':[],'type':'train'} #тип - тест по ошибкам
    st.session_state.stat = stat

    st.session_state.answer='' #тут хранится ответ на тест
    st.session_state.q = '' #тут хранится вопрос и ПРАВИЛЬНЫЙ ответ теста
    ##st.session_state.last=0
    


def start_test(*current_parameters):

    st.session_state.answer='' #тут хранится ответ на тест
    st.session_state.q = '' #тут хранится вопрос и ПРАВИЛЬНЫЙ ответ теста
    ##st.session_state.last=0
    #сохраняем параметры текущего теста
    st.session_state.param = current_parameters
        
        
    #генерируем тут сразу новое задание с нужным количеством примеров
    l = [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10]
    numbers = [i+1 for i in range(len(l)) if l[i]]
    n = []
   

    start =[1,2][del1]
    finish=[11,10][del10]
    long = finish - start + 1
    for i in numbers:
        n.extend(list(zip(range(start,finish), [i]*long)))
    n=[(min(i), max(i)) for i in n]
    n = list(set(n))

    zd = n * (N//len(n))
    zd.extend(random.sample(n, N % len(n)))

    #генерируем операции
    oper = []
    if mult:
        oper.append(miltiplication)
    if div:
        oper.append(division)
    oper = oper * N
    oper = oper[:N]

    #соединяем цифры с операциями
    new_zd = []
    for i in range(N):
        tmp= list(zd[i])
        random.shuffle(tmp)
        tmp.append(oper[i])
        new_zd.append(tmp)

    random.shuffle(new_zd)
    st.session_state.zadacha = new_zd




    #ГОТОВИМ ДАННЫЕ В СТАТИСТИКУ
    s = time.ctime()
    start_time = s.split()[3]
    start_time_cek =time.time()
    numbers=['x'+str(n) for n in numbers]
    stat={'good':0, 'wrong':0, 'voprosov':N, 'start_time':start_time,'start_time_cek':start_time_cek, 'mistakes':[], 'numbers':numbers, 'деление':div, 'умножение':mult, 'wrong_answer':[],'type':'train'} #тип - обычный тест
    st.session_state.stat = stat

    #сюда будем складывать не правильно отвеченные примеры. Возможно, что их придется добавить в конце на штрафной круг
    st.session_state.crug=[]
    st.session_state.shot =''

def comp_test(*current_parameters): #ЭТО ТЕСТ, КОТОРЫЙ ГЕНЕРИРУЕТСЯ ДЛЯ СОРЕВНОВАНИЙ И ПОДСЧЕТА РЕЙТИНГА
    #print('готовим соревноват.тест для ', pupil)

    st.session_state.answer='' #тут хранится ответ на тест
    st.session_state.q = '' #тут хранится вопрос и ПРАВИЛЬНЫЙ ответ теста
    ##st.session_state.last=0
    #сохраняем параметры текущего теста
    st.session_state.param = current_parameters
        
        
    #генерируем тут сразу новое задание с нужным количеством примеров
    l = [False,False,False,True,True,True,True,True,True,False]
    numbers = [i+1 for i in range(len(l)) if l[i]]
    n = []
   

    start = 2 #исключаем умн на 1
    finish= 10 #искл умн на 10
    long = finish - start + 1
    for i in numbers:
        n.extend(list(zip(range(start,finish), [i]*long)))
    n=[(min(i), max(i)) for i in n]
    n = list(set(n))

    N = RATING_N #
    zd = n * (N//len(n))
    zd.extend(random.sample(n, N % len(n)))

    #генерируем операции. Искользовать будем и умножение и деление
    oper = []
    oper.append(miltiplication)
    oper.append(division)
    oper = oper * N
    oper = oper[:N]

    #соединяем цифры с операциями
    new_zd = []
    for i in range(N):
        tmp= list(zd[i])
        random.shuffle(tmp)
        tmp.append(oper[i])
        new_zd.append(tmp)

    random.shuffle(new_zd)
    st.session_state.zadacha = new_zd




    #ГОТОВИМ ДАННЫЕ В СТАТИСТИКУ
    s = time.ctime()
    start_time = s.split()[3]
    start_time_cek =time.time()
    numbers=['x'+str(n) for n in numbers]
    stat={'good':0, 'wrong':0, 'voprosov':N, 'start_time':start_time,'start_time_cek':start_time_cek, 'mistakes':[], 'numbers':numbers, 'деление':div, 'умножение':mult, 'wrong_answer':[], 'type':'comp'} #тип - соревнование
    st.session_state.stat = stat

    #сюда будем складывать не правильно отвеченные примеры. Возможно, что их придется добавить в конце на штрафной круг
    st.session_state.crug=[]
    st.session_state.shot =''

    #print('Соревновательный тест подготовлен', pupil)
    return



with st.expander("НАСТРОЙКИ ОБУЧЕНИЯ"):
    st.text('При изменении настроек теста, текущий тест будет прерван.')
    pos = 0
    pupils = load_class()
    #print(st.session_state)
    if (not 'pupil' in st.session_state) or (st.session_state.pupil=='Выберите..'):
        if 'current_user' in st.session_state:
            remember_fio = st.session_state.current_user
            if remember_fio in pupils:
                pos = pupils.index(remember_fio)
    else:
        #print('Взято с неба', st.session_state.pupil)
        pos = pupils.index(st.session_state.pupil)

    pupil = st.selectbox(':blue[ФИО ученика]', pupils, index = pos, on_change=set_cookies,args =['pupil'], key='pupil')
    
    st.write(':blue[Выберите на сколько будем умножать:]')

    col1, col2, col3, col4,col5 = st.columns(5)
    with col1:
        x1 = st.checkbox('x1', value=False)
        x2 = st.checkbox('x2', value=True)
        
    with col2:
        x3 = st.checkbox('x3', value=True)
        x4 = st.checkbox('x4', value=True)
        
    with col3:
        x5 = st.checkbox('x5', value=True)
        x6 = st.checkbox('x6', value=True)
        
    with col4:
        x7 = st.checkbox('x7', value=True)
        x8 = st.checkbox('x8', value=True)
        
    with col5:
        x9 = st.checkbox('x9', value=True) 
        x10 = st.checkbox('x10', value=False)
    
         
    st.write(':blue[Выберите операцию:]')
    op1, op2 = st.columns(2)
    with op1:
         mult = st.checkbox('Умножение', value=True)
    with op2:
         div = st.checkbox('Деление', value=False)
    if not mult and not div:
        st.write(':red[необходимо выбрать хотя бы одну операцию умножение или деление]')
    
    N =st.slider(':blue[Количество примеров:]', 5, 100,10)
    
    inp = st.selectbox(':blue[Ввод ответа]', ('выбор из четырех предложенных','ввод числа'))
    
    st.write(':blue[Дополнительные параметры:]')
    del1 = st.checkbox('исключить умножение на 1 из х2....x10', value=True)
    del10 = st.checkbox('исключить умножение на 10 из х1....x9', value=True)
    shtraf = st.checkbox('дополнительно повторить ошибочные примеры в конце теста', value=False, disabled=False, help = 'Вопрос будет добавлен в конец теста и будет появляться пока не будет получен верный ответ')
    right_answer = st.checkbox('показать правильный ответ, если ошибка', value=True)




current_parameters = (x1,x2,x3,x4,x5,x6,x7,x8,x9,x10, mult, div, N, inp, pupil)
but = 0
if 'param' not in st.session_state or st.session_state.param !=current_parameters:
    but = 1



if but:
    
    show_buttons()
    #start = st.button('Новый тест', on_click=start_test, args=current_parameters, type='secondary')
    #if pupil != 'Выберите..':
    #    start_rating = st.button('Соревнование', on_click=comp_test, args=current_parameters, type='secondary')

    
  
#у нас уже идет тест
#пока есть вопросы - мы их задаем, но сначала проверяем правильность предыдущего ответа
else:
    alert_mistake = 0 #установится =1, если ошибка и пример выводить не надо будет
    #СНАЧАЛА ПРОВЕРЯЕМ ПРЕДЫДУЩИЙ ОТВЕТ, ЕСЛИ ОН БЫЛ, ТОГДА МОЖЕТ БЫТЬ НАДО ВЫВЕСТИ ОШИБКУ
    
    if 'answer' in st.session_state:
        last_example = st.session_state.answer
    else:
        last_example = 0 #не было ответа
    
    #try:
    #print('answer', answer)

    if type(last_example) is tuple:
        #st.write(last_example, len(last_example), type(last_example))
        if last_example[-1] != last_example[-2]: #если ответы не сходятся
            st.session_state.stat['wrong'] +=1 #считаем ошибку
            st.session_state.stat['mistakes'].append(f'{last_example[0]} = {last_example[-2]}')
            st.session_state.stat['wrong_answer'].append(f'{last_example[0]} = {last_example[-1]}')
            
            #вопросы в штрафной круг на соревновании не копятся 
            if st.session_state.stat['type'] != 'comp':
               st.session_state.crug.append(st.session_state.shot)


            if right_answer and st.session_state.stat['type'] != 'comp': #надо сообщить верный ответ
                #placeholder_big.empty()
                #if st.session_state.last !=1:
                #    next_example()
                st.session_state.answer='' #тут хранится ответ на тест
                st.session_state.q = '' #тут хранится вопрос и ПРАВИЛЬНЫЙ ответ теста  
                st.title(f':red[Ответ неверный]')
                st.title(f'Запомни: {last_example[0]} = {last_example[-2]}')
                alert_mistake = 1 #чтобы не выводить пример
                st.button('Дальше')
        else: #ответ верный, надо посчитать
            st.session_state.stat['good'] +=1












    if not alert_mistake: #тогда берем новый пример и выводим его
        zd = st.session_state.zadacha
        if (len(zd)>0) or (shtraf and len(st.session_state.crug)>0):
            #st.title(zd)
            if len(zd)>0:
                vopros = list(st.session_state.zadacha[0])
                st.session_state.zadacha = st.session_state.zadacha[1:]
            else: #начинаем брать вопросы из штрафного круга
                vopros = list(st.session_state.crug[0])
                vopros=[vopros[1], vopros[0], vopros[2]]  #меняем местами цифры, чтобы жизнь легкой не казалась
                st.session_state.crug = st.session_state.crug[1:] #удаляем из очереди взятый пример
                st.session_state.stat["voprosov"] +=1
            
            st.session_state.current_example = vopros #возможно, что пример придется вернуть в очередб
       
        
           
            func = vopros[2] #получаем функцию
            a,b = vopros[0],vopros[1] #получаем 2 числа
            q,otv = func(a,b)  # q = это запись примера, otv - это ответ в примере
        
            def click_b(*answer):
                #print('llll',answer)
                if inp=='ввод числа':
                    answer= list(answer)
                    answer[2]=st.session_state.text_key
                st.session_state.shot = st.session_state.current_example
                st.session_state.answer=tuple(answer)
                st.session_state.q = answer[:2]
            
                ##if inp!='ввод числа':
                ##    st.session_state.last=1


        
           
            if inp=='ввод числа': 
                with st.form(key='qwe', clear_on_submit=True):
                    st.title(q)
                    answer = st.number_input('Введите ответ',step=1, format='%i', key='text_key') #%d %e %f %g %i %u

                    s_b = st.form_submit_button("Готово", on_click=click_b, args=[q,otv, answer])
                
                   

            else: #кнопки
                 #candidat = [otv-1,otv-2, otv-3,otv+1,otv+2, otv+3]
                 candidat = random.sample([otv-1,otv-2, otv-3,otv+1,otv+2, otv+3], 3)
                 candidat.append(otv)
                 random.shuffle(candidat)
                 ##st.session_state.last=0
                
                 with st.form(key='qwe2'):
                    st.title(q)
                    st.write('Нажмите кнопку с ответом')
                    #выводим кнопки
                    col = st.columns(4)
                    for i in  range(4):
                        with col[i]:
                            st.form_submit_button(use_container_width=True, label = str(candidat[i]), on_click=click_b, args=(q, otv, candidat[i]))
        else:#вопросы закончились, подводим итоги
           
            
            
            #st.title('Всего примеров: '+str(st.session_state.stat['voprosov']))
            st.title(f':green[Правильных ответов: {st.session_state.stat["voprosov"] - st.session_state.stat["wrong"]}]')
            st.title(f':red[Ошибочных ответов: {st.session_state.stat["wrong"]}]')
            t = end_time_cek =time.time() - int(st.session_state.stat['start_time_cek'])
            if  (st.session_state.stat['type'] == 'comp'):
                st.title('Время прохождения: '+str( f'{t:.2f} сек.'))
            if st.session_state.stat['wrong'] !=0:
                st.title(':blue[Запомни эти примеры:]')
                tmp = set(st.session_state.stat['mistakes']) #так как может быть штрафной круг, то надо убрать дубли
                for m in tmp:
                    st.title(f'   {m}')
            show_buttons()
            

            #СОХРАНЯЕМ СТАТИСТИКУ ОБУЧЕНИЯ
            if (st.session_state.stat['type'] == 'train'):
                tmp_dict=st.session_state.stat
                zad=' '.join(tmp_dict['numbers'])
                wrong_answer = ', '.join(tmp_dict['wrong_answer'])
                for_big_stat={'Начало':tmp_dict['start_time'], 'Длит.':f'{t:.2f} сек.', 'Задание': zad, 'Вопросов':tmp_dict['voprosov'], 'Ошибок':tmp_dict['wrong'], 'Ошибки':wrong_answer}
                df_for_big_stat = pd.DataFrame(for_big_stat, index=[0])
                #st.dataframe(df_for_big_stat)
                #st.write(for_big_stat)
                #st.write(tmp_dict['numbers'])
                if 'big_stat' in st.session_state:
                    st.session_state.big_stat = pd.concat([st.session_state.big_stat[st.session_state.big_stat['Начало'] !=tmp_dict['start_time']], df_for_big_stat])
                else:
                    st.session_state.big_stat = df_for_big_stat
                with open(LOG_TRAIN, 'a', encoding='utf8') as handle:
                    #фио, правильно, не правильно, секунд, дата, 1 попытка
                    handle.write(f'{pupil};{RATING_N - tmp_dict["wrong"]};{tmp_dict["wrong"]};{t};{datetime.datetime.now()};{wrong_answer};1\n')
                if wrong_answer: #если есть ошибки, тоже их сохраним в файл
                    with open(ALL_MISTAKES, 'a', encoding='utf8') as handle:
                        wrong_answer = wrong_answer.replace(',','\n')
                        handle.write(f'{wrong_answer}\n')
                    

            
            #РЕЗУЛЬТАТЫ ТЕСТА НА СОРЕВНОВАНИЕ    
            if (st.session_state.stat['type'] == 'comp') and (not pupil in NOT_SAVE_RESULTS) : #у нас тест на соревнование. Надо записать итоги
                tmp_dict=st.session_state.stat

                re_write_file = 0 #надо ли перезаписать файл, перезапись только в случае изменений происходит
                wrong_answer = ', '.join(tmp_dict['wrong_answer'])
                if os.path.isfile(RATING_FILE):
                    with open(RATING_FILE, 'rb') as file:
                        rating = pickle.load(file)
                else: #файла нет, делаем пустую таблицу, видимо первый участник
                    rating = pd.DataFrame({'ФИО':[], 'Правильно':[],'Ошибок':[],'Время (сек.)':[],'Дата':[] }).set_index('ФИО')
                
                if  pupil in rating.index: #если он у нас уже в таблице, смотрим улучшил ли он результат
                    if (rating.at[pupil, 'Ошибок'] > tmp_dict['wrong']) or ((rating.at[pupil, 'Ошибок'] == tmp_dict['wrong']) and (rating.at[pupil, 'Время (сек.)'] > t)): #улучшил результат
                        re_write_file = 1
                        rating.loc[pupil, ['Правильно', 'Ошибок', 'Время (сек.)', 'Дата']] = [RATING_N - tmp_dict['wrong'], tmp_dict['wrong'], t, datetime.datetime.now().strftime('%d.%m.%Y %H:%M') ]
                else: #первый раз попал в рейтинг, до этого его не было
                    re_write_file = 1
                    new_row = {'Правильно':RATING_N - tmp_dict['wrong'],'Ошибок':tmp_dict['wrong'],'Время (сек.)':t, 'Дата': datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}
                    #rating = rating.append(pd.DataFrame(new_row, index=[pupil]))
                    rating = pd.concat([rating, pd.DataFrame(new_row, index=[pupil])])
                if re_write_file: #далее делаем только если были изменения в таблице
                    rating.sort_values(['Ошибок','Время (сек.)'],ascending=[True, True], inplace =True)
                    if "Место" in rating.columns:
                        rating['Место'] = range(1,rating.shape[0]+1)
                    else:
                        rating.insert(0, "Место", range(1,rating.shape[0]+1))
                    with open(RATING_FILE, 'wb') as handle:
                        pickle.dump(rating, handle, protocol=pickle.HIGHEST_PROTOCOL)

                    #ФОТОФИНИШ
                    if 'foto_finish' in st.session_state and st.session_state.foto_finish:
                        print('фотофиниш')
                        try:
                            cam = cv2.VideoCapture(0)
                            ret, frame = cam.read()
                            if not os.path.isdir('arh'):
                                os.mkdir('arh')
                            now = datetime.datetime.now().strftime('%d_%m_%Y__%H_%M')
                            isWritten  = cv2.imwrite(f'arh/{transliterate(pupil)}__{now}.jpg',frame)
                            del cam
                        except:
                            pass
                    
                if (not pupil in NOT_SAVE_RESULTS):    
                    with open(LOG_COMP, 'a', encoding='utf8') as handle:
                    #фио, правильно, не правильно, секунд, дата, 1 попытка
                        handle.write(f'{pupil};{RATING_N - tmp_dict["wrong"]};{tmp_dict["wrong"]};{t};{datetime.datetime.now()};1\n')
                if (not pupil in NOT_SAVE_RESULTS):    
                    if wrong_answer: #если есть ошибки, тоже их сохраним в файл
                        with open(ALL_MISTAKES, 'a', encoding='utf8') as handle:
                            wrong_answer = wrong_answer.replace(',','\n')
                            handle.write(f'{wrong_answer}\n')



     



            
          

with st.expander("РЕЗУЛЬТАТЫ ОБУЧЕНИЯ"):
    if 'big_stat' in st.session_state:
           st.write('Статистика тестов:')
           df = st.session_state.big_stat
           if df.shape[0]>0:
               st.dataframe(st.session_state.big_stat)
               c1, c2 = st.columns(2)
               with c1:
                   hard_test = st.button('Запуcтить тест по ошибкам', on_click =mistake_test, disabled=False)
               with c2:
                   mutirovat = st.checkbox('мутировать примеры', help='примеры будут изменены, например:\nвместо 3х5 будет 5х3, вместо 24:3 будет 24:8')
    else:
           st.write('Здесь будет индивидуальная статистика полностью пройденных тестов')


with st.expander("РЕЗУЛЬТАТЫ СОРЕВНОВАНИЙ"):
    #чтобы не читать файл каждый раз, смотрим на дату его изменения, читаем только если дата изменилась
    
    if os.path.isfile(RATING_FILE):
        last_modify = os.path.getmtime(RATING_FILE)
        if  (not 'last_modify_rating_file' in st.session_state) or (st.session_state.last_modify_rating_file !=last_modify):
           with open(RATING_FILE, 'rb') as file: 
                #print('Читаем рейтинг')
                rating = pickle.load(file)
                st.session_state.last_modify_rating_file =last_modify #сохраняем, чтобы не читать
                st.session_state.last_rating_file = rating            #сохраняем, чтобы не читать
        else:
            #print('не Читаем рейтинг')
            rating = st.session_state.last_rating_file
        #rating.sort_values(['Ошибок','Время (сек.)'],ascending=[True, True], inplace =True)
        ##rating['Место'] = range(1,rating.shape[0]+1)
        #rating.insert(0, "Место", range(1,rating.shape[0]+1))
        st.dataframe(rating)
        st.caption('В таблице лучший результат за все попытки участия в соревновании.')

    else:
        st.write('Результатов пока нет')

with st.expander("ПРИЗ"):
     c1, c2 = st.columns(2)
     with c1:
        st.write('Побеждает участник по результатам соревнований с наименьшим количеством ошибок. В случае, если таких участников несколько, победитель тот, кто выполнил тест быстрее.')
        st.write('Срок проведения чемпионата: с 5 апреля до 24.00 часов 30 апреля 2023 года.')
     with c2:
        st.image('pi.jpg', use_column_width = True, caption='Приз за 1 место: большая пицца "4 сыра".')
    


with st.expander("Инструкция для родителей"):
   
    st.write('Вопросы, отзывы и пожелания отправляйте в telegram:  @makarov75')
    st.video('https://youtu.be/AmSY6_jfc4k')
if 'current_user'  in st.session_state:
    st.caption(st.session_state.current_user)

foto_finish = st.checkbox('Фотофиниш', value = False, key='foto_finish', help ='Автоматическое фото на память при улучшении участником своих результатов в соревновании.')
#if 'stat' in st.session_state:
#    st.write(st.session_state.stat)
##if 'mist' in st.session_state:
##    st.write(st.session_state.mist)
#if 'crug' in st.session_state:
#    st.write(st.session_state.crug)

#if 'shot' in st.session_state:
#    st.write(st.session_state.shot)
