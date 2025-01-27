from flask import Flask,render_template,url_for,request,redirect,session
import testdb
app=Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
@app.route("/signin")
def signin():
   return render_template("fsign_in.html")
@app.route("/signup")
def signup():
    return render_template("fsignup.html")
@app.route("/menu")
def menu():
    if "user" in session:
        data=testdb.getProducts()
        return render_template("fmenu.html",data=data)
    else:
        return render_template("findex.html")
@app.route("/index")
def index():
    return render_template("findex.html")
@app.route("/contact")
def contact():
    return render_template("fcontact.html")
@app.route("/admin")
def admin():
    return render_template("adashboard.html")
@app.route("/register",methods=["POST","GET"])
def register():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        print(name,email,password)
    elif request.method=="GET":
        name=request.args.get("name")
        email=request.args.get("email")
        password=request.args.get("password")
        print(name,email,password)
    s=testdb.signup(name,email,password)
    if(s=="Success"):
        return redirect(url_for("index"))
    else:
        return  render_template("fsignup.html",message=s)
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        print(email,password)
    elif request.method=="GET":
        email=request.args.get("email")
        password=request.args.get("password")
        print(email,password)
    user=testdb.signin(email,password)
    if(user[2]=="u"):
        session["user"]=user
        return redirect(url_for("menu"))
    elif(user[2]=="a"):
        session["user"]=user
        return redirect(url_for("admin"))
    else:    
        return render_template("fsign_in.html",message=user)
@app.route("/cart",methods=["POST","GET"])
def cart():
    session.modified=True
    if request.method=="POST":
        id=request.form["product_id"]
        price=request.form["product_cost"]
        qty=request.form["qty"]
        name=request.form["product_name"]
        print(id,name,price,qty)
        total=float(price)*int(qty)
        p=[id,name,price,qty,total]
        ''' if "cart" not in session:
            session["cart"]=[]
        session["cart"].append(p)'''
    elif request.method=="GET":
        id=request.args.get("product_id")
        price=request.args.get("poduct_cost")
        qty=request.args.get("qty")
        print(id,price,qty)
        name=request.args.get["product_name"]
        total=float(price)*int(qty)
        p=[id,name,price,qty,total]
    if "cart" not in session:
        session["cart"]={}
    dict=session["cart"]
    if(id in dict.keys()):
        p=dict[id]
        p[3]=int(p[3])+int(qty)
        p[4]=float(p[4])+float(total)
    dict[id]=p
    print(type(dict))
    print("cart len is ",dict)
    return redirect(url_for("menu"))
@app.route("/viewcart",methods=["POST","GET"])
def viewcart():
    if "cart" in session:
        data=session["cart"]
        print(type(data))
        return render_template("fviewcart.html",data=data)
    else:
        return render_template("fviewcart.html",data={})
@app.route('/remove_from_cart',methods=["POST","GET"])
def remove_from_cart():
    if request.method=="POST":
        id=request.form["product_id"]
    elif request.method=="GET":
        id=request.args.get("product_id")
    dict=session['cart']
    print(dict)
    print(id)
    dict.pop(id)
    session['cart']=dict
    print(dict)
    return redirect(url_for('viewcart'))  
@app.route("/checkout",methods=["POST","GET"])
def checkout():
    if "cart" in session:
        data=session["cart"]
        return render_template("fcheckout.html",data=data)
    else:
        return render_template("fcheckout.html",data={})
@app.route("/placed",methods=["POST","GET"])
def placed():
    if request.method=="POST":
        padd=request.form["address"]
        rname=request.form["name"]
        pnumber=request.form["phone"]
    elif request.method=="GET":   
        padd=request.args.get("address")
        rname=request.args.get("name") 
        pnumber=request.args.get("phone")
    if "cart" not in session:
        return redirect(url_for("menu"))
    if "user" not in session:
        return redirect(url_for("signin"))
    data=session["cart"]
    user=session["user"]
    email=user[0]
    oid=testdb.getcid(email,padd,rname,pnumber,data)
    session.pop("cart")
    return render_template("fplaced.html",oid=oid)
@app.route("/click")
def click():
    return url_for("index")
@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("index"))
@app.route("/dashboard")
def dashboard():
    return render_template("adashboard.html")
@app.route("/amenu")
def amenu():
    data=testdb.getProducts()
    return render_template("amenu.html",data=data)
@app.route("/addprod",methods=["POST","GET"])
def add_prod():
    return render_template("add_prod.html")
@app.route("/save_product",methods=["POST"])
def save_product():
    f=request.files["iname"]
    f.save("static/"+f.filename)
    iname=f.filename
    name=request.form["name"]
    price=request.form["rate"]
    testdb.insertprod(name,price,iname)
    return render_template("add_prod.html",message="Product Added Successfully")
@app.route("/delprod",methods=["POST","GET"])
def delprod():
    if request.method=="POST":
        id=request.form["id"]
    elif request.method=="GET":
        id=request.args.get("id")
    testdb.delprod(id)
    return redirect(url_for("amenu"))
@app.route("/edit",methods=["POST","GET"])
def edit():
    if request.method=="POST":
        id=request.form["id"]
    elif request.method=="GET":
        id=request.args.get("id")
    data=testdb.getprod(id)
    return render_template("aedit.html",data=data)
@app.route("/update",methods=["POST","GET"])
def update():
    if request.method=="POST":
        id=request.form["id"]
        name=request.form["name"]
        price=request.form["rate"]
        f=request.files["iname"]
        iname=f.filename
        if len(iname)==0:
            iname=request.form["oiname"]
        else:
            f.save("static/"+f.filename)
            iname=f.filename        
    elif request.method=="GET":
        id=request.args.get("id")
        name=request.args.get("name")
        price=request.args.get("rate")
        f=request.files["iname"]
        iname=f.filename
        if len(iname)==0:
            iname=request.form["oiname"]
        else:
            f.save("static/"+f.filename)
            iname=f.filename
    testdb.updateprod(id,name,price,iname)
    return redirect(url_for("amenu"))
@app.route("/orders")
def orders():
    data=testdb.getOrders()
    return render_template("aorders.html",data=data)
@app.route("/showdet",methods=["POST","GET"])
def showdet():
    if request.method=="POST":
        id=request.form["id"]
        name=request.form["name"]
        email=request.form["email"]
        rname=request.form["rname"]
        phone=request.form["phone"]
    elif request.method=="GET":
        id=request.args.get("id")
        name=request.args.get("name")
        email=request.args.get("email")
        rname=request.args.get("rname")
        phone=request.args.get("phone")
    if id is not None:
        det={"id":id,"name":name,"email":email,"rname":rname,"phone":phone}
    else:
        det={}
    data=testdb.showdetails(id)
    return render_template("ashow_det.html",data=data,det=det)
@app.route("/customers",methods=["POST","GET"])
def customers():
    if request.method=="POST":
        email=request.form["email"]
    elif request.method=="GET":
        email=request.args.get("email")
    data=testdb.getcustomers()
    return render_template("acustomer.html",data=data)
@app.route("/delivered",methods=["POST","GET"])
def delivered():
    if request.method=="POST":
        id=request.form["id"]
    elif request.method=="GET":
        id=request.args.get("id")
    testdb.delivered(id)
    return redirect(url_for("orders"))
