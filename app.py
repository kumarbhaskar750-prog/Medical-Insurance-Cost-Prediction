from flask import Flask, render_template, request, session, redirect,url_for,g
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "your_secret_key"

client = MongoClient('mongodb://localhost:27017')
db = client['bhaskar']


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/first_page')
def first_page():
    return render_template('index.html')

@app.route('/relogin')
def relogin():
    return render_template('login.html')

  
@app.route('/resignup')
def resignup():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    session.pop('user',None)
    username = request.form['username']
    password = request.form['password']
    user = db.new.find_one({'username': username})

    if user['password'] == password:
        g.user = user
        return redirect(url_for("protect"))
    else:
        return render_template('index.html', error="Invalid username or password")

@app.route("/protect")
def protect():
        return render_template('protected.html')



@app.route('/register_save', methods=['POST'])
def register_save():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    phone_number = request.form['phone_number']

    # Validate the form data (e.g., check if username or email already exist)
    # ...

    # Save the data to the database
    user_data = {
        'username': username,
        'email': email,
        'password': password,
        'phone_number': phone_number
    }
    db.new.insert_one(user_data)

    return render_template('login.html')


@app.route("/upload",methods=['GET', 'POST'])
def upload():
    #Main program start
    #import necessary libaries
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from matplotlib import style
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score


    #import dataset
    df = pd.read_csv("data/insurance.csv")

    #remove null value
    df.isnull().sum()

    #convert the strings into integer variables
    df['sex'] = df['sex'].apply({'male':0, 'female':1}.get)
    df['smoker'] = df['smoker'].apply({'yes':1, 'no':0}.get)
    df['region'] = df['region'].apply({'southwest':1, 'southeast':2, 'northwest':3, 'northeast':4}.get)

    #describe x and y 
    X = df.drop(['charges',], axis=1)
    y = df.charges

    #train model
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, random_state=42)
    print("X_train shape: ", X_train.shape)
    print("X_test shape: ", X_test.shape)
    print("y_train shpae: ", y_train.shape)
    print("y_test shape: ", y_test.shape)

    linreg = LinearRegression()

    linreg.fit(X_train, y_train)
    pred = linreg.predict(X_test)

    #accuracy of the model
    print("R2 score: ",(r2_score(y_test, pred)))

    #if you want to print the accuracy in a graph format
    # plt.scatter(y_test, pred)
    # plt.xlabel('Y test')
    # plt.ylabel('Y pred')
    # plt.show()
    
    #inputs
    if request.method == 'POST':
        age = int(request.form.get('age'))
        sex = int(request.form.get('sex'))
        bmi = float(request.form.get('bmi'))
        children = int(request.form.get('children'))
        smoker = int(request.form.get('smoker'))
        region = int(request.form.get('region'))

    data = {'age': age, 'sex': sex, 'bmi': bmi, 'children': children, 'smoker': smoker, 'region': region}
    index = [0]
    cust_df = pd.DataFrame(data, index)


    cost_pred = linreg.predict(cust_df)
    #print("The medical insurance cost of the new customer is: ", cost_pred)
    return render_template('result.html', cost_pred=cost_pred)


    #Main program end

if __name__ == '__main__':
    app.run(debug=True)