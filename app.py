from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
# import mysql.connector
from werkzeug.utils import secure_filename
import os
import json
import time
from datetime import datetime


app = Flask(__name__)
root = os.getcwd() + "/mysite"
root = os.getcwd()

app.secret_key = "asdlkjf!@Kjsa"
@app.route('/')
def index_kor():
    session['language'] = 'kor'
    return render_template("index_kor.html")

@app.route('/index_en')
def index_en():
    session['language'] = 'en'
    return render_template('index_en.html')

@app.route('/about_kor')
def about_kor():
    return render_template('about_kor.html')

@app.route('/portfolio_architecture')
def portfolio_architecture():
    imgSrcList = load_portfolio('architecture')
    return render_template('portfolio_architecture.html', imgSrcList=imgSrcList, category='All')

@app.route('/portfolio_environment')
def portfolio_environment():
    imgSrcList = load_portfolio('environment')
    return render_template('portfolio_environment.html', imgSrcList=imgSrcList, category='All')

@app.route('/portfolio_character')
def portfolio_character():
    imgSrcList = load_portfolio('character')
    return render_template('portfolio_character.html', imgSrcList=imgSrcList, category='All')


def load_portfolio(category, subCategory='all'):
    imgPath = root+'/static/img/portfolio/' + category + '/'
    with open(imgPath + category + '.csv', 'r') as f:
        portfolioList = f.readlines()
    # portfolioList[0] = portfolioList[0][2:] # 링크 첫번째 주소의 첫 문자가 꺠지는걸 교정
    # portfolioList[0] = 'h' + portfolioList[0]
    print(portfolioList)
    
    imgSrcList = []
    for img in portfolioList:
        if subCategory in img or subCategory == 'all':
            imgSrcList.append(img)
    return imgSrcList

@app.route('/reload_portfolio/<category>')
def reload_portfolio(category):
    category = category.split('-')
    mainCategory = category[0]
    subCategory = category[1]
    imgSrcList = load_portfolio(mainCategory, subCategory)
    return render_template('portfolio_' + mainCategory + '.html', imgSrcList=imgSrcList, subCategory=subCategory)


@app.route('/contact_kor')
def contact_kor():
    return render_template('contact_kor.html')

@app.route('/service_kor')
def service_kor():
    return render_template('service_kor.html')


@app.route('/update_users_change/<update_country>')
def update_users_change(update_country):
    session['country'] = update_country
    return redirect(url_for('update_users'))

@app.route('/update_agent_change/<update_country>')
def update_agent_change(update_country):
    session['country'] = update_country
    return redirect(url_for('update_agent'))



@app.route('/update_agent', methods=['GET', 'POST'])
def update_agent():
    country = session['country']
    session['company_login'] = False
    session['users_login'] = False
    connection, cursor = dbConnect()
    if request.method == 'POST':
        rtn = get_userData("agent")
        cursor.execute("set names utf8")

        sql = "UPDATE agent SET password=%s, name=%s, country=%s, visa=%s WHERE user_id =%s"
        cursor.execute(sql, (rtn[1],rtn[2],rtn[3],rtn[4],rtn[0]))
        connection.commit()
    


    user_id=session['user_id']
    cursor.execute("SELECT * FROM agent WHERE user_id=%s", (user_id,))
    userDetails = cursor.fetchall()
    agentCode = user_id[-4:]
    cursor.execute(f'SELECT * FROM users WHERE agentCode={agentCode}')
    myUser = cursor.fetchall()
    myUserID = tuple([userData[0] for userData in myUser])
    if len(myUserID) == 0:
        sql = f"SELECT * FROM offer WHERE user_id=''"
    elif len(myUserID) == 1:
        sql = f'SELECT * FROM offer WHERE user_id={myUserID[0]}'
    else:
        sql = f'SELECT * FROM offer WHERE user_id IN {myUserID}'
    cursor.execute(sql)
    myOffer = cursor.fetchall()
    offer_ing = []
    offer_fin = []
    for offer in myOffer:
        if offer[7]:
            offer_fin.append(offer)
        else:
            offer_ing.append(offer)
    
    cursor.close()
    connection.close()
    
    return render_template(f'update_agent_{country}.html', userDetails=userDetails, myUser=myUser, offer_ing=offer_ing, offer_fin=offer_fin)



