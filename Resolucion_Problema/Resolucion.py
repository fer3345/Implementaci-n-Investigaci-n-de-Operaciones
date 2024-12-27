from pulp import LpMaximize, LpProblem, LpVariable, lpSum

model = LpProblem(name="maximizar_z", sense=LpMaximize)

g = [95.9, 138.15, 247.5, 189.6, 437.59, 193.97]
c = [12.1, 21.35, 32.5, 11.2, 31.2, 45]
v = [28.21, 11.2, 18.17]
t = [1.75, 2.5, 4, 2.3, 7, 12.5]
a = [0.75, 1.4, 2.8, 2.1, 1.2, 4]
d = [20, 30, 15, 5, 10, 20]
x = [[LpVariable(f"x_{i}_{j}", lowBound=0, cat="Integer") for j in range(3)] for i in range(6)]
m = [LpVariable(f"m_{j}", lowBound=0, cat="Continuous") for j in range(3)]
y = [LpVariable(f"y_{j}", cat="Binary") for j in range(3)]

model += (lpSum(g[i] * x[i][j] for i in range(6) for j in range(3)) -
          lpSum(c[i] * x[i][j] for i in range(6) for j in range(3)) -
          lpSum(v[j] * m[j] for j in range(3))) - 10000/4


limits = [50, 30, 15, 5, 10, 20]
for i in range(6):
    model += lpSum(x[i][j] for j in range(3)) <= limits[i]

model += lpSum(t[i] * x[i][j] for i in range(6) for j in range(3)) <= 155

model += lpSum(c[i] * x[i][j] for i in range(6) for j in range(3)) + lpSum(v[j] * m[j] for j in range(3)) <= 6000

for j in range(3):
    model += lpSum(a[i] * x[i][j] for i in range(6)) <= m[j]

model += y[0] + y[1] == 1
model += y[2] == 1

for i in range(6):
    for j in range(3):
        model += x[i][j] <= d[i] * y[j]

for j in range(3):
    for i in range(6):
        model += m[j] >= d[i] * a[i] * y[j]
        print(model.status)

model.solve()

threshold = 1e-5
print("Estado:", model.status)
print("Valor óptimo de Z:", model.objective.value())
for i in range(6):
    for j in range(3):
        if x[i][j].value() > threshold:
            print(f"x_{i+1}_{j+1} = {x[i][j].value()}")
for j in range(3):
    if m[j].value() > threshold:
        print(f"m_{j+1} = {m[j].value()}")
for j in range(3):
    if y[j].value():
        print(f"y_{j+1} = {y[j].value()}")
