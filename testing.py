from ProjectApp import connection, cursor

cursor.execute("SELECT branch_name FROM Branch")
branches_query = cursor.fetchall()
branches_fixed = [''.join(i) for i in branches_query]
for branch in branches_fixed:
    print(branch)
    # print(branch)
