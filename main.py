from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/dcc-dbase"
db = SQLAlchemy(app)

class Purchase(db.Model):
    sno = db.Column(db.String(10), primary_key=True)
    reference_no = db.Column(db.String(20), nullable=False)
    # Define other columns for the Purchase table similarly

class Redemption(db.Model):
    sno = db.Column(db.String(10), primary_key=True)
    encashment_date = db.Column(db.String(40), nullable=False)
    # Define other columns for the Redemption table similarly

@app.route('/search', methods=['GET'])
def search():
    table = request.args.get('table')
    column = request.args.get('column')
    query = request.args.get('query')

    if table == 'purchase':
        model = Purchase
    elif table == 'redemption':
        model = Redemption
    else:
        return "Invalid table specified"

    if column:
        results = model.query.filter(getattr(model, column).contains(query)).all()
    else:
        # Modify the filter conditions based on the columns of Purchase and Redemption
        results = model.query.filter(
            db.or_(
                Purchase.sno.contains(query),
                # Add other columns for 'purchase' table as needed
            )
        ).all()

    purchase_results = []
    redemption_results = []
    for result in results:
        if isinstance(result, Purchase):
            purchase_results.append(result)
        elif isinstance(result, Redemption):
            redemption_results.append(result)

    return render_template("search_results.html", purchase_results=purchase_results, redemption_results=redemption_results)

# Define other routes and their corresponding functions similarly

if __name__ == '__main__':
    app.run(debug=True)
