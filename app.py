from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>LifeCircle Financial Planner</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial; background:#f4f6f9; padding:40px; }
        .card { background:white; padding:20px; border-radius:10px; box-shadow:0 4px 10px rgba(0,0,0,0.1); margin-bottom:20px;}
        h2 { color:#2c3e50; }
        input, select { padding:8px; width:100%; margin-bottom:10px; }
        button { padding:10px; background:#2c3e50; color:white; border:none; border-radius:5px; width:100%; }
        .safe { color:green; font-weight:bold; }
        .risk { color:red; font-weight:bold; }
    </style>
</head>
<body>

<div class="card">
<h2>LifeCircle Financial Planner</h2>
<form method="POST">
Client Name
<input type="text" name="name" required>

Age
<input type="number" name="age" required>

Annual Income
<input type="number" name="income" required>

Annual Expense
<input type="number" name="expense" required>

Existing Life Cover
<input type="number" name="life_cover" required>

Total Future Goals Cost
<input type="number" name="goals" required>

<button type="submit">Calculate Plan</button>
</form>
</div>

{% if result %}

<div class="card">
<h2>Client: {{name}}</h2>

<p>Liquidity Required: ₹ {{liquidity}}</p>
<p>Savings Required: ₹ {{savings}}</p>
<p>Growth Required: ₹ {{growth}}</p>

<canvas id="myChart"></canvas>

<script>
var ctx = document.getElementById('myChart').getContext('2d');
new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Liquidity', 'Savings', 'Growth'],
        datasets: [{
            data: [{{liquidity}}, {{savings}}, {{growth}}],
        }]
    }
});
</script>

</div>

{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        age = int(request.form["age"])
        income = float(request.form["income"])
        expense = float(request.form["expense"])
        life_cover = float(request.form["life_cover"])
        goals = float(request.form["goals"])

        retirement_age = 60
        working_years = retirement_age - age

        liquidity = (expense / 12) * 6
        insurance_gap = (income * working_years) - life_cover
        savings = expense + insurance_gap
        growth = goals

        return render_template_string(
            HTML,
            result=True,
            name=name,
            liquidity=round(liquidity,2),
            savings=round(savings,2),
            growth=round(growth,2)
        )

    return render_template_string(HTML, result=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
