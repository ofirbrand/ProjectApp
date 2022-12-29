from ProjectApp import connection, cursor

cursor.execute("SELECT * FROM Librarian")
branches_query = cursor.fetchone()
print(branches_query[2])
# branches_fixed = [''.join(i) for i in branches_query]
# for branch in branches_fixed:
#     print(branch)
#     # print(branch)
