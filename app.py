from flask import Flask, render_template, request, redirect, session, flash
import datetime
import aiModel
import dbModule
import random
from base64 import b64encode

app = Flask(__name__)
app.secret_key = 'q1w2e3'

db = dbModule.Database()
model = aiModel.Aimodel()

@app.route('/')         #주소 접속시 intro출력
def hello_world():
    return redirect('/intro')

@app.route('/main', methods = ['POST', 'GET'])  #메인화면 링크
def main():
    if session.get('logininfo') is None:        #로그인된 정보가 없을때
        if request.method == 'POST':        #값이 전달되었을때
            param = request.form
            if param.get('regi') is not None:       #레지스터 폼에서 넘어왔다면
                return redirect('/login')
            else:
                row = db.executeAll("select * from ai_users where user_id = '%s'" % param['id'])        #아이디가 존재하는지 찾기.
                if len(row) != 0:   #하나라도 탐색이 되었다면
                    if row[0]['user_pw'] == param['pw']:        #입력한 패스워드가 등록된 패스워드와 같을때
                        session['logininfo'] = row[0]       #로그인정보 저장
                        return render_template('main.html')
                flash("아이디 또는 비밀번호가 맞지 않습니다")
                return redirect('/login')
        return redirect('/login')
    else:
        print(session['logininfo'])
        return render_template('main.html')

@app.route('/login', methods = ['POST', 'GET'])     #로그인 링크
def login():
    if session.get('logininfo') is None:        #로그인된 정보가 없을때
        return render_template('login.html')
    else:
        return redirect('/main')        #로그인 정보가 있다면 메인 호출


@app.route('/logout', methods = ['POST', 'GET']) #로그아웃 링크
def logout():
    session.pop('logininfo', None)      #로그인 정보 제거
    return redirect('/login')