@app.route('/update_company', methods=['GET', 'POST'])
def update_company():
    print('here')
    session['users_login'] = False
    connection, cursor = dbConnect()
    if request.method == 'POST':
        rtn = get_userData("company")
        cursor.execute("set names utf8")
        sql = "UPDATE company SET password=%s, name=%s, adress=%s, manager=%s, sector=%s, task=%s, wage=%s, wage_period=%s, wage_day=%s, bonus=%s, period=%s, work_period=%s, start_hour=%s, start_min=%s, end_hour=%s, end_min=%s, work_day=%s, etc_condition=%s, dwelling=%s, bus=%s, food=%s, insurance=%s, severance=%s, etc_welfare=%s, subscribe=%s WHERE user_id=%s"
        cursor.execute(sql, (rtn[1],rtn[2],rtn[3],rtn[4],rtn[5],rtn[6],rtn[7],rtn[8],rtn[9],rtn[10],rtn[11],rtn[12],rtn[13],rtn[14],rtn[15],rtn[16],rtn[17],rtn[18],rtn[19],rtn[20],rtn[21],rtn[22],rtn[23],rtn[24],rtn[25],rtn[0]))
        connection.commit()

    user_id=session['user_id']
    cursor.execute("SELECT * FROM company WHERE user_id=%s", (user_id,))
    userDetails = cursor.fetchall()
    cursor.execute("SELECT * FROM offer WHERE company=%s AND user_confirm='yes'", (session['user_name'],))
    offers = cursor.fetchall()
    userList = []
    if offers:
        year = datetime.now().date().year

        for offer in offers:
            employee_id = offer[0]
            cursor.execute("SELECT * FROM users WHERE user_id=%s", (employee_id,))
            user = cursor.fetchall()[0]
            user = list(user)
            del user[1]
            del user[-2:]
            user[2] = year-int(user[2])
            userList.append(user)
    cursor.close()
    connection.close()

    # 유저 프로필사진 딕셔너리에 등록
    uploadFile = os.listdir(root+'/static/uploads/users')
    user_profiles = {}
    for user in userList: # user_profiles id명을 키값으로 세팅
        employee_id = user[0]
        user_profiles[employee_id] = 'static/img/noimage.jpg'
    for img in uploadFile:
        imgName = img.split('.')[0]
        imgName = imgName.split('_')[0]
        for user in user_profiles:
            if imgName == user:
                if "profile" in img:
                    imgSrc = "../static/uploads/users/" + img
                    user_profiles[user] = imgSrc

    # 회사 프로필 추가이미지 등록
    uploadFile = os.listdir(root+'/static/uploads/company')
    img_company = []
    img_profile = 'static/img/noimage.jpg'
    for img in uploadFile:
        imgName = img.split('.')[0]
        imgName = imgName.split('_')[0]
        if user_id == imgName:
            imgSrc = "../static/uploads/company/" + img
            if "profile" in img:
                img_profile = imgSrc
            else:
                img_company.append(imgSrc)

    return render_template('update_company.html', userList=userList, user_profiles=user_profiles, userDetails=userDetails, img_profile=img_profile, img_company=img_company)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    connection, cursor = dbConnect()

    user_id=session['user_id']
    cursor.execute("SELECT * FROM company WHERE user_id=%s", (user_id,))
    userDetails = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('payment.html', userDetails=userDetails)


@app.route('/offer', methods=['GET', 'POST'])
def offer():
    connection, cursor = dbConnect()
    if request.method == 'POST':

        cursor.execute("set names utf8")
        date = datetime.now().date()
        company = request.form.get('company')
        charge = request.form.get('charge')
        checkedUser = request.form.get('checkedUser')
        checkedUser = checkedUser.split(',')
        sql = "INSERT INTO offer(user_id, user_name, company, user_confirm, company_confirm, charge, date) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        for user_info in checkedUser:
            user_info = user_info.split('=')
            user_id = user_info[0]
            user_name = user_info[1]
            cursor.execute(sql, (user_id, user_name, company,'','', charge, date))
            connection.commit()

        cursor.close()
        connection.close()

    return redirect(url_for('admin_search'))

@app.route('/offer_detail/<company_name>')
def offer_detail(company_name):
    connection, cursor = dbConnect()
    inputSplit = company_name.split('-')
    country = inputSplit[0]
    name = inputSplit[1]
    cursor.execute("SELECT * FROM company WHERE name=%s", (name,))
    userDetails = cursor.fetchall()
    cursor.close()
    connection.close()
    user_id = userDetails[0][0]
    uploadFile = os.listdir(root+'/static/uploads/company')
    rtn = []
    img_profile = 'static/img/noimage.jpg'
    for img in uploadFile:
        imgName = img.split('.')[0]
        imgName = imgName.split('_')[0]
        if user_id == imgName:
            imgSrc = "../static/uploads/company/" + img
            if "profile" in img:
                img_profile = imgSrc
            else:
                img_company = imgSrc
                rtn.append(img_company)
    return render_template(f'offer_detail_{country}.html', userDetails=userDetails, img_profile=img_profile, img_company=rtn)


@app.route('/offer_detail/user_confirm/<company_name>')
def user_confirm(company_name):

    connection, cursor = dbConnect()
    user_id = session['user_id']
    sql = "UPDATE offer SET user_confirm='yes' WHERE user_id=%s AND company=%s"
    cursor.execute(sql, (user_id, company_name))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('update_users'))

@app.route('/company_confirm/<employee_id>')
def company_confirm(employee_id):
    connection, cursor = dbConnect()
    splitData = employee_id.split('-')
    employee_id = splitData[0]
    company_name = splitData[1]
    print(employee_id, company_name)
    sql = "UPDATE offer SET company_confirm='yes' WHERE user_id=%s AND company=%s"
    cursor.execute(sql, (employee_id, company_name))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('admin_main'))

@app.route('/finishContract/<contract>')
def finishContract(contract):
    connection, cursor = dbConnect()
    splitData = contract.split('-')
    employee_id = splitData[0]
    company_name = splitData[1]
    date = datetime.now().date()
    sql = "UPDATE offer SET complete=%s WHERE user_id=%s AND company=%s"
    cursor.execute(sql, (date, employee_id, company_name))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('admin_main'))
    

@app.route('/change_country')
def change_country():
    urlPath = request.args.get('urlPath', type = str)
    urlPath = urlPath.split('_')[0]
    chng_country = request.args.get('country', type = str)
    return redirect(url_for(f'{urlPath}', input_country=chng_country))


@app.route('/login_korea')
def login_korea():
    return render_template('login_korea.html')
@app.route('/login_china')
def login_china():
    return render_template('login_china.html')

@app.route('/register_users_korea')
def register_users_korea():
    agentCode = session['agentCode']
    return render_template('register_users_korea.html',agentCode=agentCode)
@app.route('/register_users_china')
def register_users_china():
    agentCode = session['agentCode']
    return render_template('register_users_china.html',agentCode=agentCode)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)