@app.route('/register', methods = ['POST', 'GET'])  #회원가입 링크
def register():
    if request.method == 'POST':    #전달된 값이 있을때
        param = request.form
        print(" [+} ", param)
        if session.get('regiform') is None:     #회원가입1번 정보가 없다면
            session['regiform'] = param
            return render_template('register1.html')
        else:
            if session.get('regiform2') is None:    #회원가입 2번 정보가 없다면
                session['regiform2'] = param
                return render_template('register2.html')
            else:                                                  #회원가입 1, 2번 정보가 모두 있다면
                regi = session['regiform']
                regi2 = session['regiform2']
                param = request.form
                if param.get('alle') is not None or param.get('alle1') is not None or param.get('alle2') is not None:     #알러지 정보가 하나라도 입력되었다면
                    alle = param['condition'] + '@$' + str(param.get('alle')) + '@$' + str(param.get('alle1')) + '@$' + str(param.get('alle2'))     #알러지정보 입력
                    condi = str(param.get('alle')) + str(param.get('alle1')) +  str(param.get('alle2')) + "알러지를 가지고 있습니다."
                    condi.strip('None')
                else:
                    alle = param['condition']       #선택된 컨디션 정보 입력
                    if param.get('condition') == 'diabetes':
                        condi =  "당뇨를 가지고 있습니다."
                    else:
                        condi = "임산부 입니다."
                db.execute("INSERT INTO ai_users (user_id, user_pw, user_email, user_name, user_age, user_gender, user_height, user_weight, user_has, user_belly) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (regi['id'], regi['pw'], regi['email'], regi2['name'], regi2['age'], regi2['gender'], regi2['height'],regi2['weight'],alle, regi2['belly']))
                db.commit()         #회원정보 db에 정보 입력

                weight = float(regi2['weight'])
                height = float(regi2['height']) / 100
                bmi = weight / (height * height)
                WHtR = round((float(regi2['belly']) / height) / 100, 2)

                if WHtR < 0.43:
                    WHtRcon = '저체중'
                elif WHtR < 0.53:
                    WHtRcon = '정상'
                elif WHtR < 0.58:
                    WHtRcon = '과체중'
                else:
                    WHtRcon = '비만'

                if bmi < 18.5:
                    con = '저체중'
                elif bmi < 22.9:
                    con = '정상'
                elif bmi < 24.9:
                    con = '과체중'
                elif bmi < 29.9:
                    con = '경도비만'
                elif bmi < 34.9:
                    con = '중도비만'
                else:
                    con = '고도비만'

                bmi = round(bmi, 2)

                if regi2['gender'] == '남':
                    avg = round(height * height * 22, 2)
                else:
                    avg = round(height * height * 21, 2)

                session.pop('regiform', None)
                session.pop('regiform2', None)  # 회원가입 정보 제거


                flash("회원가입 되었습니다.")
                return render_template('preCondi.html', weight=weight, height=height, name=regi2['name'], bmi=bmi,con=con, avg=avg, condi = condi, whtr = WHtR, whtrcon = WHtRcon)

                # return render_template('register2.html')
    else:
        session.pop('regiform', None)           #회원가입 버튼이 눌리면 혹시모를 회원가입 정보 제거
        session.pop('regiform2', None)
        row = db.executeAll("select user_id from ai_users")
        return render_template('register.html', ids = row)

@app.route('/preCondi')
def preCondi():
    info = session['logininfo']

    weight = float(info['user_weight'])
    height = float(info['user_height']) / 100
    bmi = weight / (height * height)
    WHtR = round((float(info['user_belly']) / height) / 100, 2)

    if WHtR < 0.43:
        WHtRcon = '저체중'
    elif WHtR < 0.53:
        WHtRcon = '정상'
    elif WHtR < 0.58:
        WHtRcon = '과체중'
    else:
        WHtRcon = '비만'

    if bmi < 18.5:
        con = '저체중'
    elif bmi < 22.9:
        con = '정상'
    elif bmi < 24.9:
        con = '과체중'
    elif bmi < 29.9:
        con = '경도비만'
    elif bmi < 34.9:
        con = '중도비만'
    else:
        con = '고도비만'

    bmi = round(bmi, 2)

    if info['user_gender'] == '남':
        avg = round(height * height * 22, 2)
    else:
        avg = round(height * height * 21, 2)

    if info.get('user_has') == 'None':
        condi = ""
    elif info.get('user_has') == 'allergy':
        condi = info.get('user_has')+ "알러지를 가지고 있습니다."
        condi.strip('allergy')
        condi.strip('@$')
        condi.strip('None')
    else:
        if info.get('user_has') == 'diabetes':
            condi = "당뇨를 가지고 있습니다."
        else:
            condi = "임산부 입니다."
    return render_template('preCondi.html', weight = weight, height = height, name = info['user_name'], bmi=bmi, con=con, avg=avg, condi = condi, whtr = WHtR, whtrcon = WHtRcon)

@app.route('/analy', methods = ['POST', 'GET'])
def analy():
    param = request.form
    sub = param['sub']
    return render_template('analy.html', sub = sub)

# @app.route('/analysis', methods = ['POST', 'GET'])
# def analysis():
#     if request.method == 'POST':
#         param = request.form
#         if param['sub'] == 'nutri':
#             f = request.files['file']       #post로 전달된 이미지 받기
#             img = f.stream.read()        #이미지를 byte형으로 저장
#             result = list(model.yamemodel(f))         #ai모델에 연결하여 이미지 전달 후 분석
#             percent = round(result[1] * 100, 2)         #분석 정확도가 0.nnnn으로 되어있는걸 nn.nn으로 변환
#             result[1] = str(percent) + "%"
#             result[0] = result[0].strip()   #공백 제거
#
#             row = db.executeAll("select * from ai_dish join ai_nutrient on ai_dish.dish_no = ai_nutrient.dish_no where dish_name = '%s'" % result[0])
#             #분석 결과에 해당하는 db데이터 불러오기
#
#             session['savecurlog'] = row[0]['dish_no']
#             print(param['sub'])
#                               #영양분석이 클릭되었을 경우
#             row[0].pop('ai_nutrient.dish_no')
#             row[0].pop('dish_no')
#             row[0].pop('dish_name')
#             row[0].pop('재료')                                    #출력에 필요없는 결과 데이터 제거
#             return render_template('analysis.html', result = result, mimetype='image/png', img=b64encode(img).decode('ascii'), sub = row[0])
#                                                                                                     #A1 (byte로 저장한 이미지 문자열을 b64로 인코드하여 이미지타입을 png로 전달)
#         else:
#             f = request.files['file']  # post로 전달된 이미지 받기
#             img = f.stream.read()  # 이미지를 byte형으로 저장
#             result = list(model.activemodel(f))  # ai모델에 연결하여 이미지 전달 후 분석
#             percent = round(result[1] * 100, 2)  # 분석 정확도가 0.nnnn으로 되어있는걸 nn.nn으로 변환
#             result[1] = str(percent) + "%"
#             result[0] = result[0].strip()  # 공백 제거
#
#             row = db.executeAll(
#                 "select * from ai_dish join ai_nutrient on ai_dish.dish_no = ai_nutrient.dish_no where dish_name = '%s'" %
#                 result[0])
#             # 분석 결과에 해당하는 db데이터 불러오기
#
#             session['savecurlog'] = row[0]['dish_no']
#
#             row[0] = {key : value for key, value in row[0].items() if key == '재료'}
#             test = ""
#             for i in str(row[0]['재료']).split("@$"):     #db에 등록된 기준데이터를 @$기준으로 텍스트 나누어 저장
#                 test = test + "\n" + i
#             row[0]['재료'] = test
#             print(row[0]['재료'])
#             return render_template('analysis.html', result = result, mimetype='image/png', img=b64encode(img).decode('ascii'), sub = row[0])

@app.route('/analysis', methods = ['POST', 'GET'])
def analysis():
    if request.method == 'POST':
        f = request.files['file']       #post로 전달된 이미지 받기
        img = f.stream.read()        #이미지를 byte형으로 저장
        result = list(model.activemodel(f))         #ai모델에 연결하여 이미지 전달 후 분석
        percent = round(result[1] * 100, 2)         #분석 정확도가 0.nnnn으로 되어있는걸 nn.nn으로 변환
        result[1] = str(percent) + "%"
        result[0] = result[0].strip()   #공백 제거

        row = db.executeAll("select * from ai_dish join ai_nutrient on ai_dish.dish_no = ai_nutrient.dish_no where dish_name = '%s'" % result[0])
        #분석 결과에 해당하는 db데이터 불러오기

        session['savecurlog'] = row[0]['dish_no']
        param = request.form
        print(param['sub'])
        if param['sub'] == 'nutri':                         #영양분석이 클릭되었을 경우
            row[0].pop('ai_nutrient.dish_no')
            row[0].pop('dish_no')
            row[0].pop('dish_name')
            row[0].pop('재료')                                    #출력에 필요없는 결과 데이터 제거
            return render_template('analysis.html', result = result, mimetype='image/png', img=b64encode(img).decode('ascii'), sub = row[0])
                                                                                                    #A1 (byte로 저장한 이미지 문자열을 b64로 인코드하여 이미지타입을 png로 전달)
        else:
            row[0] = {key : value for key, value in row[0].items() if key == '재료'}
            test = ""
            for i in str(row[0]['재료']).split("@$"):     #db에 등록된 기준데이터를 @$기준으로 텍스트 나누어 저장
                test = test + "\n" + i
            row[0]['재료'] = test
            print(row[0]['재료'])
            return render_template('analysis.html', result = result, mimetype='image/png', img=b64encode(img).decode('ascii'), sub = row[0])
                                                                                                    #A1

@app.route('/recom')
def recom():
    ran = random.randrange(13, 61)
    row = db.executeAll("select * from ai_dish join ai_nutrient on ai_dish.dish_no = ai_nutrient.dish_no where ai_dish.dish_no = '%i'" % ran)

    name = row[0]['dish_name']
    row[0].pop('ai_nutrient.dish_no')
    row[0].pop('dish_no')
    row[0].pop('dish_name')
    row[0].pop('재료')
    return render_template('recom.html', row = row[0], name = name)
    #예정) 만일 유저가 condition(당뇨,임산부 등)을 가지고 있다면 db의 where not in 을 이용하여 view를 생성한 후 해당 view를 출력

@app.route('/deluser', methods = ['POST', 'GET'])
def deluser():
    if request.method == 'POST':
        form = request.form
        pw = session['logininfo']['user_pw']
        if form['pwc'] != pw:
            flash("비밀번호가 맞지 않습니다.")
            return redirect('/main')
        else:
            db.execute("delete from ai_users where user_no = '%s'" % session['logininfo']['user_no'])
            db.commit()
            session.pop('logininfo', None)
            flash("회원이 탈퇴되었습니다.")
            return redirect('/login')
    return render_template("delcheck.html")

@app.route('/savelog')
def savelog():
    data = session['savecurlog']
    date = datetime.datetime.now()
    print('[+]', data)
    print(session['logininfo']['user_no'])
    db.execute("insert into ai_log(user_no, dish_no, log_cate, log_date)values('%s', '%s', '%s', '%s')" % (session['logininfo']['user_no'], data, 'test', date))
    db.commit()
    return redirect('/main')

@app.route('/log')
def log():
    # row = db.executeAll("SELECT * FROM ai_log where user_no = '%s'" % session['logininfo']['user_no'])
    row = db.executeAll("SELECT dish_name FROM ai_dish where dish_no in (SELECT dish_no FROM ai_log where user_no = '%s')" % session['logininfo']['user_no'])
    print(row)
    return render_template('log.html', logs = row)

@app.route('/finder', methods = ['POST', 'GET'])
def finder():
    if request.method == 'POST':
        femail = request.form['femail']
        print(femail)
        row = db.executeAll("select user_id from ai_users where user_email = '%s'" % femail)
        return render_template('idfound.html', ids = row)
    else:
        return render_template('idfind.html')

@app.route('/mypage', methods = ['POST', 'GET'])
def mypage():
    if session.get('logininfo') is None:
        return redirect('/login')
    if request.method == 'POST':
        login = session['logininfo']
        if request.form['pwc'] == login['user_pw']:
            session['pwch'] = 1
            return render_template('mypage.html', login=login)
        else:
            flash("비밀번호가 맞지 않습니다")
            return redirect('/main')
    else:
        return render_template('isme.html')

@app.route('/changeinfo')
def changeinfo():
    if session.get('logininfo') is None:
        return redirect('/login')
    else:
        if session.get('pwch') is None:
            return redirect('/main')
        else:
            login = session['logininfo']
            session.pop('pwch', None)
            return render_template('changeinfo.html', login = login)

@app.route('/changepw', methods = ['POST', 'GET'])
def changepw():
    if session.get('logininfo') is None:
        return redirect('/login')
    else:
        if session.get('pwch') is None:
            return redirect('/main')
        else:
            if request.method == "POST":
                form = request.form
                print(form)
                if form['ppw'] != session['logininfo']['user_pw']:
                    flash("현재 비밀번호가 맞지 않습니다")
                    session.pop('pwch', None)
                    return redirect('/main')
                else:
                    db.execute("UPDATE ai_users SET user_pw = '%s' WHERE user_id = '%s'" % (form['npw'], session['logininfo'][0]['user_id']))
                    db.commit()
                    row = db.executeAll("select * from ai_users where user_id = '%s'" % session['logininfo'][0]['user_id'])
                    session['logininfo'] = row
                    session.pop('pwch', None)
                    return redirect('/main')
            else:
                login = session['logininfo']
                print(login)
                return render_template('changepw.html', login = login)

@app.route('/findpw', methods = ['POST', 'GET'])
def findpw():
        if request.method == "POST":
            param = request.form
            if len(param) < 2:
                row = db.executeAll("select user_id from ai_users where user_id = '%s'" % param['pwid'])
                print(row)
                if len(row) != 0:
                    session['findpw'] = row[0]
                    print(session['findpw'])
                    return render_template('findpw1.html')
                else:
                    flash("아이디가 존재하지 않습니다.")
                    return redirect('/login')
            else:
                db.execute("UPDATE ai_users SET user_pw = '%s' WHERE user_id = '%s'" % (param['npw'], session['findpw']['user_id']))
                db.commit()
                flash("비밀번호가 변경되었습니다.")
                return render_template('login.html')
        else:
            return render_template('findpw.html')

@app.route('/updateuser', methods = ['POST'])
def updateuser():
    param = request.form.to_dict()
    for i in param.items():
        if i[1] =='':
            param[i[0]] = 'NULL'
        elif i[0] == 'name':
            param[i[0]] = '\'' + i[1] + '\''
    db.execute("UPDATE ai_users SET user_name = COALESCE(%s, user_name), user_age = COALESCE(%s, user_age), user_height = COALESCE(%s, user_height), user_weight = COALESCE(%s, user_weight), user_belly = COALESCE(%s, user_belly) WHERE user_id = '%s'" % (param['name'], param['age'], param['height'], param['weight'], session['logininfo']['user_id']))
    db.commit()
    row = db.executeAll("select * from ai_users where user_id = '%s'" % session['logininfo'][0]['user_id'])
    session['logininfo'] = row
    return render_template('main.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug = True)